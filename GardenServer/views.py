from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from GardenServer.Modules.Helpers import Authentication
from GardenServer.Modules.Core    import DataRequest
from GardenServer.Modules.Core    import ProcessorRequest

import json
import logging

logger = logging.getLogger(__name__)

################################################################################
#------------------------------------------------------------------------------#
################################################################################
def dataRequest(request):

    logger.info( "Processing " + request.method + " Data Request" )

    responseObj = HttpResponse()

    try:
        logger.debug( "Body:\n" + request.body + "\n" )
        reqBody = json.loads( request.body )

    except Exception as ex:
        logger.error( "Failed To Parse Body" )
        logger.error(ex)
        responseObj.status_code = 400
        return responseObj

    if 'auth' not in reqBody:
        responseObj.status_code = 400
        return responseObj

    try:
        userObj = Authentication.authUser( reqBody['auth'] )
    except Exception as ex:
        logger.error(ex)
        responseObj.status_code = 400
        return responseObj

    if userObj == None:
        responseObj.status_code = 401
        return responseObj
#------------------------------------------------------------------------------#
    if request.method == 'POST':

        if 'data' not in reqBody:
            responseObj.status_code = 400
            return responseObj

        try:
            if DataRequest.request( userObj , reqBody['data'] ):
                responseObj.status_code = 202
                return responseObj
            else:
                responseObj.status_code = 400
                return responseObj
        except Exception as ex:
            logger.error(ex)
            responseObj.status_code = 500
            return responseObj

#------------------------------------------------------------------------------#
    if request.method == 'GET':

        try:
            result = DataRequest.response( userObj )
        except Exception as ex:
            logger.error(ex)
            responseObj.status_code = 500
            return responseObj

        if result == None:
            responseObj.status_code = 400
            return responseObj

        return HttpResponse(result, content_type='application/json' )
    #endif

#------------------------------------------------------------------------------#
    responseObj.status_code = 402
    return responseObj
#enddef
################################################################################
#------------------------------------------------------------------------------#
################################################################################
def processorRequest( request ):

    logger.info( "Processing " + request.method + " Processor Request" )
    responseObj = HttpResponse()

    try:
        logger.debug( "Body:\n" + request.body + "\n" )
        reqBody = json.loads( request.body )

    except Exception as ex:
        logger.error( "Failed To Parse Body" )
        logger.error(ex)
        responseObj.status_code = 400
        return responseObj

    if 'auth' not in reqBody:
        responseObj.status_code = 400
        return responseObj

    try:
        userObj = Authentication.authUser( reqBody['auth'] )
    except Exception as ex:
        logger.error(ex)
        responseObj.status_code = 400
        return responseObj

    if userObj == None:
        responseObj.status_code = 401
        return responseObj

#------------------------------------------------------------------------------#


    if request.method == 'POST':

        if 'response' not in reqBody:
            responseObj.status_code = 400
            return responseObj

        try:
            if ProcessorRequest.postResponse( reqBody['response'] ):
                responseObj.status_code = 202
                return responseObj
            else:
                responseObj.status_code = 400
                return responseObj

        except Exception as ex:
            logger.error(ex)
            responseObj.status_code = 500
            return responseObj


#------------------------------------------------------------------------------#
    if request.method == 'GET':
        if 'request' not in reqBody:
            responseObj.status_code = 400
            return responseObj

        try:
            result = ProcessorRequest.getData( reqBody['request'] )
        except Exception as ex:
            logger.error(ex)
            responseObj.status_code = 500
            return responseObj

        if result == None:
            responseObj.status_code = 400
            return responseObj


        return HttpResponse(result, content_type='application/json' )



