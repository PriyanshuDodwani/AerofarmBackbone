#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager
#include <PubSubClient.h>
#include <DHTesp.h>
DHTesp dht;

const char* mqttServer = "10.0.131.233";
const int mqttPort = 1883;
const char* mqtt_username = "aerofarm"; 
const char* mqtt_password = "1234"; 

const unsigned int MAX_MESSAGE_LENGTH = 31;
String PHval, Waterlvl;
//stringPH=PH:7.16, W:22, L:  39, T:  40;


// setting up MQTT and wifi client

WiFiClient espClient;
PubSubClient client(mqttServer, mqttPort, espClient);


void setup() {
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
85
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
    while (Serial.available() > 0){
      static char message[MAX_MESSAGE_LENGTH];
      static unsigned int message_pos = 0;
      String inByte = Serial.readString();
      inByte.trim();
      PHval = (inByte.substring(3, 8));
      Waterlvl = (inByte.substring(12, 14));
    }
    float temperature = dht.getTemperature();
    float humidity = dht.getHumidity();
    String T1 = String((float)temperature);
    String H1 = String((float)humidity);
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
    if(client.publish("Rack/RackTemp/Humid",H1.c_str())){

      Serial.println("Temp sent");
      Serial.println(H1.c_str());
    }

    else{
      Serial.println("Temp failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/RackTemp/Humid",H1.c_str());
    }

    if(client.publish("Rack/RackTemp/PH",PHval.c_str())){

      Serial.println("PH sent");
      Serial.println(PHval.c_str());
    }

    else{
      Serial.println("Temp failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/RackTemp/PH",PHval.c_str());
    }

    if(client.publish("Rack/RackTemp/WL",Waterlvl.c_str())){

      Serial.println("WL sent");
      Serial.println(Waterlvl.c_str());
    }

    else{
      Serial.println("Temp failed to send. Reconnecting to MQTT Broker and trying again");
      connect_MQTT();
      delay(10);
      client.publish("Rack/RackTemp/WL",Waterlvl.c_str());
    }
  delay(2000);
    
    client.loop();
 }
