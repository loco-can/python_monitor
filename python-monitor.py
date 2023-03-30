#!/usr/bin/python3

# Importing Libraries
import os
import serial
import time
import serial.tools.list_ports



def connect():

    USBport = False;
    USBname = False;

    ports = serial.tools.list_ports.comports()

    if (os.name == 'posix'):
        os_filter = "FT232"
    else:
        os_filter = "USB"

    # get USB ports with FT232 description
    for port, desc, hwid in sorted(ports):

        print(port, ' ', desc)

        if desc.find(os_filter) != -1:

            USBport = port
            USBname = desc
            break


    # connect to serial adapter
    if USBport != False:

        print("connected to ", USBport, USBname)
        return serial.Serial(port=USBport, baudrate=115200, timeout=.2)

    else:
        print("no active FT232 found");
        # exit()
        return False


def checksum(data):

    sum = 0

    for v in data:
        sum ^= v

    return sum


# read message
# def write_read(x):

#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data

print(os.name)

arduino = False

message = {
    "id": 0,
    "uuid": 0,
    "size": 0,
    "data": []
}


# main loop
try:
    while True:

        # num = input("Enter a number: ") # Taking input from user
        # value = write_read(num)
        # print(value) # printing the value

        if arduino != False:

            try:
                value = arduino.read(18);

                if len(value) > 0:

                    # convert bytes to list
                    bytelist = list(value)

                    # remove checksum from message
                    cs = bytelist.pop()

                    # display bytes
                    # for i in bytelist:
                    #     print(hex(i), end=' ')


                    # test message start and chesum
                    if bytelist[0] == 0xFF and bytelist[1] == 0xFF and checksum(bytelist) == cs:

                        message["size"] = hex(bytelist[2])
                        message["id"] = hex((bytelist[3] << 24) | (bytelist[4] << 16) | (bytelist[5] << 8) | bytelist[6])
                        message["uuid"] = hex((bytelist[7] << 8) | bytelist[8])

                        message["data"] = []
                        
                        for i in range(bytelist[2]):
                            message["data"].append(hex(bytelist[9 + i]))

                        print(message)



            except serial.serialutil.SerialException:

                arduino = False



        else:
            arduino = connect();

            time.sleep(1)


except KeyboardInterrupt:

    if arduino != False:
        arduino.close()

    print("")
    exit()