from GardenServer.models          import Response,Data
from GardenServer.Modules.Helpers import DataFormat
from GardenServer.Modules.Core    import GardenModels

import datetime
import time
import logging

logger = logging.getLogger(__name__)

def postResponse( data ):
    logger.info("POST PROCESSOR REQUESET");

    for responseIdent in data:
        if GardenModels.getResponse(identifier = responseIdent ) == None:
            return False
    #endfor

    for responseIdent in data:
        responseObj = GardenModels.getResponse(identifier = responseIdent )
        responseObj.value = data[ responseIdent ]
        responseObj.save()

    return True

def getData( request ):
    logger.info("GET PROCESSOR REQUESET");

    response = {}
    dataCount = 0

    for device in request:

        logger.debug("Device: " + device)
        response[ device ] = {}

        for datatype in request[ device ]:

            logger.debug("DataType: " + datatype )
            response[ device ][ datatype ] = {}

            data = GardenModels.getDataRange(
                int(request[ device ][ datatype ]['points']),
                device   = device,
                datatype = datatype
            )

            dataCount = dataCount + len(data)

            logger.debug("Data Returned: " + str(data))
            for datapoint in data:

                dataAge = int( ( datapoint.created.replace(tzinfo=None) - datetime.datetime(1970,1,1)).total_seconds() )
                if 'time' in request[ device ][ datatype ] :
                    if dataAge < ( int( time.time() ) - request[ device ][ datatype ]['time' ] ) :
                        logger.debug(int( time.time() ) - dataAge )
                        dataCount = dataCount - 1
                        continue

                response[ device ][ datatype ][ datapoint.identifier ] = {
                    'value'      : datapoint.value,
                    'created'    : int( ( datapoint.created.replace(tzinfo=None) - datetime.datetime(1970,1,1)).total_seconds() )
                }
        #endfor
    #endfor
    logger.info("Returning: " + str(dataCount) + " Points of Data")
    return DataFormat.formatJsonResponse( response )

#enddef

