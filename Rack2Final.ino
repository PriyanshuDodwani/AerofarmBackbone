#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
#include <Wire.h>
#include <BH1750.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager
#include <PubSubClient.h>
#include<FastLED.h>
#define LED_PIN 2
#define NUM_LEDS 21
#define LED_TYPE WS2811
#define COLOR_ORDER RBG


CRGB leds[NUM_LEDS];
BH1750 lightMeter;
const int moist_sensor_pin = A0;

const char* mqttServer = "10.0.131.126"; // Rpi IP
const int mqttPort = 1883;
const char* mqtt_username = "aerofarm"; 
const char* mqtt_password = "1234"; 
int required_light = 50;

// Callback for Mqtt reciving messages
void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
    Serial.println();
  
  String message = "";
  for (int i = 0; i < length; i++) {
    message+=(char)payload[i];
  }
  Serial.println("-----------------------");
  required_light = message.toInt();
  Serial.println(required_light);
    
}

// setting up MQTT and wifi client

WiFiClient espClient;
PubSubClient client(mqttServer, mqttPort, callback, espClient);


void setup() {
  // put your setup code here, to run once:
  delay(1000); // power saftey delay
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  Serial.begin(9600);
  Wire.begin();
  //WiFiManager
  WiFiManager wifiManager;
  wifiManager.autoConnect("Rack1");
  Serial.println("connected...yeey :)");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("Rack1",mqtt_username, mqtt_password)) {
      client.subscribe("Rack1L");
      Serial.println("connected");

    } 
    else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
}
}

// If we get disconnected in between the code this will help to reconnect to MQTT
void connect_MQTT(){
   while (!client.connected()) {
    
      if (client.connect("Rack1",mqtt_username, mqtt_password)) {
          client.subscribe("Rack1L");
          Serial.println("connected");
        } 
        else {
    
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
        }
   }
}

void loop() {
  for(int i = 0 ; i < NUM_LEDS; i++){
    leds[i] = CRGB::Purple;
    FastLED.setBrightness(required_light);
    //Serial.println(required_light);
    FastLED.show();
    }
    client.subscribe("Rack1L");
    float moisture_percentage;
    moisture_percentage = ( 100.00 - ( (analogRead(moist_sensor_pin)/1024.00) * 100.00 ) );
    //Serial.print("Soil Moisture(in Percentage) = ");
    //Serial.print(moisture_percentage);
    //Serial.println("%");
    float lux = lightMeter.readLightLevel();
    //Serial.print("Light: ");
    //Serial.print(lux);
    //Serial.println(" lx");
    lightMeter.configure(BH1750::ONE_TIME_HIGH_RES_MODE);

    String M1 = String((float)moisture_percentage);
    String L1 = String((float)lux);

    if(client.publish("Rack/Rack1/Moist",M1.c_str())){

      Serial.println("Moisture sent");
      Serial.println(M1.c_str());
    }

    else{
      Serial.println("Moisture failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/Rack1/Moist",M1.c_str());
    }
    if(client.publish("Rack/Rack1/Light",L1.c_str())){

      Serial.println("Light sent");
      Serial.println(L1.c_str());
    }
   else {
      Serial.println("Light failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/Rack1/Light",L1.c_str());
  } 
  client.loop();
  delay(3000);
 }
