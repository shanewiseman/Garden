from GardenServer.models import *
import logging

logger = logging.getLogger(__name__)

def store( userObj , data ):

    for deviceKey in data.keys():

        logger.info( "Processing Device: " + deviceKey )
        try:
            deviceObj = Device.objects.get( indentifier = deviceKey)
            logger.debug( "DeviceObj: " + deviceObj.identifier )
        except model.DoesNotExist:
            logger.error( "Device Does Not Exist: " + deviceKey )
            return 0

        # making sure device belongs to the user
        if deviceObj.user.id != userObj.id:
            logger.error( "Device Does Not Belong To User: " + deviceKey )
            return 0

        # device may have different data types
        for dataTypeKey in data.deviceKey.keys():

            logger.debug( "Processing DataType: " + dataTypeKey )
            try:
                dataTypeObj = DataType( identifier = dataTypeKey )
                logger.debug( "DataType: " + dataTypeObj.identifier )
            except model.DoesNotExist:
                logger.error( "DataType Does Not Exist: " + dataTypeKey )
                return 0

            prepareReponseObject( deviceObj , dataTypeObj )

            logger.debug( "Converting Data" )
            storeData = json.dumps( data.device.datatype )
            logger.debug( storeData )

            logger.info( "Creating Data Objects -> Device: " + deviceKey + " Type: " + dataTypeKey )
            Data( device = device , datatype = dataType , value = storeData ).save()

        #endfor
        logger.info( "Done with Device" )
    #endfor

    return
#enddef

def response( userObj ):

    logger.info( "Reponse for " + userObj.id )

    devices = Devices.objects.filter( user_id = userObj.id )

    logger.info( "Process Response for " + len(devices) + " Devices" )

    if len(devices) < 1:
        return 0

    responses = {}
    for device in devices:

        logger.debug( "Working on " + device.identifier )
        responses[ device.identifier ] = {}
        resonseObjs= Response.objects.filter( device =  device )

        for responseObj in responseObjs:
            logger.debug( "Response Object: " + responseObj.id )
            responses[ responseObj.device.identifier ][ responseObj.datatype.identifier ] = \
                    responseObj.value

        #endfor
    return responses
#enddef

def prepareResponseObject( deviceObj , dataTypeObj ):

    logger.debug("PreparingResponseObject")
    try:
        Response.objects.get( device = deviceObj , datatype = dataTypeObj )
    except model.DoesNotExist:
        logger.info("Creating Response Object")
        Response( device = deviceObj , datatype = dataTypeObj , value = "" )

#enddef

