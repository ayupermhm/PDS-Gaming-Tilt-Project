import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
#Helps initialize The firebase
cred = credentials.Certificate("Firebase_sdk.json")
firebase_admin.initialize_app(cred, { 'databaseURL':'https://ctd-lab-project-7c38e-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference('/')
#Titles of data being recieved
titles = 'Red_light,IR,GSR,AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ, Time'
id = '01' #Changes per player.
team_id = '01' #changes per team
ref.set({#Setup of the dictionary format
    f'Team {team_id}':{
        f'Player{id}':{ 'Serial0': titles,
                     'Testing':{'Serial0': titles}, #Incase data is not, so it can be looked back on
                     'Training':{'Serial0': titles}} #incase data is being used to train the model
    }
})