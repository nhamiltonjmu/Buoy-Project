void setup() {
  Serial.begin(115200);
  float current = 7;
  
}
//ACM1
void loop() {
  float current = analogRead(A2);
  Serial.println(current);
  float voltage = analogRead(A3);
  Serial.println(voltage);
  delay(5000);

}
