import serial
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
i = 0

def sensorw_function(i):
    sHigh=ord(ser.read(1)) #High byte
    data[i]=sHigh
    sLow=ord(ser.read(1)) #Low byte
    data[i+1]=sLow
    iwVar=sHigh*256+sLow
    return iwVar

def reading_pos(i):
    
    sHigh=ord(ser.read(1)) #High byte
    data[i]=sHigh
    sLow=ord(ser.read(1)) #Low byte
    data[i+1]=sLow
    
    if (i < 12):
        iwVar=(sHigh*256) + sLow
    else:
        iwVar = sHigh + (sLow/10)
    
    return iwVar          

def sensorb_function(i):
    sInt=ord(ser.read(1))#Integer value
    data[i]=sInt
    sDec=ord(ser.read(1))#Rest value
    data[i+1]=sDec
    
    ibVar = (sInt)+ (sDec/10)
    
    return ibVar

def sensorCheck_function(*data):
    suma = 0
    for val in range(0, len(data)):
        suma = suma + data[val]
    check = ser.read(1)#checksum
    return suma, check
   


    