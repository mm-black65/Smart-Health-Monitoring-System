#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Pins
#define HEART_PIN 35   // pot1
#define SPO2_PIN 34    // pot2
#define TEMP_PIN 32    // NTC
#define BUZZER_PIN 25  // buzzer

// Thresholds (you can tune later)
int hr_low = 60;
int hr_high = 100;

int spo2_low = 90;

float temp_high = 37.5;

void setup() {
  Serial.begin(115200);

  pinMode(BUZZER_PIN, OUTPUT);

  // OLED init
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED failed");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  // CSV Header (IMPORTANT for ML)
  Serial.println("HeartRate,SpO2,Temperature,Status");
}

void loop() {

  // Read raw values
  int hr_raw = analogRead(HEART_PIN);
  int spo2_raw = analogRead(SPO2_PIN);
  int temp_raw = analogRead(TEMP_PIN);

  // Map to realistic values
  int heartRate = map(hr_raw, 0, 4095, 50, 130);
  int spo2 = map(spo2_raw, 0, 4095, 85, 100);
  float temperature = map(temp_raw, 0, 4095, 30, 42);

  // Condition logic
  String status = "Healthy";

  if (heartRate < hr_low || heartRate > hr_high ||
      spo2 < spo2_low ||
      temperature > temp_high) {
    status = "Risky";
  }

  // Buzzer control
  if (status == "Risky") {
    digitalWrite(BUZZER_PIN, HIGH);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  // OLED Display
  display.clearDisplay();

  display.setCursor(0, 0);
  display.print("HR: ");
  display.print(heartRate);
  display.println(" bpm");

  display.print("SpO2: ");
  display.print(spo2);
  display.println(" %");

  display.print("Temp: ");
  display.print(temperature);
  display.println(" C");

  display.println("----------------");

  display.setTextSize(2);
  display.setCursor(0, 40);
  display.print(status);

  display.display();

  // CSV Output (FOR ML TRAINING)
  Serial.print(heartRate);
  Serial.print(",");
  Serial.print(spo2);
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(status);

  delay(1000);
}
