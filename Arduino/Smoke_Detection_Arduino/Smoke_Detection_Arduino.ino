#include <DHT.h>

#define DHTPIN 2           // DHT11 connected to pin 2
#define DHTTYPE DHT11
#define MQ2_PIN A0         // MQ2 sensor to A0
#define BUZZER_PIN 10      // Buzzer to pin 10

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(MQ2_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("✅ Arduino Smoke Detection Initialized...");
  delay(2000);
}

void loop() {
  int smokeValue = analogRead(MQ2_PIN);
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Handle reading errors
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Error reading DHT11!");
    return;
  }

  // Send data to Python
  Serial.print(smokeValue);
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);

  // 🔹 Check if Python sent alert (1 = anomaly, 0 = normal)
  if (Serial.available() > 0) {
    int signal = Serial.parseInt();

    if (signal == 1) {
      tone(BUZZER_PIN, 1000);   // Start buzzer sound
      delay(500);
      noTone(BUZZER_PIN);
    } else {
      noTone(BUZZER_PIN);       // Stop buzzer
    }
  }

  delay(1000);
}

