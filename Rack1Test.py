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
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

#global varaible
R1LBS = 50;
R2LBS = 50;
R1MS = 0;
R2MS =0;

RPWM = 19;  # GPIO pin 19 to the RPWM on the BTS7960
LPWM = 26;  # GPIO pin 26 to the LPWM on the BTS7960

# For enabling "Left" and "Right" movement
L_EN = 20;  # GPIO pin 20 to L_EN on the BTS7960
R_EN = 21;  # GPIO pin 21 to R_EN on the BTS7960

# Set all of our PINS to output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)

# Enable "Left" and "Right" movement on the HBRidge
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)


rpwm= GPIO.PWM(RPWM, 100)
lpwm= GPIO.PWM(LPWM, 100)

rpwm.ChangeDutyCycle(0)
lpwm.ChangeDutyCycle(0)

rpwm.start(0)
lpwm.start(0)

#Getting ip of wlan 0
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
print(ip)

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
        R1M = strifinal
        root.setvar(name= "rack1_moist" , value=R1M)
        db.child("Rack_No").child("Rack No 1").child("SoilMoisture").set(strifinal)
        print("Moist1 sent to database")
    if msg.topic == 'Rack/Rack1/Light':
        R1L = strifinal
        root.setvar(name="rack1_light", value=R1L)
        db.child("Rack_No").child("Rack No 1").child("Light").set(strifinal)
        print("Light1 sent to database")
    if msg.topic == 'Rack/Rack2/Moist':
        R2M = strifinal
        root.setvar(name= "rack2_moist" , value=R2M)
        db.child("Rack_No").child("Rack No 2").child("SoilMoisture").set(strifinal)
        print("Moist2 sent to database")
    if msg.topic == 'Rack/Rack2/Light':
        R2L = strifinal
        root.setvar(name="rack2_light", value=R2L)
        db.child("Rack_No").child("Rack No 2").child("Light").set(strifinal)
        print("Light2 sent to database")
    if msg.topic == 'Rack/RackTemp/PH':
        db.child("Rack_No").child("Rack No 1").child("WaterParameter").set("PH:" + strifinal)
        db.child("Rack_No").child("Rack No 2").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 3").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 4").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 5").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 6").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 7").child("WaterParameter").set("PH:"+ strifinal)
        db.child("Rack_No").child("Rack No 8").child("WaterParameter").set("PH:"+ strifinal)
        print("PH sent to database")
    if msg.topic == 'Rack/RackTemp/WL':
        db.child("Rack_No").child("Rack No 1").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 2").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 3").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 4").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 5").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 6").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 7").child("WaterLevel").set(strifinal)
        db.child("Rack_No").child("Rack No 8").child("WaterLevel").set(strifinal)
        print("WaterLevel sent to database")
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
    lpwm.ChangeDutyCycle(0)
    rpwm.ChangeDutyCycle(0)
    time.sleep(10)
    rpwm.ChangeDutyCycle(0)
    lpwm.ChangeDutyCycle(0)
    time.sleep(10)
    
def start():
    Tmotor_ctrl.start()

if __name__=="__main__":
    Tmotor_ctrl = threading.Thread(target= motor_control, daemon= True )
    print("Done threading")
    main()
    
#program should end when exited the GUI
def close():
    lpwm.ChangeDutyCycle(0)
    rpwm.ChangeDutyCycle(0)
    exit(0)

def rack1_light_slidercall(value):
    R1LBS = value
    print(value)
    
def rack2_light_slidercall(value):
    R2LBS = value
    print(value)
    
def rack1_moist_slidercall(value):
    R1MS = value
    print(value)
    
def rack2_moist_slidercall(value):
    R2MS = value
    print(value)
    
root.geometry("1280x720")
root.title("Aerofarm system")
root.resizable(width = 1, height=1)
frame_1 = CTK.CTkFrame(root, width = 1200, height = 35,fg_color="blue")
frame_1.place(x = 30, y =5)


frame_2 = CTK.CTkFrame(root, width= 500, height= 500, fg_color="blue")
frame_2.place(x = 100, y = 120)

frame_3 = CTK.CTkFrame(root, width= 500, height= 500, fg_color="blue")
frame_3.place(x = 700, y = 120)

label_temp = CTK.CTkLabel(root,text="AeroFarming Agriculture System", bg_color="blue")
label_temp.place(x= 555, y = 10)

button_1 = CTK.CTkButton( root, text= "START", command= start)
button_1.place(x=575, y=50)

tempdisp = CTK.StringVar(master= root,value = "null" ,name= "tempdis")
rack1_moist =CTK.StringVar(master= root, value="null", name = "rack1_moist")
rack2_moist =CTK.StringVar(master= root, value="null", name = "rack2_moist")
rack1_light =CTK.StringVar(master= root, value="null", name = "rack1_light")
rack2_light =CTK.StringVar(master= root, value="null", name = "rack2_light")

label_temp_val = CTK.CTkLabel(root,textvariable= tempdisp, fg_color="blue")
label_temp_val.place(x=0, y=0)

label_rack1_moist = CTK.CTkLabel(root,textvariable= rack1_moist, fg_color="blue")
label_rack1_moist.place(x=250, y=180)

label_rack2_moist = CTK.CTkLabel(root,textvariable= rack2_moist, fg_color="blue")
label_rack2_moist.place(x=850, y=180)

label_rack1_light = CTK.CTkLabel(root,textvariable= rack1_light, fg_color="blue")
label_rack1_light.place(x=250, y=250)

label_rack2_light = CTK.CTkLabel(root,textvariable= rack2_light, fg_color="blue")
label_rack2_light.place(x=850, y=250)

label_Rack1 = CTK.CTkLabel(root, text= "RACK 1" , bg_color="blue")
label_Rack1.place(x= 325, y = 150)

label_Rack2 = CTK.CTkLabel(root, text= "RACK 2" , bg_color="blue")
label_Rack2.place(x= 925, y = 150)

label_rack1_moist_text =CTK.CTkLabel(root, text= " Soil Moisture = " ,bg_color="blue")
label_rack1_moist_text.place(x = 150 ,y = 180)

lr1mt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr1mt.place(x = 380 ,y = 180)

label_rack2_moist_text =CTK.CTkLabel(root, text= "Soil Moisture = " ,bg_color="blue")
label_rack2_moist_text.place(x =750 ,y = 180 )

lr2mt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr2mt.place(x = 980 ,y = 180)

label_rack1_light_text =CTK.CTkLabel(root, text= "Light intensity = " ,bg_color="blue")
label_rack1_light_text.place(x = 150,y = 250)

lr1lt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr1lt.place(x = 380 ,y = 250)

label_rack2_light_text =CTK.CTkLabel(root, text= "Light intensity = " ,bg_color="blue")
label_rack2_light_text.place(x = 750 ,y = 250)

lr2lt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr2lt.place(x = 980 ,y = 250)

slider_rack1_light= CTK.CTkSlider(root ,command= rack1_light_slidercall, from_=0 , to=100)
slider_rack1_light.place(x= 375 , y= 280)

slider_rack2_light= CTK.CTkSlider(root ,command= rack2_light_slidercall, from_=0 , to=100)
slider_rack2_light.place(x= 975, y= 280)

slider_rack1_moist= CTK.CTkSlider(root ,command= rack1_moist_slidercall, from_=0 , to=100)
slider_rack1_moist.place(x= 375 , y= 210 )

slider_rack2_moist= CTK.CTkSlider(root ,command= rack2_moist_slidercall, from_=0 , to=100)
slider_rack2_moist.place(x= 975, y= 210)

root.protocol("WM_DELETE_WINDOW", close) #when window is closed exit the whole program

root.mainloop()
