#!/usr/bin/python


import MySQLdb
import logging
import logging.handlers
import time
import serial
import re

ser = serial.Serial('/dev/ttyACM0', 9600)
print "OK"
time.sleep(5)
db = MySQLdb.connect( '127.0.0.1' ,'garden','password','SensorInOut' )

def main():
    while True:
        data = readData()
        if len(data.keys()) < 1:
            print "NO DATA TO READ"
            continue

        writeToSensor( data )
        data = readSensor()
        writeToDatabase( data )
        time.sleep(2)
#enddef

def readData():
    sql = "select * from sensor_in"

    returnData = {}

    cursor = db.cursor()
    cursor.execute( sql )

    results = cursor.fetchall()

    for row in results:
        returnData[ row[0] ] = row[1]
        sql = "UPDATE sensor_in set time_read="+str(int(time.time()))+ " WHERE function='"+row[0]+"'"
        cursor.execute( sql )
        db.commit()

    return returnData
#enddef

def writeToSensor( data ):

    sendData = ''
    for key in data.keys():
        sendData = sendData + str(key)+'='+str(data[ key]) +';'


    sendData = sendData + "DONE;"
    print sendData
    ser.write(sendData)
#enddef

def readSensor():
    print "READING"
    data = ''
    line = ''
    while True:
        line =  ser.readline()

        data = data + line
        if re.search("DONE;", data):
            print data
            data = data[:-5]
            break
    #endwhile

    lines = []
    lines = data.split(";")

    returnData = {}
    for line in lines[:-1]:
        split = line.split("=")
        print str(split)
        returnData[ split[0]] = split[1]

    return returnData
#enddef

def writeToDatabase( data ):

    for key in data.keys():
        cursor = db.cursor()
        print "INSERT into sensor_out values('"\
                + key+"' , "\
                + str(data[ key]) +" , "\
                + str(int(time.time()))+" , 0 ) "\
                + "ON DUPLICATE KEY UPDATE "\
                + "value="+str(data[ key])
        cursor.execute("INSERT into sensor_out values('"\
                + key+"' , "\
                + str(data[ key]) +" , "\
                + str(int(time.time()))+" , 0 ) "\
                + "ON DUPLICATE KEY UPDATE "\
                + "value="+str(data[ key]+ " ,")\
                + "time_write=" + str(int(time.time()))
                )
        db.commit()
#enddef

main()








