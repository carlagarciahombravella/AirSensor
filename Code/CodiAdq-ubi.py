#mesures mediambiental
import time
from datetime import datetime

from threading import Thread
import socket

import mysql.connector as mysql

import serial
import RPi.GPIO as GPIO

from FuncionsSensor import reading_pos, sensorw_function,sensorb_function
from FuncioMariaDB import localDB_function, awsDB_function
from FuncionsUbidots import build_payload, post_request, get_var

GPIO.setwarnings(False)

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

medidas = {"Temps":0,"CO2":0,"Formaldehil":0,"TVOC":0,"PM25":0,"PM10":0,"Temperatura":0,"Humitat":0, "IP":0}
meskey_list = list(medidas)
mesdata_list = list(medidas.values())

data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
suma = 0


def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address


def sensor_reading():  
    i=0
    a=ser.read(1)
    data[i]=ord(a)
    b=ser.read(1)
    data[i+1]=ord(b)
 

    if (a==b'<' and b==b'\x02'):
            #Temps de la mostra: Data i hora
        Tiempo = datetime.now()
        m_sTiempo = Tiempo.strftime("%d/%m/%Y %H:%M:%S")
        medidas.update({'Temps':m_sTiempo})
        
        i=1
        B3=ord(ser.read(1)) # eCO2 high
        data[i]=B3
        ser.write(data[i])
        B4=ord(ser.read(1)) # eCO2 low
        CO2=(B3*256+B4)*1.1
        CO2 = round (CO2,2)
        medidas.update({'CO2':CO2})
        
        i=i+1
        data[i]=B4
        ser.write(data[i])          
        B5=ord(ser.read(1)) # eCH2O high
        i=i+1
        data[i]=B5
        ser.write(data[i])          
        B6=ord(ser.read(1)) # eCH2O low
        formaldehil=B5*256+B6
        medidas.update({'Formaldehil':formaldehil})        
        
        i=i+1
        data[i]=B6
        ser.write(data[i])          
        B7=ord(ser.read(1)) # TVOC high
        i=i+1
        data[i]=B7
        ser.write(data[i])         
        B8=ord(ser.read(1)) # TVOC low
        TVOC=(B7*256+B8)*0.9
        medidas.update({'TVOC':TVOC})
        
        i=i+1
        data[i]=B8
        ser.write(data[i])          
        B9=ord(ser.read(1)) # PM25 high
        i=i+1
        data[i]=B9
        ser.write(data[i])          
        B10=ord(ser.read(1))# PM25 low
        PM25=(B9*256+B10)*0.64
        medidas.update({'PM25':PM25})
        
        i=i+1
        data[i]=B10
        ser.write(data[i])          
        B11=ord(ser.read(1))#PM10 high
        i=i+1
        data[i]=B11
        ser.write(data[i])          
        B12=ord(ser.read(1))#PM10 low
        PM10=B11*256+B12
        medidas.update({'PM10':PM10})
        
        i=i+1
        data[i]=B12
        ser.write(data[i])          
        B13=ord(ser.read(1))#temp int
        i=i+1
        data[i]=B13
        ser.write(data[i])          
        B14=ord(ser.read(1))#temp decimal
        temperatura=(B13+B14*0.1)*0.97
        temperatura = round (temperatura,2)
        medidas.update({'Temperatura':temperatura})
        
        i=i+1
        data[i]=B14
        ser.write(data[i])          
        B15=ord(ser.read(1))#humidity int
        i=i+1
        data[i]=B15
        ser.write(data[i])          
        B16=ord(ser.read(1))#humidity decimal
        humitat=(B15+B16*0.1)*1.04
        humitat = round (humitat,2)
        medidas.update({'Humitat':humitat})
        
        i=i+1
        data[i]=B16
        ser.write(data[i])          
        check=B3+B4+B5+B6+B7+B8+B9+B10+B11+B12+B13+B14+B15+B16
        B18=hex(check)
        B17=ser.read(1)#checksum
        ser.write(B17)         
        i=1
        
        IP= get_ip_address()
        medidas.update({'IP':IP})
        
        print(medidas) # to check if everything is ok
          
        # loop to iterate for values
        awsDB_function("airquality",medidas)
        #localDB_function("Datos_CarlaAWS",medidas)
                
                
        #Send data to UBIDOTS

        VAR_LABELS = ['CO2','Formaldehyde','TVOC','PM2.5','PM10','Temperature','Humidity']
        
        payload = build_payload(medidas,VAR_LABELS)
        print("[INFO] Attemping to send data")
        post_request(payload,TOKEN,DEVICE_LABEL)
        print("[INFO] finished")
        

# Ubidots related variables
TOKEN = "BBFF-i2wdsPU4rutDmyLyY2l0uJce7o6J6s"  # Token of ubidots account
DEVICE_LABEL = "airrubotmecanum"  # Device label
VARIABLE = "switch"  # Variable label from which we want to extract data: switch takes 1 when on, 0 when off.
    
try:
    while True:
        if get_var(DEVICE_LABEL, VARIABLE, TOKEN) == 1: # if switch in ubidots is turned on (boolean value 1)
            t = Thread(target=sensor_reading) # Create thread
            t.start() # Start thread
            time.sleep(5)
except KeyboardInterrupt:
   GPIO.cleanup()


        
        
