#include <Adafruit_NeoPixel.h>

const int potPin = A0;
const int ledPin = D4;
const int numPixels = 1;

Adafruit_NeoPixel strip(numPixels, ledPin, NEO_GRB + NEO_KHZ800);

int lastPotVal = -1;
unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(115200);

  strip.begin();
  strip.setBrightness(40);
  strip.show();
}

void loop() {
  int rawVal = analogRead(potPin);
  
  if (abs(rawVal - lastPotVal) > 8) { 
    int percent = map(rawVal, 0, 1023, 0, 100);

    int red = map(percent, 0, 100, 255, 0);
    int green = map(percent, 0, 100, 0, 255);
    strip.setPixelColor(0, strip.Color(red, green, 0));
    strip.show();

    if (millis() - lastSendTime > 20) {
      Serial.print("BRIGHT_VAL:");
      Serial.println(percent);
      lastSendTime = millis();
    }
    
    lastPotVal = rawVal;
  }

  delay(10);
}
