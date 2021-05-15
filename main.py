import requests
import json
import time
from datetime import datetime, timedelta
from fb import ref

print_flag = "Y"

def get_pincodes():
    data = ref.get()
    pinCodes = []
    phoneNumbers = []
    for entry in data.keys():
        k = data.get(entry)
        pinCodes.append(k.get("pinCode"))
        phoneNumbers.append(k.get("phoneNumber"))

    return pinCodes, phoneNumbers

