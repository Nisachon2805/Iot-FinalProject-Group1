#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_SHT4x.h>
#include <WiFi.h>
#include <time.h>
#include <esp_task_wdt.h>
#include <WiFiUdp.h>
#include <freertos/queue.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <PubSubClient.h>
#include <stdlib.h>
#include <Adafruit_NeoPixel.h>

// WiFi settings
#define WIFI_SSID "My Heart"
#define WIFI_PASSWORD "heartkung0388"

WiFiClient espClient;

// MQTT settings for Raspberry Pi
const char* mqtt_server = "192.168.154.229";
const int mqtt_port = 1883;
const char* mqtt_topic_publish = "@msg/data";
const char* mqtt_topic_subscribe = "@msg/cb";

PubSubClient client(espClient);

// Sensors settings
Adafruit_BMP280 bmp;
Adafruit_SHT4x sht4;

Adafruit_Sensor *BMP280_temp = bmp.getTemperatureSensor();
Adafruit_Sensor *BMP280_pressure = bmp.getPressureSensor();

struct SensorData {
  float temperature;
  float humidity;
  float pressure;
};

QueueHandle_t sensorDataQueue;

// RGB LED Settings
#define PIN 18

Adafruit_NeoPixel pixels(1, PIN, NEO_GRB + NEO_KHZ800);

// Declare variables
unsigned long previousTime = millis();
const int intervalTime = 59000;
int colorIndex = 0;

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void connectToMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
  client.subscribe(mqtt_topic_subscribe);
}

void getData(void *pvParameters) {
  SensorData data;
  for(;;){
    sensors_event_t sht4_humidity, sht4_temp,bmp_temp, bmp_pressure;

    sht4.getEvent(&sht4_humidity, &sht4_temp);
    BMP280_temp->getEvent(&bmp_temp);
    BMP280_pressure->getEvent(&bmp_pressure);
    
    data.temperature = sht4_temp.temperature;
    data.humidity = sht4_humidity.relative_humidity;
    data.pressure = bmp_pressure.pressure;

    xQueueSend(sensorDataQueue, &data, ( TickType_t ) 10  );
    
    vTaskDelay(1000);
  }
}

void PublishData(void *pvParameters) {
  char topic[100];
  SensorData data;
  for(;;) {
    if (xQueueReceive(sensorDataQueue, &data, portMAX_DELAY) && (millis() - previousTime >= intervalTime) ) {
        if (!client.connected()) {
          connectToMQTT();
      }
      
      float temperature = data.temperature; // Example float value
      float humidity = data.humidity;
      float pressure = data.pressure;

      char buffer1[21]; // Buffer to store the string
      char buffer2[21];
      char buffer3[21];

      // Convert float to string
      dtostrf(temperature, 6, 2, buffer1); // Format: dtostrf(floatVar, width, precision, charBuffer)
      dtostrf(humidity, 6, 2, buffer2);
      dtostrf(pressure, 6, 2, buffer3);

      // Convert char arrays to String objects
      String strTemp(buffer1);
      String strHumid(buffer2);
      String strPressure(buffer3);

      // Construct the JSON string
      String jsonData = "{\"data\": { \"temp\" : " + strTemp + ", \"humid\": " + strHumid + ", \"pressure\": " + strPressure + "} }";
      
      client.publish(mqtt_topic_publish, jsonData.c_str());
      Serial.println("Data published to MQTT");
      
      previousTime = millis();
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.println("Message arrived.");
  Serial.print("Message : ");
  for(int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();

  pixels.setPixelColor(0, color(colorIndex++));
  pixels.show();
  if (colorIndex == 7) {
    colorIndex = 0;
  }
}

// RGB LED function to return color based on input index
uint32_t color(byte index) {
  if (index == 0) return pixels.Color(128, 0, 128); // Purple
  else if (index == 1) return pixels.Color(135, 206, 235); // Sky Blue
  else if (index == 2) return pixels.Color(0, 0, 255); // Blue
  else if (index == 3) return pixels.Color(0, 255, 0); // Green
  else if (index == 4) return pixels.Color(255, 255, 0); // Yellow
  else if (index == 5) return pixels.Color(255, 165, 0); // Orange
  else if (index == 6) return pixels.Color(255, 0, 0); // Red
  else return pixels.Color(0, 0, 0); // Off
}

void setup() {
  Serial.begin(115200);
  Wire.begin(41,40);

  connectToWiFi();

  // Check sensor 
  Serial.println("HTS221 sensor checking...");
  if (sht4.begin()) { 
    Serial.println("Found SHT4x sensor.");
  }
  else {
    Serial.println("Failed to initialize SHT4x sensor!");
  } 

  Serial.println("BMP280 sensor checking...");
  if (bmp.begin(0x76)) {
    Serial.println("Found BMP280 sensor.");
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                Adafruit_BMP280::SAMPLING_X2,
                Adafruit_BMP280::SAMPLING_X16,
                Adafruit_BMP280::FILTER_X16,
                Adafruit_BMP280::STANDBY_MS_500);
  } else {
    Serial.println("Failed to initialize BMP280 sensor!");
  }

  sensorDataQueue = xQueueCreate(10, sizeof(SensorData));

  // Set up MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  // Set up RGB LED
  pixels.setBrightness(50);
  pixels.begin();

  xTaskCreate(getData, "getData", 2048, NULL, 1, NULL);
  xTaskCreate(PublishData, "PublishData", 2048, NULL, 1, NULL);
}

void loop() {
  client.loop();
}