
#include <avr/sleep.h>
#define interruptPin 2
String onoff;


//The starting of our code
//this is ACM0
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  while(!Serial){}
  pinMode(13, OUTPUT); 
  digitalWrite(13, HIGH);

  }

//Going to sleep method 
  void Go_Sleep() {
    sleep_enable();
    attachInterrupt(digitalPinToInterrupt(2), Wake_Up, CHANGE);
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.flush();
    sleep_cpu();
    delay(5000);
  }
//Waking up method
  void Wake_Up() {
  sleep_disable();
  digitalWrite(LED_BUILTIN, HIGH);
  detachInterrupt(0);
  }

void loop() {
  
  float do_sensor = analogRead(A1);
  Serial.println(do_sensor);
  float turbidity_sensor = analogRead(A0);
  Serial.println(turbidity_sensor);
  delay(5000);
  
  Serial.println(turbidity_sensor);
  if (Serial.available() > 0) {
    byte message = Serial.read();
    onoff = String(message, HEX);
  
  if (onoff == "4e") {
    Go_Sleep();
    delay(3000);
  }
  
  }
}

 

 



  
  



  


  

  
