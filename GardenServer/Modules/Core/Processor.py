from GardenServer.model import Device , DataType , ProcessorInstance

def createProcessor( dataTypeObj , deviceObj ):

    instance = __startInstance( deviceObj.identifier , dataTypeObj.identifier )

    ProcessorInstance(
        identifier = instance['identifier'],
        channel = instance['channel'],
        device = dataTypeObj,
        datatype = deviceObj
    ).save()

#enddef

def __startInstance( device , datatype )
