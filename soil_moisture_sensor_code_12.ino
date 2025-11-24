
const int analogPin = A0;   
const int digitalPin = 2;   

void setup() {
  Serial.begin(9600);
  pinMode(analogPin, INPUT);
  pinMode(digitalPin, INPUT);
}

void loop() {
  int rawValue = analogRead(analogPin);
  int moisturePercent = map(rawValue, 1023, 0, 0, 100);

  Serial.print("RAW=");
  Serial.print(rawValue);
  Serial.print("  Moisture=");
  Serial.print(moisturePercent);
  Serial.print("%  D0=");
  Serial.println(digitalRead(digitalPin));

  delay(1000);
}


