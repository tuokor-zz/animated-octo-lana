#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "printf.h"

RF24 radio(7,8);

const uint64_t writepipe = 0xF0F0F0F0E1LL;

void setup() {
  Serial.begin(57600);
  printf_begin();
  printf("\nSensor node starting");
  
  radio.begin();
  radio.enableDynamicPayloads();
  radio.setRetries(5,15);
  
  radio.openWritingPipe(writepipe);
  radio.printDetails();
}

void loop() {
  printf("sending data\n");
  char data[] = "hello from node";
  radio.write(data, sizeof(data));
  delay(2000);
}
