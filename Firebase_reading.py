import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from Initialize_firebase import cred, titles
#This is information to find the player whos data is being checked
team_check = input("Type in the team ID of the player you are checking:")
id_check = input("Input the ID of the player you want to check:")
ref = db.reference(f'Team {team_check}')
player_ref = ref.child(f"Player{id_check}")

def line_fixer(x):
#Fixing lines where the csv is off/has shifted values
    if len(x) != 7:
        return x[len(x)-7:len(x)]


def firebase_to_csv(p):
    #Extract data of current session and making it a dataframe
    ref = db.reference(f'Team {team_check}')
    player_ref = ref.child(f"Player{id_check}")

    with open(f'SensorData.csv', mode='a') as sensor_file:
        sensor_writer = csv.writer(sensor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data = player_ref.get()[f'Serial{p}']#Itterating through each item in Player dictionary except Training and Testing
        sep_data = data.split(',')
        sensor_writer.writerow(sep_data)
    df = pd.read_csv("Sensorli.csv", on_bad_lines=line_fixer, engine='python')
    return  df

def data_to_csv(export_Dict):
    #If you want to export either training or Testing directories to your local computer

    if export_Dict == 'Training' or export_Dict == 'Testing':
        p = 1
        ref = db.reference(f'Team {team_check}')
        player_ref = ref.child(f"Player{id_check}")
        train_ref = player_ref.child(f"{export_Dict}")
        head = player_ref.get()[f'Serial0']#Getting column names from first dictionary
        head_list = titles.split(',')

        while p< len(train_ref):
            with open(f'{export_Dict}{p}.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=head_list)
                writer.writeheader()
                writer.writerows(train_ref[f'Serial{p}'])#Iterating through all the sessions
            p+=1

def test_data_clear(q):
    #If you want to reset the testing data
    if q.lower == 'y':
        ref = db.reference(f'Team {team_check}')
        player_ref = ref.child(f"Player{id_check}")
        test_ref = ref.child(f"Testing")
        player_ref.update({f'Serial0:{titles}'})
        print('Test file cleared')
    else:
        pass




fig,  axs= plt.subplots(2,3)
#Making subplots for different types of reading



def animate(i):#To animate an updating plot

        p = 0
        global axs#So subplots wont reset

        plt.cla()
        df = firebase_to_csv(p)#Gets data, and is updated every pass through


        column_list =list(df.columns.values)#Gets list of data types
        y_list = []
        colours = ['red','orange','blue','pink','green','cyan','magenta','yellow','black', "brown", "purple"]
        #Colours so that different values can be differentiated in graph



        for i in column_list:
                if column_list.index(i) < (len(column_list)-1):
                        y_list.append(df[str(i)].tolist())
                        #Gets first columns as y values in the graph
                else:
                        xpoints = df[i].tolist()#Last time column is x axis

        print(axs)
        for i in range(len(y_list)):
            #Plotting the values in their diffferent suplots, with different colloured lines and legends for identification

            if i == 0 or i ==1:
                axs[0,0].plot(xpoints, y_list[i], label=column_list[i], color=colours[i])
                axs[0,0].legend(column_list[0:2])#Heart rate
            elif i==2:
                axs[0,1].plot(xpoints, y_list[i], label=column_list[i], color=colours[i])
                axs[0,1].legend([column_list[2]])#GSR
            elif i ==3 or i == 4 or i == 5:
                axs[1,0].plot(xpoints, y_list[i], label=column_list[i], color=colours[i])
                axs[1,0].legend(column_list[3:6])#Acceleration in x, y and z direction
            elif i == 6 or i == 7 or i == 8:
                axs[1,1].plot(xpoints, y_list[i], label=column_list[i], color=colours[i])
                axs[1,1].legend(column_list[6:9])#Gyro/Angular acceleration across x, y and z
#Titles for each drawn graph
        axs[0, 0].set_title('Heart Rate')
        axs[0, 1].set_title('GSR')
        axs[1, 0].set_title('Acceleration')
        axs[1, 1].set_title('Rotation')
        for ax in axs.flat:
            ax.set(xlabel='Time(s)')#Labeling x axis
        plt.tight_layout()
        plt.cla()#Clearing lines for animation


        if p <= len(player_ref.get())-4:#Stops animating so error isn't generated
            p+=1

def clear_unneeded(string):
    question.replace(' ','')
    question.replace('.','')
    question.replace('?', '')
    return string


question = input("Would you like to export data?[y/n]:")
question = clear_unneeded(question)
if question.lower() == 'y' or question.lower() == 'yes':
    q = "From Training or Testing?"
    q = clear_unneeded(q)
    data_to_csv(q)#If yes then extract requested data
else:
    print("Okay, moving on")
d = input('Would you like to clear data in Testing? [y/n]:')
d = clear_unneeded(d)
if d.lower() == 'y' or d.lower() == 'yes':
    test_data_clear()#If yes then clear training
else:
    print("Okay, data will remain")
a = input("Would you like to see current session? [y/n]:")
a = clear_unneeded(a)
if a.lower() == 'y' or a.lower() == 'yes':
    #If yes, animate the currently updating graph and show it
    ani = animation.FuncAnimation(fig, animate, interval=100, cache_frame_data=False)  # Running animation in MatplotLib
    plt.show()


