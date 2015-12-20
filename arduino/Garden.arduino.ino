
#include <WString.h>

int waterPin  = 12;
int lightPin  = 11;
int ledPin    = 13;



String sensors_ids[] = {
  "ded2ea9e8f028eb7bc301461314fd34fd2f5172947c3dea0e71696f8b8fcd8e6",
  "7b15bcdd9f91d9b8d5558bec3437485011ffe7ba5cf8c7e24e67042363408c45",
  "247c32aad7cac61314f1e2aa8d0faa3299ca3853d4226373864e60a8278f0f6a",
};
int sensors_pins[] = {
  A0,
  A1,
  A2
  
};
 


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);


  
  for(int i = 0; i < sizeof(sensors_pins) / 2; i++ ){
    pinMode(sensors_pins[ i ], INPUT );  
  }

  
  pinMode(waterPin, OUTPUT);
  pinMode(lightPin, OUTPUT);
  pinMode(ledPin  , OUTPUT);
  
  digitalWrite(waterPin , HIGH );
  digitalWrite(lightPin , HIGH );
  digitalWrite(ledPin   , LOW) ;


}

void loop() {
  // put your main code here, to run repeatedly:
  readIn();
  sendOut();
}
void sendOut(){
  for(int i = 0; i < sizeof(sensors_pins) / 2; i++){
    Serial.print(sensors_ids[ i ] + "=" + String( map(analogRead(sensors_pins[ i ]), 302, 1023,0,100) ) +";");
  }
  Serial.println("DONE;");
  Serial.flush();
}
int readIn(){
    
    String serial_in;
    while(1 == 1 ){
        digitalWrite(ledPin , HIGH) ;
        if(Serial.available() > 0 ){
        serial_in = Serial.readStringUntil(';');
        
        String function = serial_in.substring(0, serial_in.indexOf("=") );
        int    value = serial_in.substring( (serial_in.indexOf("=") + 1) , ( serial_in.length() ) ).toInt();
    
        if( function.equals("WATER") ){
            modulateOutput( waterPin , value );
          
        }
        if( function.equals("LIGHT") ){
            modulateOutput( lightPin , value );
          
        }
        if( function.equals("TEST") ){
            test();
            digitalWrite(waterPin, LOW );
            digitalWrite(lightPin, LOW);
        }
        if( function.equals("DONE") ){
          digitalWrite(ledPin , LOW) ;
          return 0;
        }
      }
    }
}
void modulateOutput( int pin, bool output ){
  digitalWrite(pin, ! output);
}


void test() {

  for(int i = 0; i < 10; i++){
    digitalWrite(waterPin, HIGH);
    digitalWrite(lightPin, LOW );
    delay(1000);
    digitalWrite(waterPin, LOW );
    digitalWrite(lightPin, HIGH);
    delay(1000);
    digitalWrite(waterPin, LOW );
    digitalWrite(lightPin, LOW);
    delay(1000);
  }
}


