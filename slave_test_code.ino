#include <avr/sleep.h>
#define interruptPin 2
String onoff;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(10);
  while (!Serial) {}
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}

void Go_Sleep(){
  sleep_enable();
  attachInterrupt(digitalPinToInterrupt(2), wakeUp, LOW);
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  sleep_cpu();
  delay(5000);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(5000); //Do not take this out, delay to help the arduino catch up
  onoff = '59';
}

void wakeUp(){
  sleep_disable();
  while (Serial.available() > 0){
    Serial.read();
  }
  detachInterrupt(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    byte message = Serial.read();
    onoff = String(message, HEX);
    Serial.println(onoff);
  if (onoff == "4e"){ //4e is Hexadecimal for 'N'
    Go_Sleep();
    delay(1000);
  }
  else{
    
    }
  }
  delay(1000);
}
