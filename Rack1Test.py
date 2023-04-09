import paho.mqtt.client as mqtt
import pyrebase

# setting MQTT Parameters
MQTT_ADDRESS = '192.168.0.171'
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
        db.child("Rack_No").child("Rack No 1").child("SoilMoisturer").set(strifinal)
        print("Moist1 sent to database")
    if msg.topic == 'Rack/Rack1/Light':
        db.child("Rack_No").child("Rack No 1").child("Light").set(strifinal)
        print("Light1 sent to database")
    if msg.topic == 'Rack/RackTemp/Temp':
        db.child("Rack_No").child("Rack No 1").child("Temperature").set(strifinal)
        print("Temp sent to database")
    

def main():
    mqtt_client=mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER,MQTT_PASS)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()
    
if __name__=='__main__':
    main()
