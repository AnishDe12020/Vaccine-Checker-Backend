import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from dotenv import load_dotenv
import os
import json

try:
    with open("config.json", "r+") as config_file:
        config_file_json = json.load(config_file)
        FIREBASE_DATABASE_URL = config_file_json.get("FIREBASE_DATABASE_URL")
except:
    pass        

load_dotenv()

cred_obj = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred_obj)

db = firestore.client()

data_ref = db.collection(u'data')
data_docs = data_ref.stream()

if __name__ == "__main__":
    for doc in data_docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))