from GardenServer.models import Device , DataType , Response , ProcessorInstance
from paramiko import SSHClient
from django.conf import settings

import paramiko
import logging

logger = logging.getLogger(__name__)

def createProcessor( dataTypeObj , deviceObj , responseObj ):

    logger.info("Creating New Data Processor" )

    pcount = ProcessorInstance.objects.all().count()

    logger.debug(str(pcount) + " Existing Active Processors")

    instance = __startInstance( deviceObj , dataTypeObj , responseObj , pcount )

    ProcessorInstance(
        identifier = instance['identifier'],
        node = instance['node'],
        datatype = dataTypeObj,
        device = deviceObj,
        response = responseObj
    ).save()

#enddef

def __startInstance( device , datatype , response , pcount ):

    processorNode = settings.PROCCESSOR_NODES[ (pcount + 1 ) % len( settings.PROCCESSOR_NODES ) ]

    logger.debug("Creating Node On " + processorNode )

    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    rsa_private_key = paramiko.RSAKey.from_private_key_file( settings.SSHID )
    client.connect( processorNode , username="swiseman" , pkey = rsa_private_key )

    logger.debug( 'docker run -d ' + datatype.processor + ' python /root/Processor.py ' + settings.MASTER_HOSTNAME + \
            ' ' + device.identifier + ' ' + datatype.identifier + ' ' + response.identifier )

    stdin, stdout, stderr = client.exec_command(
            'docker run -d ' + datatype.processor + ' python /root/Processor.py ' + settings.MASTER_HOSTNAME + \
                    ' ' + device.identifier + ' ' + datatype.identifier + ' ' + response.identifier
    )

    for i in stderr.readlines():
        logger.error(str(i))
    for i in stdout.readlines():
        logger.debug(str(i))
        identifier = i

    return { 'identifier' : identifier , 'node' : processorNode }




