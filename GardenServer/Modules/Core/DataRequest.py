from GardenServer.Modules.Core    import GardenModels
from GardenServer.Modules.Helpers import DataFormat
from GardenServer.Modules.Core    import Processor
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
    logger.info("Screening DATA Request")

    for deviceKey in data.keys():

        deviceObj = GardenModels.getDevice( identifier = deviceKey)

        if deviceObj == None:
            return False

        logger.debug( "DeviceObj: " + deviceObj.identifier )

        # making sure device belongs to the user
        if deviceObj.user.identifier != userObj.identifier:
            logger.error( "Device Does Not Belong To User: " + deviceKey )
            return False

        for dataTypeKey in data[ deviceKey ].keys():

            dataTypeObj = GardenModels.getDataType( identifier = dataTypeKey )

            if dataTypeObj == None:
                return False

            logger.debug( "DataTypeObj: " + dataTypeObj.identifier )

            __prepareResponseObject( deviceObj , dataTypeObj )
        #endfor
    #endfor
    return __storeData( data )
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def response( userObj, data ):
    logger.info("Screening RESPONSE Request")

    for deviceKey in data.keys():

        deviceObj = GardenModels.getDevice( identifier = deviceKey)

        if deviceObj == None:
            return False

        logger.debug( "DeviceObj: " + deviceObj.identifier )

        # making sure device belongs to the user
        if deviceObj.user.identifier != userObj.identifier:
            logger.error( "Device Does Not Belong To User: " + deviceKey )
            return False

        for dataTypeKey in data[ deviceKey ]:

            dataTypeObj = GardenModels.getDataType( identifier = dataTypeKey )

            if dataTypeObj == None:
                return False

            logger.debug( "DataTypeObj: " + dataTypeObj.identifier )

        #endfor
    #endfor
    return __retrieveResponse( data )
#enddef
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def __retrieveResponse( data ):

    returnData = {}

    for deviceKey in data.keys():
        deviceObj = GardenModels.getDevice( identifier = deviceKey)

        logger.debug( "DeviceObj: " + deviceObj.identifier )

        for dataTypeKey in data[ deviceKey ]:

            dataTypeObj = GardenModels.getDataType( identifier = dataTypeKey )

            logger.debug( "DataTypeObj: " + dataTypeObj.identifier )

            returnData[ deviceObj.identifier ] = {}
            responseObj= GardenModels.getResponse( device =  deviceObj, datatype = dataTypeObj)
            if responseObj == None:
                return False

            logger.debug( "Response Object: " + str( responseObj.identifier ) )
            returnData[ responseObj.device.identifier ][ responseObj.datatype.identifier ] = \
                    responseObj.value

        #endfor
        returnDataString = DataFormat.formatJsonResponse( returnData )
        logger.debug("Response: " + returnDataString )

    return returnDataString
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
def __prepareResponseObject( deviceObj , dataTypeObj ):

    logger.debug("PreparingResponseObject")
    if None == GardenModels.getResponse( device = deviceObj , datatype = dataTypeObj ):
        responseObj = GardenModels.setResponse( deviceObj, dataTypeObj, "" )
        Processor.createProcessor( dataTypeObj , deviceObj , responseObj )


#enddef

