#include "Arduino.h"
#include "TinyWS2812B.h"

#define LED_PIN     3
#define NUM_LEDS    144

TinyWS2812B leds(LED_PIN, NUM_LEDS);

void runCommand(int cmd);

void setup() {
    Serial.begin(115200);

    // wait for serial port to connect. Needed for native USB port only
    while (!Serial);

    leds.clear();
    leds.updateLeds();
}

int color[3];
size_t colorIndex = 0;
int zone = 0;

void loop() {
    while (Serial.available()) {
        int data = Serial.read();

        if (data > 250) {
            runCommand(data);
        } else {
            color[colorIndex] = data;
            colorIndex++;
            if (colorIndex == 3) {
                leds.setColor(zone, color[0], color[1], color[2]);
                colorIndex = 0;
                zone++;
            }
        }
    }
}

void runCommand(int cmd) {
    switch (cmd) {
        case 0xff:
            leds.updateLeds();
            colorIndex = 0;
            zone = 0;
    }
}
