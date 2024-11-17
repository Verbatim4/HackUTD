import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://edir-87cf6-default-rtdb.firebaseio.com/' 
})

def get_database_reference(dataset: str):
    return db.reference(dataset)