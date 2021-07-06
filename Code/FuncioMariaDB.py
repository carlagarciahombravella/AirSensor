#MariaDB_Function
import mysql.connector as mysql

def localDB_function(sDB, dvar):
        #mariadb connection
    db = mysql.connect(host='localhost', user="euss",passwd="rasppi",database=sDB)
    cursor = db.cursor() 
        
        #insert information
    sql_insert = "INSERT INTO AirQuality (Time, CO2, Formaldehyde, TVOC, PM25, PM10, Temperature, Humidity, IP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert,(dvar['Temps'], dvar['CO2'], dvar['Formaldehil'], dvar['TVOC'],dvar['PM25'], dvar['PM10'], dvar['Temperatura'], dvar['Humitat'], dvar['IP'])) 
        
        #se envia a la base de datos
    db.commit()  
            
    cursor.close()
    db.close()
        
def awsDB_function(sawsDB, dvar):
    awsdb = mysql.connect(host="airquality-id.ckvkvwrfnnhu.eu-west-2.rds.amazonaws.com", user="andreacosta",passwd="Barcelona98!",database=sawsDB)
    awsCursor = awsdb.cursor() 

            #insert information
    aws_insert = "INSERT INTO AirQuality (Time, CO2, Formaldehyde, TVOC, PM25, PM10, Temperature, Humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    awsCursor.execute(aws_insert,(dvar['Temps'], dvar['CO2'], dvar['Formaldehil'], dvar['TVOC'], dvar['PM25'], dvar['PM10'], dvar['Temperatura'], dvar['Humitat'])) 
            #se envia a la base de datos
    awsdb.commit()
    
    awsCursor.close()
    awsdb.close()
    