// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

#include <MQTT.h>
int i=0;
int buzzer = D3;
int board_led = D7;
int led = D6;
void callback(char* topic, byte* payload, unsigned int length);

MQTT client("test.mosquitto.org",1883,callback);
void callback(char* topic, byte* payload, unsigned int length)
{
    i=1;

    
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

    if (!strcmp(p, "intruder"))
        digitalWrite(board_led,HIGH);
    else 
    {
        digitalWrite(board_led,LOW);
        // client.disconnect();
    }
//     if (digitalRead(D7) == HIGH)
//     {
//         tone(buzzer, 2093, 650);
//   }
//     else{
//         digitalWrite(buzzer,LOW);
//         tone(buzzer, 0, 650);
//     }
    delay(3000);
}

void setup() {
    client.connect("ArgonClient");
    pinMode(D7, OUTPUT);
    pinMode(led,OUTPUT);
    pinMode(buzzer,OUTPUT);
    digitalWrite(board_led,LOW);
    // digitalWrite(buzzer,LOW);

    if (client.isConnected()) {
        // client.publish("outTopic/message","hello world");
        client.subscribe("motion");
    }
    Particle.subscribe("gmail_alarm_control_event", myHandler);


}

void loop() {
    // if (client.isConnected()) {
    //     client.loop();
    //     delay(100);
    //     }
    client.loop();
    if (digitalRead(board_led) == HIGH)
    {
        Particle.publish("Security","Intruded");
        digitalWrite(led,HIGH);
        
    }
    else
    {
        digitalWrite(led,LOW);
        tone(buzzer, 0, 650);
        
    }
    
   

}

void myHandler(const char *event, const char *data)
{
  /* Particle.subscribe handlers are void functions, which means they don't return anything.
  They take two variables-- the name of your event, and any data that goes along with your event.
  In this case, the event will be "buddy_unique_event_name" and the data will be "on" or "off"
  */

  if (strcmp(data,"alarm-off")==0) {
    // if subject line of email is "off"
    // digitalWrite(led,LOW);
    digitalWrite(buzzer,LOW);
  }
  else if (strcmp(data,"alarm-on")==0) {
    // if subject line of email is "on"
    // digitalWrite(led,HIGH);
    tone(buzzer, 2093, 6500);
    delay(2);
  }
}