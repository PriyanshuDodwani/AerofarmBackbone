#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager
#include <PubSubClient.h>
#include <DHTesp.h>
DHTesp dht;

const char* mqttServer = "192.168.0.171";
const int mqttPort = 1883;
const char* mqtt_username = "aerofarm"; 
const char* mqtt_password = "1234"; 


// setting up MQTT and wifi client

WiFiClient espClient;
PubSubClient client(mqttServer, mqttPort, espClient);


void setup() {
  // put your setup code here, to run once:
  delay(1000); // power saftey delay
  Serial.begin(9600);
  dht.setup(5, DHTesp::DHT22);
  //WiFiManager
  WiFiManager wifiManager;
  wifiManager.autoConnect("RackTemp");
  Serial.println("connected...yeey :)");
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("RackTemp",mqtt_username, mqtt_password)) {
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
    
      if (client.connect("RackTemp",mqtt_username, mqtt_password)) {
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
    float temperature = dht.getTemperature();
    String T1 = String((float)temperature);

    if(client.publish("Rack/RackTemp/Temp",T1.c_str())){

      Serial.println("Temp sent");
      Serial.println(T1.c_str());
    }

    else{
      Serial.println("Temp failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/RackTemp/Temp",T1.c_str());
    }
  delay(3000);
    
    client.loop();
 }
