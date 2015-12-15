from GardenServer.Modules.Core    import GardenModels
import logging
import json
import ast
import re
import time

logger = logging.getLogger(__name__)

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def request( userObj , data ):
    logger.info("Screening Request")

    for deviceKey in data.keys():

        deviceObj = GardenModels.getDevice( identifier = deviceKey)

        if deviceObj == None:
            return 0

        logger.debug( "DeviceObj: " + deviceObj.identifier )

        # making sure device belongs to the user
        if deviceObj.user.identifier != userObj.identifier:
            logger.error( "Device Does Not Belong To User: " + deviceKey )
            return 0

        for dataTypeKey in data[ deviceKey ].keys():

            dataTypeObj = GardenModels.getDataType( identifier = dataTypeKey )

            if dataTypeObj == None:
                return 0

            logger.debug( "DataTypeObj: " + dataTypeObj.identifier )

            __prepareResponseObject( deviceObj , dataTypeObj )
        #endfor
    #endfor
    return __storeData( data )
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def response( userObj ):

    logger.info( "Response for " + str( userObj.identifier ) )

    deviceObjs = GardenModels.getDeviceList( user_id = userObj.identifier )

    logger.info( "Process Response for " + str( len(deviceObjs) ) + " Devices" )

    if len(deviceObjs) < 1:
        return 0

    returnData = {}
    for deviceObj in deviceObjs:

        logger.debug( "Working on " + deviceObj.identifier )
        returnData[ deviceObj.identifier ] = {}
        responseObjs = GardenModels.getResponseList( device =  deviceObj )

        for responseObj in responseObjs:
            logger.debug( "Response Object: " + str( responseObj.identifier ) )
            returnData[ responseObj.device.identifier ][ responseObj.datatype.identifier ] = \
                    responseObj.value

        #endfor
        returnDataString = __formatResponse( returnData )
        logger.debug("Response: " + returnDataString )

    return returnDataString
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def __storeData( data ):
    logger.info("Storing Data For Request")
    for deviceKey in data.keys():

        logger.debug( "Processing Device: " + deviceKey )
        deviceObj = GardenModels.getDevice( identifier = deviceKey)

        # device may have different data types
        for dataTypeKey in data[ deviceKey ].keys():

            logger.debug( "Processing DataType: " + dataTypeKey )
            dataTypeObj = GardenModels.getDataType( identifier = dataTypeKey )

            logger.info( "Converting Data" )
            storeData = json.dumps( data[ deviceKey ][ dataTypeKey ] )
            logger.debug( storeData )

            logger.info( "Creating Data Objects -> Device: " + deviceKey + " Type: " + dataTypeKey )
            GardenModels.setData( deviceObj , dataTypeObj , storeData )

        #endfor
        logger.info( "Done with Device" )
    #endfor

    return 1
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def __formatResponse( returnData ):

    response = json.dumps( returnData )
    response = re.sub(r'\\','', response)
    response = re.sub(r'"\{','{', response)
    response = re.sub(r'\}"','}', response)
    response = re.sub(r'"\[','[', response)
    response = re.sub(r'\]"',']', response)

    return response

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def __prepareResponseObject( deviceObj , dataTypeObj ):

    logger.debug("PreparingResponseObject")
    if None == GardenModels.getResponse( device = deviceObj , datatype = dataTypeObj ):
        GardenModels.setResponse( deviceObj, dataTypeObj, "" )

        #NOTE need to instantiate processor

#enddef

