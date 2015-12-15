from GardenServer.models import User

import hashlib
import logging

logger = logging.getLogger(__name__)

def authUser( authObj ):

    try:
        logger.info( "Authenticating User: " + authObj['username'] )
        userObj = User.objects.get( identifier = authObj['username'] )
    except User.DoesNotExist:
        logger.error( "User Not Found" )
        return None

    userPassword = generateIdentifier( authObj['password'] )
    logger.debug( "Password: " + userPassword + " UserObject: " + userObj.password )
    if userObj.password == userPassword:
        return userObj;
    else:
        logger.error( "Failed Verification" )
        return None;

#enddef

def generateIdentifier( saltList ):

    salt = ""
    for i in saltList:
        salt = salt + str(i)
    logger.debug( "Salt: " + salt )
    return hashlib.sha256(salt).hexdigest()
