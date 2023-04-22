import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Initialize_firebase import titles, cred



id = '01' #Changes per player.
team_id = '01' #changes per team
p_ref = db.reference('/')
if list(p_ref.get().keys()).__contains__(f'Team {team_id}'):#Checking if team of the player is in firebase
    ref = db.reference(f'Team {team_id}')
else:#Else, make a new Team ID with the Players ID
    ref.update({f'Team {team_id}':{ f'Player{id}':{'Serial0': titles,#
                     'Testing':{'Serial0': titles},
                     'Training':{'Serial0': titles}}}})


player_list = list(ref.get().keys())
if player_list.__contains__('Player'+id):#Checks list of all players in Team for ID of player
    player_ref = ref.child(f'Player{id}')
else:#Else makes a new player
    ref.update({
    f'Player{id}':{'Serial0': titles,
                     'Testing':{'Serial0': titles},
                     'Training':{'Serial0': titles}}

})
    player_ref = ref.child(f'Player{id}')

def clear_unneeded(string):
    #Clear some common special characters from a string
    question.replace(' ','')
    question.replace('.','')
    question.replace('?', '')
    return string
move = False
while move == False:
    limit = input("How long is your session for(in [hr,mn,sc] format)?:")#Lets you controll how long a session is
    limit = clear_unneeded(limit)
    if len(limit) == 10:#In case they input with the brackets
        sh = 1
        sm = 4
        ss = 7
    elif len(limit) == 8:#In case they dont
        sh = 0
        sm = 3
        ss = 6
    else:
        print("Wrong format, try again")#Otherwise it loops again, so limiting mistakes
        continue
    #This bit converts all the time to seconds
    hour = float(limit[sh:sh + 2]) * 3600
    min = float(limit[sm:sm + 2]) * 60
    sec = float(limit[ss:ss + 2])
    limit = hour + min + sec
    move = True

i=1
entry_dict = {}#
start_time = time.time()
com = "COM12"#Serial Port of Device, can be different on different devices
baud = 9600 #Baud rate of reciever code
x = serial.Serial(com, baud, timeout = 0.1)
while x.isOpen() == True:

    data = str(x.readline().decode('latin-1')).rstrip()#Taking reading of sensor values from serial monitor
    end_time = time.time()
    time_sec = str(end_time-start_time)#This logs time taken for each reading
    if data != '':
         entry_dict[f'Serial{i}'] = data+','+time_sec#Adding time to the recorded data and making it a dictionary for later
         player_ref.update({f'Serial{i}':data+','+time_sec})#updating that reading to Player
         i+=1#Increment so that each entry has a unique but iterable name
         if float(time_sec) >= limit:

            while True:
                send = input("Do you want to use the data to train the model?[Y/N]")
                if send.lower() == 'y':
                    #If they want to use data to train, the completed dictionary from earlier goes in here

                    train_ref = player_ref.child('Training')
                    train_list = list(train_ref.get().keys())
                    last_sess = train_list[-1]
                    last_no = last_sess[6::]
                    print(last_no)
                    train_ref.update({f'Serial{int(last_no)+1}':f'{dataframe}'})
                    break
                elif send.lower() == 'n':
                    #Else that data goes into the Testing file to be saved so it can be looked back on
                    test_ref = player_ref.child('Testing')
                    test_list = list(test_ref.get().keys())
                    last_sess = test_list[-1]
                    last_no = last_sess[6::]
                    test_ref.update({f'Serial{int(last_no)+1}':f'{dataframe}'})
                    break
                else:
                    print("Incorrect input, try again.")#Else, it loops to make sure we dont get invalid input

            break




