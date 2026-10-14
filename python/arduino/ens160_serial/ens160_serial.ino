#include <Arduino.h>
#include <ScioSense_ENS16x.h>
#include <Wire.h>

// Hardware configuration recovered from the ENS160_rUBot project.
constexpr uint8_t ENS160_ADDRESS = 0x52;
constexpr uint8_t TCA9548A_ADDRESS = 0x70;
constexpr uint8_t SENSOR_ENABLE_PIN = A6;
constexpr uint8_t SENSOR_COUNT = 6;
constexpr uint8_t TCA_CHANNELS[SENSOR_COUNT] = {0, 1, 2, 3, 4, 5};
constexpr unsigned long SERIAL_BAUD = 9600;
constexpr unsigned long SAMPLE_INTERVAL_MS = 1000;

ENS160 sensors[SENSOR_COUNT];
bool sensor_ready[SENSOR_COUNT] = {false};
unsigned long last_sample_ms = 0;

bool select_channel(uint8_t channel) {
  if (channel > 7) {
    return false;
  }
  Wire.beginTransmission(TCA9548A_ADDRESS);
  Wire.write(1U << channel);
  return Wire.endTransmission() == 0;
}

void initialize_sensors() {
  for (uint8_t index = 0; index < SENSOR_COUNT; ++index) {
    const uint8_t channel = TCA_CHANNELS[index];
    Serial.print(F("Init CH"));
    Serial.print(channel);

    if (!select_channel(channel)) {
      Serial.println(F(" -> multiplexer error"));
      continue;
    }

    sensors[index].begin(&Wire, ENS160_ADDRESS);
    sensor_ready[index] = sensors[index].init();
    Serial.println(sensor_ready[index] ? F(" -> OK") : F(" -> sensor error"));
    delay(50);
  }
}

void publish_reading(uint8_t index) {
  const uint8_t channel = TCA_CHANNELS[index];
  if (!sensor_ready[index] || !select_channel(channel)) {
    return;
  }
  if (sensors[index].update() != RESULT_OK || !sensors[index].hasNewData()) {
    return;
  }

  Serial.print(millis());
  Serial.print(F(",CH"));
  Serial.print(channel);
  Serial.print(F(",eCO2="));
  Serial.print(sensors[index].getEco2());
  Serial.print(F(",TVOC="));
  Serial.print(sensors[index].getTvoc());
  Serial.print(F(",AQI="));
  Serial.print(sensors[index].getAirQualityIndex_UBA());
  Serial.print(F(",R0="));
  Serial.print(sensors[index].getRs0());
  Serial.print(F(",R1="));
  Serial.print(sensors[index].getRs1());
  Serial.print(F(",R2="));
  Serial.print(sensors[index].getRs2());
  Serial.print(F(",R3="));
  Serial.println(sensors[index].getRs3());
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(SENSOR_ENABLE_PIN, OUTPUT);
  digitalWrite(SENSOR_ENABLE_PIN, HIGH);
  delay(1000);
  Wire.begin();
  initialize_sensors();
  last_sample_ms = millis();
}

void loop() {
  const unsigned long now = millis();
  if (now - last_sample_ms < SAMPLE_INTERVAL_MS) {
    return;
  }
  last_sample_ms = now;
  for (uint8_t index = 0; index < SENSOR_COUNT; ++index) {
    publish_reading(index);
  }
}
