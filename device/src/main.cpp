#include "Arduino.h"
#include "TinyWS2812B.h"

#define LED_PIN     3
#define NUM_LEDS    144

TinyWS2812B leds(LED_PIN, NUM_LEDS);

void startHandshake();

void setup() {
    Serial.begin(115200);

    // wait for serial port to connect. Needed for native USB port only
    while (!Serial);

    leds.clear();
    leds.updateLeds();

    startHandshake();
}

void startHandshake() {
    while (Serial.available() == 0) {
        Serial.write(0xfe);
        Serial.write(0xfa);
        delay(300);
    }
    Serial.read();
}

unsigned long time = 0;
bool change = false;

void loop() {
    if (Serial.available() > 0) {
        while (Serial.available() >= 4) {
            int index = Serial.read();
            int r = Serial.read();
            int g = Serial.read();
            int b = Serial.read();

            leds.setColor(index, r, g, b);
            change = true;
        }

        Serial.write(0xff);
        Serial.write(0xff);

        delay(100);
    }

    if (change) {
        if (millis() - time >= 100) {
            change = false;
            time = millis();
            leds.updateLeds();
        }
    }
}