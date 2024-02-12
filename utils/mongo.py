from pymongo import MongoClient

USERNAME = 'admin'
PASSWORD = 'hmcblUZX6d5w5V6p'
CONNECTION_STRING = f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.qh8t139.mongodb.net/'
CLIENT = MongoClient(CONNECTION_STRING)