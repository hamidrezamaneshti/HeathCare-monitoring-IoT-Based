import pyrebase
import time
from datetime import datetime
import csv

#config database
config = {
  "apiKey": "AIzaSyBmSb9Rk1JQD-kGzpYWx-xxh_SSbvQOGgg",
  "authDomain": "ecgfirebaseproject-673ed.firebaseapp.com",
  "databaseURL": "https://ecgfirebaseproject-673ed.firebaseio.com/",
  "storageBucket": "ecgfirebaseproject-673ed.appspot.com"
  }
fb=pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = fb.auth()
db = fb.database()
#authenticate a user
user = auth.sign_in_with_email_and_password("hamidreza.maneshti@gmail.com", "hamidreza3703100")


count=0
timest1 = datetime.now().strftime("%H:%M:%S")
timeday = time.strftime('%d-%m-%Y')
#loop
i=0
a=0
while count<10:
    timest2 = datetime.now().strftime("%H:%M:%S")

    #time_stamp
    c=""
    # timest = datetime.now().strftime("%H:%M:%S:%f")
    print("time before:",timest2)
    timest=datetime.now().timestamp()

    bi = 1
    with open('healthcare/Sample_Dataset','r')as csvFile:
        reader=csv.reader(csvFile, None)
        #assert isinstance(reader)

        for row in reader:
            r=row[0]
            c=str(r)
            print("r in loop: ", c, "  x in loop: ", a)
    #add data to firebase
            ecg={"xValue" :a,"yValue":c}
            a+=1
    #ecg = {"xValue": xvalue, "yValue": yvalue}

            db.child("ecgdata").push(ecg, user['idToken'])

    #db.child("chartTable").push(ecg, user['idToken'])
    #db.child("ECG "+ timeday+"--"+timest1).push(ecg, user['idToken'])
    #db.child("temp " + timeday + "--" + timest1).update({timest: "hamid"}, user['idToken'])
    count+=1

print("time aftre while:",timest2)