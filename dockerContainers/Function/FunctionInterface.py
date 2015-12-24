#!/usr/bin/python

import MySQLdb
import json
import httplib
import time
import logging
import logging.handlers
import sys

from FunctionMapping import FunctionMapping

authData = {
    "auth" : {
                "username" : "348259135bdab48bf5ce36c3d8900379147dc1e92da08b5c4a26c9068ed5ecf4",
                "password" : "Ef@490515+"
            }
}


db = None
sensorHost = sys.argv[1]
masterHost = sys.argv[2]
function   = sys.argv[3]


logFormat  = logging.Formatter('%(asctime)s %(module)s:%(lineno)s %(levelname)s %(message)s' )
logHandler = logging.handlers.TimedRotatingFileHandler('Function.log', when='h', interval=1, backupCount= 24 )

logger = logging.getLogger(__name__)
logHandler.setFormatter( logFormat )
logger.setLevel('INFO')
logger.addHandler( logHandler )


def main():

    logger.info( "SensorHost: " + sensorHost )
    logger.info( "MasterHost: " + masterHost )
    logger.info( "Function  : " + function )


    functionMap = FunctionMapping()
    functionObj = functionMap.functionObjMap[ function ]( logger )

    logger.info( str( functionObj ) )

    logger.info("Setting Up DB")
    setupDB(functionObj)

    while True:
        try:
            logger.info("Get Sensor Data" )
            data = getSensorData( functionObj )

            if not data:
                logger.warn("No SensorData")
                continue
            else:
                logger.info("Processing Sensor Data")
                data = processSensorData( functionObj , data )

            logger.info("Sending Data To Server")
            sendServerData( data )

            logger.info("Getting Server Data")
            data = getServerData( functionObj )

            if not data:
                logger.warn("No Server Data")
                data = functionObj.defaultReturn()
            else:
                logger.info("Processing Server Data")
                data = processServerData( functionObj , data )

            logger.info("Setting Sensor Data")
            setSensorData( functionObj, data)

            time.sleep(1)
        except Exception as ex:
            logger.error(ex)
            data = functionObj.defaultReturn()
            setSensorData( functionObj, data)
            exit(1)
#endef
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def setupDB( functionObj ):
    global db

    db = MySQLdb.connect( sensorHost ,'garden','password','SensorInOut' )
    cursor = db.cursor()

    sql = "select * from sensor_in where function='" + functionObj.functionKey + "' LIMIT 1"
    results = __executeRetrieveQuery( sql )

    if( len( results ) < 1 ):

        logger.warn("Creating sensor_in row")

        sql = "INSERT into sensor_in values('" +functionObj.functionKey+ "'," + str(functionObj.initInVal) +\
                ", " +str(int(time.time()))+" , 0 )"
        __executeInsertQuery( sql )

    else:

        logger.warn("Updating Existing sensor_in row")

        sql = "UPDATE sensor_in set value=" + str(functionObj.initInVal) + \
            " time_write="+str(int(time.time()))+" where function='" + functionObj.functionKey + "'"

        __executeInsertQuery( sql )


################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getSensorData( functionObj ):

    returnData = {}

    for datatype in functionObj.sensorIdent.keys():
        logger.debug( datatype )
        for deviceid in functionObj.sensorIdent[ datatype ]:

            logger.debug( deviceid )

            sql = "select value from sensor_out where identifier='"+ deviceid +"'"
            results = __executeRetrieveQuery( sql )

            if len( results ) < 1:
                logger.warn("No Results")
                False

            sql = "update sensor_out set time_read="+str(int(time.time()))+" where identifier='" +deviceid+"'"
            __executeInsertQuery( sql )
            #should only be one result but anticipating
            for row in results:

                if deviceid not in returnData:
                    returnData[ deviceid ] = {}

                returnData[ deviceid ][ datatype ] = row[0]
            #endofor
        #endfor
    #endfor
    logger.debug( returnData )
    return returnData

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def processSensorData( functionObj ,  data ):

    returnData = functionObj.processSensorData( data )

    logger.debug( returnData )

    return returnData
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def sendServerData( data ):
    requestData = {
        'data' : data,
        'auth' : authData['auth'],
    }

    logger.debug( str( requestData ) )

    conn = httplib.HTTPConnection( masterHost )
    conn.request('POST', '/GardenServer/data/', json.dumps( requestData ) )
    resp = conn.getresponse()
    content = resp.read()
    logger.debug("Response response Content: " + content )

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getServerData( functionObj ):
    requestData = {
        'data' : {},
        'auth' : authData['auth'],
    }


    for datatype in functionObj.sensorIdent.keys():
        for device in functionObj.sensorIdent[ datatype ]:
            if device not in requestData[ 'data' ]:
                requestData[ 'data' ][ device ] = []

            requestData[ 'data' ][ device ].append( datatype )

    logger.debug( str( requestData ) )

    conn = httplib.HTTPConnection( masterHost )
    conn.request('GET', '/GardenServer/data/', json.dumps( requestData ) )
    resp = conn.getresponse()
    content = resp.read()
    logger.debug("Response response Content: " + content )

    try:
        response = json.loads( content )
    except:
        return False

    return response

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def processServerData( functionObj , data ):

    returnData = functionObj.processServerData( data )

    logger.debug( returnData )

    return returnData

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def setSensorData( functionObj , data ):

    for key in data.keys():
        sql = 'UPDATE sensor_in SET value='+str( data[ key ] )+' , time_write='+str(int(time.time()))+\
                ' WHERE function="'+ functionObj.functionKey +'"'

        __executeInsertQuery( sql )


################################################################################
#------------------------------------------------------------------------------#
################################################################################

def __executeRetrieveQuery( sql ):

    logger.debug("RetrieveQuery: " + sql )

    cursor = db.cursor()

    cursor.execute( sql )
    results = cursor.fetchall()

    logger.debug( str( results ) )

    return results
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def __executeInsertQuery( sql ):

    logger.debug("InsertQuery: " + sql )

    cursor = db.cursor()

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        logger.error("Insert Failed!")
        db.rollback()
        return False

    return True
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################


main()
