import importlib
from types import ModuleType
import re
from aiogram import types
import datetime
from pymongo import MongoClient
import src.telegram.content.language as lang



class UserData:
    def __init__(self, client: MongoClient, callback_query: types.Message or types.CallbackQuery) -> None:
        # Mongo DB
        self.db = client['MusicChartsBot']
        self.collection = self.db['userdata']
        
        # User identity from Telegram
        self._id: int = self.get_user_from_callback(callback_query)[0] # From telegram get user ID 
        self.username: str = self.get_user_from_callback(callback_query)[1] # From telegram get username
        
        # User default settings
        self.language = lang.ua
        
        
        # Get user
        self.fetch_database() # Read user from DB if exists, otherwise create one
        self.fetch_user_settings() # Set user details/settings in the class
    
    
    def get_user_from_callback(self, callback_query: types.CallbackQuery or types.Message) -> list[int, str]:
        # types.Message
        try: 
            _id: int = callback_query.from_id
            username: str = callback_query.from_user.username
        
        # types.CallbackQuery
        except AttributeError: # 'CallbackQuery' object has no attribute 'from_id'
            _id: int = callback_query.from_user.id
            username: str = callback_query.from_user.username
        
        return _id, username
    
    
    def fetch_database(self) -> None:
        # Get user data from the database
        db_user: dict = self.get_user_from_db(self._id)
        
        if db_user: # If user exists in database, check if username has changed
            self.validate_username(db_user, self.username)
        elif not db_user: # Add user to the database
            self.collection.insert_one({'_id': self._id, 'username': self.username, **self.default_values()})
    
    
    def fetch_user_settings(self) -> None:
        # Get user data from the database
        db_user: dict = self.get_user_from_db(self._id)
        
        # Update user info in its class
        self.username = db_user['username']
        self.language = importlib.import_module(f'{lang.__name__}.{db_user["language"]}')
    
    
    def get_user_from_db(self, _id: str) -> dict:
        db_user: dict = self.collection.find_one({"_id": _id})
        return db_user
    
    
    def validate_username(self, db_user: dict, username: str) -> None:
        # Update username, if user has changed it
        if username != db_user['username']:
            self.collection.update_one({'_id': db_user['_id']}, {'$set': {'username': username}})
    
    
    def default_values(self) -> dict:
        data = {
            'registration_date': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0),
            'language': 'ua',
            'last_activity': None,
            'search_history': []
            }
        return data
    
    
    def update_search_history(self, title: str) -> None:
        date = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        
        # Update search history
        self.collection.update_one({'_id': self._id}, {"$push": {"search_history": {"$each": [{title: date}], "$position": 0, "$slice": 15}}})
        # Update last activity
        self.collection.update_one({'_id': self._id}, {'$set': {'last_activity': date}})
    
    
    def update_language(self, language: str):
        self.language = importlib.import_module(f'{lang.__name__}.{language}')
        self.collection.update_one({'_id': self._id}, {'$set': {'language': language}})