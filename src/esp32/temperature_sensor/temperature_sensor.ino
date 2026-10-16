#include <OneWire.h>
#include <DallasTemperature.h>

#define SENSOR_PIN 4
#define AMBIENT_TEMP_C 22.0

OneWire oneWire(SENSOR_PIN);
DallasTemperature sensors(&oneWire);

int sensorCount = 0;

void setup() {
    Serial.begin(115200);
    delay(1000);
    sensors.begin();
    sensorCount = sensors.getDeviceCount();
    Serial.print("DS18B20 sensors found: ");
    Serial.println(sensorCount);
}

void loop() {
    sensors.requestTemperatures();
    delay(750);

    float temp1 = (sensorCount >= 1) ? sensors.getTempCByIndex(0) : -127.0;
    float temp2 = (sensorCount >= 2) ? sensors.getTempCByIndex(1) : -127.0;

    if (temp1 == -127.0) {
        Serial.println("Error: No sensors detected");
    } else if (temp2 == -127.0) {
        Serial.print("T1:");
        Serial.print(temp1, 2);
        Serial.println(",T2:N/A,DS:N/A,DA1:N/A,DA2:N/A");
    } else {
        float delta_string = temp1 - temp2;
        float delta_ambient1 = temp1 - AMBIENT_TEMP_C;
        float delta_ambient2 = temp2 - AMBIENT_TEMP_C;

        Serial.print("T1:");
        Serial.print(temp1, 2);
        Serial.print(",T2:");
        Serial.print(temp2, 2);
        Serial.print(",DS:");
        Serial.print(delta_string, 2);
        Serial.print(",DA1:");
        Serial.print(delta_ambient1, 2);
        Serial.print(",DA2:");
        Serial.println(delta_ambient2, 2);
    }

    delay(500);
}