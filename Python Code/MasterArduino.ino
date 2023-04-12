void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  float voltage = analogRead(A0);
  String volts = String(voltage);
  Serial.println(volts);
  delay(9000);
}
