#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile

RH_ASK driver;

void setup()
{
    Serial.begin(9600);  // Debugging only
    if (!driver.init())
         Serial.println("init failed");
}

void loop()
{
    // Set buffer to size of expected message [Sensors message [40] + , [1] + length of string[2] = 43]
    uint8_t buf[43];
    uint8_t buflen =  sizeof(buf); 
    if (driver.recv(buf, &buflen)) // Non-blocking
    {
      int i;
      //Printing message on serial monitor     
      Serial.println((char*)buf);         
    }
}