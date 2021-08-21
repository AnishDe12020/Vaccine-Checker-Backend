import requests
import json
import time
from datetime import datetime, timedelta
from fb import data_docs
from dotenv import load_dotenv
import os
import re
import smtplib

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print(EMAIL_ADDRESS, EMAIL_PASSWORD)

DAYS_IN_FUTURE = 1
AGE = 50
DAYS_TO_CHECK_FOR = 1
PRINT_FLAG = "Y"

text = ""

s = smtplib.SMTP("smtp.gmail.com", 587)
s.starttls()
s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

print("SMTP client has been set up")

todays_date = datetime.today()
dates = [todays_date + timedelta(days=i+DAYS_IN_FUTURE) for i in range(DAYS_TO_CHECK_FOR)]
dates = [i.strftime("%d-%m-%Y") for i in dates]

data = []
for doc in data_docs:
    data.append(doc.to_dict())

pinCodes = []
for user in data:
    pinCodes.append(user.get("pinCode"))

uniquePinCodes = set(pinCodes)

while True:
    counter = 0
    for pinCode in uniquePinCodes:
        for date in dates:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pinCode, date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            print(URL)

            response = requests.get(URL, headers=header)

            if response.ok:
                print("API call successful!!!")

                response_json = response.json()

                flag = False

                if response_json["centers"]:            
                    if(PRINT_FLAG.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= AGE and session["available_capacity"] > 0:
                                    print('Pincode: ' + pinCode)
                                    print("Available on: {}".format(date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    text += """
Pincode: {0}
Available on: {1}
\t Name: {2}
\t Block Name: {3}
\t Price: {4}
\t Availability: {5}
                                    """.format(
                                        pinCode,
                                        date,
                                        center["name"],
                                        center["block_name"],
                                        center["fee_type"],
                                        session["available_capacity"]
                                    )

                                    
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                        text += "\t Vaccine type: {0}".format(session["vaccine"])
                                    print("\n")

                                    text += "\n\n\n"

                                    counter += 1

                                    # print(type(date))
                                    # print(type(str(date)))

                                    # date = datetime.strptime(str(date), "%d-%m-%Y")

                                    # _date = date
                                    # try:
                                    #     day = _date.strftime("%d")

                                    # except:
                                    #     day = datetime.strptime(_date, "%d")

                                    # _date = date
                                    # try:
                                    #     month = _date.strftime("%d")

                                    # except:
                                    #     month = datetime.strptime(_date, "%d")

                                    # _date = date
                                    # try:
                                    #     year = _date.strftime("%d")

                                    # except:
                                    #     year = datetime.strptime(_date, "%d")

                                    # try:
                                    #     text = "We have found you a slot on {} of {}, {}.\n".format(date.strftime("%d"), date.strftime("%B"), date.strftime("%Y"))
                                    # except:
                                    #     text = "We have found you a slot on {} of {}, {}.\n".format(datetime.strptime(date, "%d"), datetime.strptime(date, "%B"), datetime.strptime(date, "%Y"))

                                    try:
                                        date = datetime.strptime(date, "%d-%m-%Y")
                                    except:
                                        # date = date.strftime("%d-%m-%Y")
                                        pass

                                    text = "We have found you a slot on {} of {}, {}.\n".format(date.date, date.month, date.year)
                                    text += "The center name is {} and the block name is {}.\n".format(center["name"], center["block_name"])
                                    text += "The price is {}.\n".format(center["fee_type"])
                                    text += "There are {} slots available.\n".format(session["available_capacity"])

                                    if session["vaccine"] != "":
                                        text += "The type of vaccine available is {}.\n".format(session["vaccine"])


                                    associatedEmailIds = []

                                    for i in data:
                                        if pinCode == i.get("pinCode"):
                                            associatedEmailIds.append(i.get("email"))

                                    print(associatedEmailIds)
      

                                else:
                                    pass

                else: pass

            else:
                print("No Response!!!")    

        if counter == 0:
            print("No slots available!!!")
        else:
            s.sendmail(EMAIL_ADDRESS, associatedEmailIds, text)
            print("Done Searching!!!")
        


    time.sleep(1800)