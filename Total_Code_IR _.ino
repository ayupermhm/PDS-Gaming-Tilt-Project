#include <Wire.h>
#include "MAX30105.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <RH_ASK.h>
#include <SPI.h> 
#include <string.h>


Adafruit_MPU6050 mpu;
RH_ASK rf_driver;
MAX30105 particleSensor;

//Initialize GSR sensor
const int GSR = 9;

int sensorValue = 0;

int gsr_average = 0;
  
void setup() {
  Serial.begin(9600);

  // Initialize MAX30102  Pulse sensor
  if (particleSensor.begin() == false) {
    Serial.println("MAX30102 was not found. Please check wiring/power.");
    while (1);
  }
  {
  //Initialize MPU6050 Accelerometer sensor
  while (!Serial) {
    delay(10);

  }}
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(1);
    }
    {  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
      mpu.setGyroRange(MPU6050_RANGE_250_DEG);
      mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
      Serial.println("");
      delay(1);
    }
  }
  {
    // Initialize ASK Object [Transmitter]
    rf_driver.init();
}
 
    
 
  }

void loop() {
  {
  {
  //MAX30102 Pulse sensor

 {

  long sum = 0;

  for (int i = 0; i < 10; i++)

 {

  long sum = 0;

  for (int i = 0; i < 10; i++)

  {//GSR Sensor

    sensorValue = analogRead(GSR);

    sum += sensorValue;

    

  }

  gsr_average = sum / 10;


}
{

  /* MPU6050 sensor */
  Serial.begin(115200);//Changing baud for accelerometer 
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  //Printing all the sensor outputs
  Serial.print(particleSensor.getRed());
  Serial.print(',');
  Serial.print(particleSensor.getIR());
  Serial.print(',');
  Serial.print(gsr_average);
  Serial.print(',');
  Serial.print(a.acceleration.x);
  Serial.print(',');
  Serial.print(a.acceleration.y);
  Serial.print(',');
  Serial.print(a.acceleration.z);
  Serial.print(',');
  Serial.print(g.gyro.x);
  Serial.print(',');
  Serial.print(g.gyro.y);
  Serial.print(',');
  Serial.print(g.gyro.z);
  Serial.println();
 






  delay(1);
  Serial.begin(9600);//changing it backfor rest of script
  {//Transmission 
    String msg_str = String(particleSensor.getRed()) +',' + String(particleSensor.getIR()) + ',' + String(gsr_average) + ',' + String(a.acceleration.x) + ','+ String(a.acceleration.y) + ','+ String(a.acceleration.z)+ ','+ String(g.gyro.x)+ ','+ String(g.gyro.y)+ ','+ String(g.gyro.z);
    const char *msg = msg_str.c_str();
   //Concatonate all values into one big string so it can be sent like that
    //Serial.print(msg_str);
    
    rf_driver.send((uint8_t *)msg, strlen(msg));//Send sensor value string and length of that string 


    
    rf_driver.waitPacketSent();
    delay(1);
}
}
}
}}}


