#!/usr/bin/python

import sys
import httplib
import json
import time
import logging
import logging.handlers
from SensorMapping import SensorMapping

logFormat  = logging.Formatter('%(asctime)s %(module)s:%(lineno)s %(levelname)s %(message)s' )
logHandler = logging.handlers.TimedRotatingFileHandler('Processor.log', when='h', interval=1, backupCount= 24 )

logger = logging.getLogger(__name__)
logHandler.setFormatter( logFormat )
logger.setLevel('DEBUG')
logger.addHandler( logHandler )

ITER_TIME = 1

masterHost    = sys.argv[1]
deviceIdent   = sys.argv[2]
dataTypeIdent = sys.argv[3]
responseIdent = sys.argv[4]

authData = {
    "auth" : {
                "username" : "348259135bdab48bf5ce36c3d8900379147dc1e92da08b5c4a26c9068ed5ecf4",
                "password" : "Ef@490515+"
            }
}
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def main():

    sensorMap = SensorMapping()
    #namespace = sensorMap.namespaceImport[ dataTypeIdent ]
    sensorObj = sensorMap.sensorObjMap[ dataTypeIdent ]( logger )

    error = False
    logger.info("Sensor: " + str(sensorObj) )
    while True:
        logger.info("Making Data Request")
        data = getData( sensorObj )
        logger.info("Processing Data")
        try:
            response = processData(sensorObj , data )
        except Exception as ex:
            logger.error(ex)
            error = True
            response = sensorObj.defaultResponse()

        logger.info("Sending Response")
        sendResponse( response )
        time.sleep( sensorObj.iterTime )
        if error:
            exit(1)
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getData(sensorObj):

    requestData = {
            'request' : {
                deviceIdent : {
                    dataTypeIdent : {
                        'points' : sensorObj.request_points,
                        'time'   : sensorObj.request_time
                    },
                }
            }
    }

    requestData['auth'] = authData['auth']

    logger.debug("Response request: " + str( requestData ) )

    conn = httplib.HTTPConnection( masterHost )
    conn.request('GET', '/GardenServer/processor/', json.dumps( requestData ) )
    resp = conn.getresponse()
    content = resp.read()

    logger.debug("Request repsponse Content: " + content )
    return json.loads( content )

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def processData( sensorObj , rawdata ):


    data = []
    for device in rawdata.keys():
        for datatype in rawdata[ device ].keys():
            for datapoint in rawdata[ device ][ datatype ].keys():
                data.append( rawdata[ device ][ datatype ][ datapoint ] )


    return sensorObj.process( data )

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def sendResponse( response ):
    requestData = {
        'response' : {
            responseIdent : response
        }
    }

    requestData['auth'] = authData['auth']

    logger.debug("Response request: " + str( requestData ) )

    conn = httplib.HTTPConnection( masterHost )
    conn.request('POST', '/GardenServer/processor/', json.dumps( requestData ) )
    resp = conn.getresponse()
    content = resp.read()
    logger.debug("Response response Content: " + content )

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################

main()
