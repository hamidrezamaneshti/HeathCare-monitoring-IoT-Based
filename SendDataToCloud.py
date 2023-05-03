import pyrebase
import time
from datetime import datetime
import csv

# Configure the database
config = {
    "apiKey": "******",
    "authDomain": "******",
    "databaseURL": "https://ecgfirebaseproject-673ed.firebaseio.com/",
    "storageBucket": "ecgfirebaseproject-673ed.appspot.com"
}
fb = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = fb.auth()
db = fb.database()

# Authenticate a user
user = auth.sign_in_with_email_and_password("****", "****")

count = 0
timest1 = datetime.now().strftime("%H:%M:%S")
timeday = time.strftime('%d-%m-%Y')

# Loop until count reaches 10
i = 0
a = 0
while count < 10:
    timest2 = datetime.now().strftime("%H:%M:%S")

    # Time stamp
    c = ""
    print("time before:", timest2)
    timest = datetime.now().timestamp()

    bi = 1
    with open('healthcare/Sample_Dataset', 'r') as csvFile:
        reader = csv.reader(csvFile, None)

        for row in reader:
            r = row[0]
            c = str(r)
            print("r in loop: ", c, "  x in loop: ", a)
            
            # Add data to Firebase
            ecg = {"xValue": a, "yValue": c}
            a += 1
            db.child("ecgdata").push(ecg, user['idToken'])

    count += 1

print("time after while:", timest2)
