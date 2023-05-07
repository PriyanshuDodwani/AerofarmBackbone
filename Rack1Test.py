import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import pyrebase
import netifaces as ni
import tkinter as tk
import customtkinter as CTK
import threading
from sys import exit


perc = "%"
#setting GPIO for motor controller
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

#global varaible
R1LBS = 10
R1LBS_SENT=0
R2LBS = 50
R1MS = 0
R2MS =0

RPWM = 19  # GPIO pin 19 to the RPWM on the BTS7960
LPWM = 26  # GPIO pin 26 to the LPWM on the BTS7960

# For enabling "Left" and "Right" movement
L_EN = 20  # GPIO pin 20 to L_EN on the BTS7960
R_EN = 21  # GPIO pin 21 to R_EN on the BTS7960

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
    global R1LBS_SENT
    if R1LBS != R1LBS_SENT:
        client.publish("Rack1L",R1LBS)
        R1LBS_SENT = R1LBS
        print(R1LBS)
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
        client.publish("Rack2L", R2LBS)
    if msg.topic == 'Rack/RackTemp/PH':
        PH = strifinal
        root.setvar(name="phdisp", value= PH)
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
        Wl = strifinal
        root.setvar(name="wldisp" , value=Wl)
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
    if msg.topic == 'Rack/RackTemp/Humid':
        humid = strifinal
        root.setvar(name="humdisp", value=humid)
        db.child("Rack_No").child("Rack No 1").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 2").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 3").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 4").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 5").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 6").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 7").child("Humidity").set(strifinal)
        db.child("Rack_No").child("Rack No 8").child("Humidity").set(strifinal)
        print("Humidity sent to database")
        
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
    global R1LBS
    R1LBS = value
    temp = int(value)
    temp1= str(temp)
    R1LBSpr = "%s%%"%temp1
    root.setvar(name="R1LBS_Var", value=R1LBSpr)
    print(value)
    
def rack2_light_slidercall(value):
    temp = int(value)
    temp1= str(temp)
    R2LBS=temp1
    R2LBSpr = "%s%%"%temp1
    root.setvar(name="R2LBS_Var", value=R2LBSpr)
    print(value)
    
def rack1_moist_slidercall(value):
    temp = int(value)
    temp1=str(temp)
    R1MS = "%s%%"%temp1
    root.setvar(name="R1MS_Var", value=R1MS)
    print(value)
    
def rack2_moist_slidercall(value):
    temp = int(value)
    temp1=str(temp)
    R2MS = "%s%%"%temp1
    root.setvar(name="R2MS_Var", value=R2MS)
    print(value)


#  Local GUI

root.geometry("1280x720")
root.title("Aerofarm system")
root.resizable(width = 1, height=1)

frame_1 = CTK.CTkFrame(root, width = 1200, height = 35,fg_color="blue")
frame_1.place(x = 30, y =5)

frame_2 = CTK.CTkFrame(root, width= 500, height= 250, fg_color="blue")
frame_2.place(x = 100, y = 120)

frame_3 = CTK.CTkFrame(root, width= 500, height= 250, fg_color="blue")
frame_3.place(x = 700, y = 120)

frame_4 = CTK.CTkFrame(root, width=500, height=250, fg_color="blue")
frame_4.place(x = 390, y=390)

label_AF = CTK.CTkLabel(root,text="AeroFarming Agriculture System", bg_color="blue")
label_AF.place(x= 555, y = 10)

button_1 = CTK.CTkButton( root, text= "START", command= start)
button_1.place(x=575, y=50)

label_Common = CTK.CTkLabel(root, text="Common", bg_color="blue")
label_Common.place(x= 620, y= 400)

label_Rack1 = CTK.CTkLabel(root, text= "RACK 1" , bg_color="blue")
label_Rack1.place(x= 325, y = 130)

label_Rack2 = CTK.CTkLabel(root, text= "RACK 2" , bg_color="blue")
label_Rack2.place(x= 925, y = 130)

#Temperature Widgets
label_temp =CTK.CTkLabel(root, text="Temperature = ", bg_color="blue")
label_temp.place(x= 450 ,y= 450)
label_Deg = CTK.CTkLabel(root, text= "Deg C", bg_color="blue")
label_Deg.place(x= 580,y= 450)
tempdisp = CTK.StringVar(master= root,value = "null" ,name= "tempdis")
label_temp_val1 = CTK.CTkLabel(root,textvariable= tempdisp, fg_color="blue")
label_temp_val1.place(x=550, y=450)

#PH Widgets
label_PH =CTK.CTkLabel(root, text="Water PH        = ", bg_color="blue")
label_PH.place(x= 450 ,y= 480)
label_ph_text=CTK.CTkLabel(root, text="Typically 7",bg_color="blue")
label_ph_text.place(x=730 ,y= 480)
phdisp = CTK.StringVar(master= root,value = "null" ,name= "phdisp")
label_ph_val1 = CTK.CTkLabel(root,textvariable= phdisp, fg_color="blue")
label_ph_val1.place(x=550, y=480)

#Water level Widgets
label_WL =CTK.CTkLabel(root, text="Water Level    = ", bg_color="blue")
label_WL.place(x= 450 ,y= 510)
label_wl_text=CTK.CTkLabel(root, text="between 0 to 25",bg_color="blue")
label_wl_text.place(x=730 ,y= 510)
wldisp = CTK.StringVar(master= root,value = "null" ,name= "wldisp")
label_wl_val1 = CTK.CTkLabel(root,textvariable= wldisp, fg_color="blue")
label_wl_val1.place(x=550, y=510)

#Humidity Widgets
label_humid =CTK.CTkLabel(root, text="Humidity = ", bg_color="blue")
label_humid.place(x= 450 ,y= 540)
label_RH = CTK.CTkLabel(root, text= "RH%", bg_color="blue")
label_RH.place(x= 580,y= 540)
label_RH_text=CTK.CTkLabel(root, text="Mumbai typically 55-75",bg_color="blue")
label_RH_text.place(x=730 ,y= 540)
humdisp = CTK.StringVar(master= root,value = "null" ,name= "humdisp")
label_humid_val1 = CTK.CTkLabel(root,textvariable= humdisp, fg_color="blue")
label_humid_val1.place(x=550, y=540)

#Rack 1 Moisture Widgets
label_rack1_moist_text =CTK.CTkLabel(root, text= " Soil Moisture = " ,bg_color="blue")
label_rack1_moist_text.place(x = 150 ,y = 180)
lr1mt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr1mt.place(x = 380 ,y = 180)
rack1_moist =CTK.StringVar(master= root, value="null", name = "rack1_moist")
label_rack1_moist = CTK.CTkLabel(root,textvariable= rack1_moist, fg_color="blue")
label_rack1_moist.place(x=250, y=180)
slider_rack1_moist= CTK.CTkSlider(root ,command= rack1_moist_slidercall, from_=0 , to=100)
slider_rack1_moist.place(x= 375 , y= 210)

R1MS_Var = CTK.StringVar(master= root, value="null" + " %", name="R1MS_Var")
label_R1MS = CTK.CTkLabel(root, text=" Set Moisture = ", bg_color="blue")
label_R1MS.place(x= 150 ,y= 210)
label_R1MS_Var = CTK.CTkLabel(root, textvariable= R1MS_Var, bg_color="blue")
label_R1MS_Var.place(x= 250,y= 210)

#Rack 2 Moisture Widgets
label_rack2_moist_text =CTK.CTkLabel(root, text= "Soil Moisture = " ,bg_color="blue")
label_rack2_moist_text.place(x =750 ,y = 180 )
lr2mt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr2mt.place(x = 980 ,y = 180)
rack2_moist =CTK.StringVar(master= root, value="null", name = "rack2_moist")
label_rack2_moist = CTK.CTkLabel(root,textvariable= rack2_moist, fg_color="blue")
label_rack2_moist.place(x=850, y=180)
slider_rack2_moist= CTK.CTkSlider(root ,command= rack2_moist_slidercall, from_=0 , to=100)
slider_rack2_moist.place(x= 975, y= 210)

R2MS_Var = CTK.StringVar(master= root, value="null" + " %", name="R2MS_Var")
label_R2MS = CTK.CTkLabel(root, text=" Set Moisture = ", bg_color="blue")
label_R2MS.place(x= 750 ,y= 210)
label_R2MS_Var = CTK.CTkLabel(root, textvariable= R2MS_Var, bg_color="blue")
label_R2MS_Var.place(x= 850,y= 210)

#Rack 1 Light Widgets
label_rack1_light_text =CTK.CTkLabel(root, text= "Light intensity = " ,bg_color="blue")
label_rack1_light_text.place(x = 150,y = 250)
lr1lt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr1lt.place(x = 380 ,y = 250)
rack1_light =CTK.StringVar(master= root, value="null", name = "rack1_light")
label_rack1_light = CTK.CTkLabel(root,textvariable= rack1_light, fg_color="blue")
label_rack1_light.place(x=250, y=250)
slider_rack1_light= CTK.CTkSlider(root ,command= rack1_light_slidercall, from_=0 , to=100)
slider_rack1_light.place(x= 375 , y= 280)

R1LBS_Var = CTK.StringVar(master= root, value="null" + " %", name="R1LBS_Var")
label_R1LBS = CTK.CTkLabel(root, text=" Set Brightness = ", bg_color="blue")
label_R1LBS.place(x= 150 ,y= 280)
label_R1LBS_Var = CTK.CTkLabel(root, textvariable= R1LBS_Var, bg_color="blue")
label_R1LBS_Var.place(x= 250,y= 280)

#Rack 2 Light Widgets
label_rack2_light_text =CTK.CTkLabel(root, text= "Light intensity = " ,bg_color="blue")
label_rack2_light_text.place(x = 750 ,y = 250)
lr2lt =CTK.CTkLabel(root, text= " Set Value below from 0 to 100%" ,bg_color="blue")
lr2lt.place(x = 980 ,y = 250)
rack2_light =CTK.StringVar(master= root, value="null", name = "rack2_light")
label_rack2_light = CTK.CTkLabel(root,textvariable= rack2_light, fg_color="blue")
label_rack2_light.place(x=850, y=250)
slider_rack2_light= CTK.CTkSlider(root ,command= rack2_light_slidercall, from_=0 , to=100)
slider_rack2_light.place(x= 975, y= 280)

R2LBS_Var = CTK.StringVar(master= root, value="null" + " %", name="R2LBS_Var")
label_R2LBS = CTK.CTkLabel(root, text=" Set Brightness = ", bg_color="blue")
label_R2LBS.place(x= 750 ,y= 280)
label_R2LBS_Var = CTK.CTkLabel(root, textvariable= R2LBS_Var, bg_color="blue")
label_R2LBS_Var.place(x= 850,y= 280)

root.protocol("WM_DELETE_WINDOW", close) #when window is closed exit the whole program

root.mainloop()
