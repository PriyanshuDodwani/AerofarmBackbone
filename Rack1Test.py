import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import pyrebase
import netifaces as ni
import tkinter as tk
import customtkinter as CTK
import threading
from sys import exit

#setting GPIO for motor controller
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

#Getting ip of wlan 0
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

# setting MQTT Parameters
MQTT_ADDRESS = ip
MQTT_USER = 'aerofarm'
MQTT_PASS = '1234'
MQTT_TOPIC = 'Rack/+/+'

#Setting config for Firebase
config = {
  "apiKey": "AIzaSyAzkf_ej7NEUhaBu4czuWE01gIHaSg2pig",
  "authDomain" : "aerofarm-ly.firebaseapp.com",
  "databaseURL" : "https://aerofarm-ly-default-rtdb.firebaseio.com",
  "storageBucket" : "aerofarm-ly.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database() #creating firebase database

CTK.set_appearance_mode("dark")
CTK.set_default_color_theme("blue")
root = CTK.CTk()

#varaible to stop program
stop_var =0


def on_connect (client, userdata,flags,rc):
    print('connected with result code' +str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic)
    stri=str(msg.payload)
    strij= stri.replace("b","")
    strifinal = strij.replace("'","")
    print(strifinal)
    if msg.topic == 'Rack/Rack1/Moist':
        db.child("Rack_No").child("Rack No 1").child("SoilMoisture").set(strifinal)
        print("Moist1 sent to database")
    if msg.topic == 'Rack/Rack1/Light':
        db.child("Rack_No").child("Rack No 1").child("Light").set(strifinal)
        print("Light1 sent to database")
        
    if msg.topic == 'Rack/RackTemp/Temp':
        temperature = strifinal
        root.setvar(name= "tempdis" , value= temperature)
        db.child("Rack_No").child("Rack No 1").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 2").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 3").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 4").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 5").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 6").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 7").child("Temperature").set(strifinal)
        db.child("Rack_No").child("Rack No 8").child("Temperature").set(strifinal)
        print("Temp sent to database")
        
def main():
    mqtt_client=mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER,MQTT_PASS)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_start()

def motor_control():
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(24,GPIO.LOW)
    time.sleep(5)
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.HIGH)
    time.sleep(5)
    motor_control()
    
def start():
    Tmotor.start()

if __name__=="__main__":
    Tmotor = threading.Thread(target= motor_control, daemon= True )
    print("Done threading")
    main()
    
#program should end when exited the GUI
def close():
    exit(0)
    
root.geometry("1280x720")
root.title("Aerofarm system")
root.resizable(width = 1, height=1)
frame_1 = CTK.CTkFrame(root, width = 1200, height = 35,fg_color="blue")
frame_1.place(x = 30, y =5)


frame_2 = CTK.CTkFrame(root, width= 500, height= 500, fg_color="blue")
frame_2.place(x = 100, y = 120)

frame_3 = CTK.CTkFrame(root, width= 500, height= 500, fg_color="blue")
frame_3.place(x = 700, y = 120)

label_temp = CTK.CTkLabel(root,text="Temperature =", bg_color="blue")
label_temp.place(x= 600, y = 10)

button_1 = CTK.CTkButton( root, text= "START", command= start)
button_1.place(x=575, y=50)

tempdisp = CTK.StringVar(master= root,value = "null" ,name= "tempdis")

label_temp_val = CTK.CTkLabel(root,textvariable= tempdisp, fg_color="blue")
label_temp_val.place(x=690, y=10)

label_Rack1 = CTK.CTkLabel(root, text= "RACK 1" , bg_color="blue")
label_Rack1.place(x= 325, y = 150)

label_Rack2 = CTK.CTkLabel(root, text= "RACK 2" , bg_color="blue")
label_Rack2.place(x= 925, y = 150)

root.protocol("WM_DELETE_WINDOW", close) #when window is closed exit the whole program
root.mainloop()

    


