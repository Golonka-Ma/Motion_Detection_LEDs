#include <FastLED.h>

#define LED_PIN 12
#define NUM_LEDS 12

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    fill_solid(leds, NUM_LEDS, CRGB::Black);

    int start = 0;
    int end = data.indexOf(',');
    while (end != -1) {
      String ledData = data.substring(start, end);
      int ledIndex = ledData.toInt();
      char color = ledData.charAt(ledData.length() - 1);

      if (ledIndex >= 0 && ledIndex < NUM_LEDS) {
        switch (color) {
          case 'W':
            leds[ledIndex] = CRGB::White;
            break;
          case 'B':
            leds[ledIndex] = CRGB::Blue;
            break;
          case 'G':
            leds[ledIndex] = CRGB::Green;
            break;
        }
      }

      start = end + 1;
      end = data.indexOf(',', start);
    }

    FastLED.show();
  }
}
