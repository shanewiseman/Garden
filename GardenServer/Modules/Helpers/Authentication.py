from GardenServer.models import User

import md5
import logging

logger = logging.getLogger(__name__)

def validate( authObj ):

    try:
        logger.info( "Authenticating User: " + authObj.username )
        userObj = User.objects.get( identifier = authObj.username )
    except model.DoesNotExist:
        logger.error( "User Not Found" )
        return 0

    userPassword = md5.new().update( authObj.password ).hexdigest()
    logger.debug( "Password: " + userPassword + "UserObject: " + userObj.password )
    if userObj.password == userPassword:
        return userObj;
    else:
        logger.error( "Pass Failed Verification" )
        return None;

#enddef
