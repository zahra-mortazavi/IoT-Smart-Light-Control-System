#include <WiFi.h>
#include <UniversalTelegramBot.h>
#define BOT_TOKEN "your-bot-token"
#define CHAT_ID "your-chat-id"
const char *ssid = "your-ssid";
const char *password = "your-password";
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(4, OUTPUT);
  pinMode(33, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  
  
    Serial.println("\nWiFi connected\nIP: " + WiFi.localIP().toString());
  server.begin();
}

void loop() {
  WiFiClient client = server.accept();
  
  if(client) {
    String request = client.readString();

    if(request.indexOf("POST /") != -1) {
      int bodyStart = request.indexOf("\r\n\r\n") + 4;
      String body = request.substring(bodyStart);
      body.trim();

      int cmdIndex = body.indexOf("cmd=");
      if(cmdIndex != -1) {
        String command = body.substring(cmdIndex + 4);
        
        command.replace("+", " ");
        command.replace("%20", " ");
        
        int ampIndex = command.indexOf('&');
        if(ampIndex != -1) {
          command = command.substring(0, ampIndex);
        }
        command.trim();

        Serial.println(command+"#"); 
        Serial.flush();
        delay(1000);

        unsigned long startTime = millis();
        while (millis() - startTime < 5000) { 
          if (Serial.available() > 0) {
            String answer =  Serial.readStringUntil('\n');
            Serial.println(answer); 
            Serial.flush();
            SetUpLights(answer);
            break;
          }
        }
      }
     

    }

   
    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println("Connection: close");
    client.println();
    client.println("<form method='POST'>");
    client.println("<input type='text' name='cmd' placeholder='Enter command'>");
    client.println("<input type='submit' value='Send'>");
    client.println("</form>");
    
    client.stop();
  }
   if(Serial.available()){
         String answer =  Serial.readStringUntil('\n');
            SetUpLights(answer);
      }
}
void SetUpLights(String answer){
        if(answer=="C") {
          digitalWrite(4, HIGH);
         
        }
        else if(answer=="D") {
          digitalWrite(4, LOW);
         
        }
        else if(answer=="A") {
          digitalWrite(33, HIGH);
          
        }
        else if(answer=="B") {
          digitalWrite(33, LOW);
          
        }
        else if(answer=="E") {
          digitalWrite(33, HIGH);
          digitalWrite(4, HIGH);

        }
        else if(answer=="F") {
          digitalWrite(4, LOW);
          digitalWrite(33, LOW);

        }
        else if(answer=="H") {
          digitalWrite(4, LOW);
          digitalWrite(33, HIGH);

        }
        else if(answer=="G") {
          digitalWrite(33, LOW);
          digitalWrite(4, HIGH);

        }
}
