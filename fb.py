import firebase_admin
from firebase_admin import db
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

cred_obj = firebase_admin.credentials.Certificate('firebase_config.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':os.getenv("FIREBASE_DATABASE_URL") or FIREBASE_DATABASE_URL
})

ref = db.reference("users")

if __name__ == "__main__":
    values = ref.get()
    print(type(values))