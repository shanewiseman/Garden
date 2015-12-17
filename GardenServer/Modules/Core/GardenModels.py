from GardenServer.models import Data , Device , Response , ProcessorInstance , DataType
from GardenServer.Modules.Helpers import Authentication
import logging
import time

logger = logging.getLogger(__name__)

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def setData( deviceObj, dataTypeObj, data ):
    logger.debug("Setting Data")
    obj = Data(
        identifier = Authentication.generateIdentifier(
            [ deviceObj.identifier , dataTypeObj.identifier, data, time.time() ]
        ),
        device = deviceObj,
        datatype = dataTypeObj,
        value = data
    )

    obj.save()
    return obj

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getData( **kwargs ):
    logger.debug("Getting Data")
    try:
        return Data.objects.get( **kwargs )
    except Data.DoesNotExist:
        logger.warn("Data Does Not Exist: " + str(kwargs) )
        return None
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getDataRange( range , **kwargs ):
    logger.debug("Getting Data")
    try:
        return Data.objects.filter( **kwargs ).order_by('created').reverse()[ :range]
    except Data.DoesNotExist:
        logger.warn("Data Does Not Exist: " + str(kwargs) )
        return None
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def setResponse( deviceObj , dataTypeObj , data ):

    logger.info("Creating Response Object")
    obj = Response(
        identifier = Authentication.generateIdentifier(
            [ deviceObj.identifier , dataTypeObj.identifier , time.time() ]
        ),
        device = deviceObj,
        datatype = dataTypeObj,
        value = data
    )

    obj.save()

    return obj

#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getResponse( **kwargs ):
    logger.debug("Getting Response")
    try:
        return Response.objects.get( **kwargs )
    except Response.DoesNotExist:
        logger.warn("Response Does Not Exist: " + str(kwargs) )
        return None
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getResponseList( **kwargs ):
    logger.debug("Getting Response List")
    return Response.objects.filter( **kwargs )
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getDevice( **kwargs ):

    logger.debug("Getting Device")
    try:
        return Device.objects.get( **kwargs )
    except Device.DoesNotExist:
        logger.warn("Device Does Not Exist: " + str(kwargs) )
        return None
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getDeviceList( **kwargs ):
    logger.debug("Getting Device List")
    return Device.objects.filter( **kwargs )
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def getDataType( **kwargs ):
    logger.debug("Getting DataType")
    try:
        return DataType.objects.get( **kwargs )
    except DataType.DoesNotExist:
        logger.warn("DataType Does Not Exist: " + str(kwargs) )
        return None
#enddef

################################################################################
#------------------------------------------------------------------------------#
################################################################################





