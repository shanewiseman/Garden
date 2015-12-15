from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from GardenServer.Modules.Helpers import Authentication
from GardenServer.Modules.Core    import DataRequest

import json
import logging

logger = logging.getLogger(__name__)

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

    try:
        userObj = Authentication.authUser( reqBody['auth'] )
    except Exception as ex:
        logger.error(ex)
        responseObj.status_code = 400
        return responseObj

    if userObj == None:
        responseObj.status_code = 401
        return responseObj

    if request.method == 'POST':

        if reqBody['data'] == None:
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

    responseObj.status_code = 402
    return responseObj
#enddef

def processorRequest( request ):

    logger.info( "Processing " + request.method + " Processor Request" )

    if request.method == 'GET':
        try:
            logger.debug( "Body:\n" + request.body + "\n" )
            reqBody = json.loads( request.body )

        except Exception as ex:
            logger.error( "Failed To Parse Body" )
            logger.error(ex)
            responseObj.status_code = 400
            return responseObj


        return HttpResponse('{ "key" : "value" }')

    if request.method == 'POST':
        try:
            logger.debug( "Body:\n" + request.body + "\n" )
            reqBody = json.loads( request.body )

        except Exception as ex:
            logger.error( "Failed To Parse Body" )
            logger.error(ex)
            responseObj.status_code = 400
            return responseObj


        return HttpResponse('ACCEPTED')


