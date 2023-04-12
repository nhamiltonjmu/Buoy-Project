void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  float turbidity = analogRead(A1);
  float sat = analogRead(A0);
  String turbs = String(turbidity);
  String sats = String(sat);
  Serial.println(sats + ", " + turbs);
  delay(9000);
}
