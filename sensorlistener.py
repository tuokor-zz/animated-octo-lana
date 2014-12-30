from RF24 import * 

radio = RF24(RPI_V2_GPIO_P1_15, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ)

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]


radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)

radio.openReadingPipe(1, pipes[0])
radio.openReadingPipe(2, pipes[1])

radio.startListening()

radio.printDetails()

while True:
    pipe = radio.available();
    #print("pipe value:",pipe)
    if(pipe == True):
        done = False
        data = None
        len = radio.getDynamicPayloadSize()
        data = radio.read(len)
        print('Got data=', data, ' from pipe=', pipe)
