import requests
import json
import time
from datetime import datetime, timedelta
from fb import ref
import pyttsx3

engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-70)

print_flag = "Y"
days_to_check_for = 1
age = 50

todays_date = datetime.today()
dates = [todays_date + timedelta(days=i+1) for i in range(days_to_check_for)]
dates = [i.strftime("%d-%m-%Y") for i in dates]


def get_pincodes():
    data = ref.get()
    # print(data)
    pinCodes = []
    phoneNumbers = []
    for entry in data.keys():
        k = data.get(entry)
        pinCodes.append(entry)
        phoneNumbers.append(k)
    uniquePinCodes = list(set(pinCodes))
    return pinCodes, phoneNumbers, uniquePinCodes, data

while True:
    pinCodes, phoneNumbers, uniquePinCodes, data = get_pincodes()

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
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= age and session["available_capacity"] > 0:
                                    print('Pincode: ' + pinCode)
                                    print("Available on: {}".format(date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")

                                    date = datetime.strptime(date, "%d-%m-%Y")

                                    text = "We have found you a slot on {} of {}, {}.\n".format(date.strftime("%-d"), date.strftime("%B"), date.strftime("%Y"))
                                    text += "The center name is {} and the block name is {}.\n".format(center["name"], center["block_name"])
                                    text += "The price is {}.\n".format(center["fee_type"])
                                    text += "There are {} slots available.\n".format(session["available_capacity"])

                                    if session["vaccine"] != "":
                                        text += "The type of vaccine available is {}.\n".format(session["vaccine"])


                                    associatedPhoneNumbers = []

                                    for i in data.keys():
                                        if i == pinCode:
                                            associatedPhoneNumbers.append(data.get(i))

                                    filename = "_".join(associatedPhoneNumbers)
                                    filename = "./recordings/" + filename + ".mp3"
                                    print("TTS Start")
                                    engine.save_to_file(text, filename)
                                    engine.runAndWait()
                                    print("TTS End")



                                    # print(associatedPhoneNumbers)        

                                else:
                                    pass

                else: pass

            else:
                print("No Response!!!")      

    time.sleep(1800)