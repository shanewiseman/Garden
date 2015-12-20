import json
import re

def formatJsonResponse( data ):

    response = json.dumps( data )
    response = re.sub(r'\\','', response)
    response = re.sub(r'"\{','{', response)
    response = re.sub(r'\}"','}', response)
    response = re.sub(r'"\[','[', response)
    response = re.sub(r'\]"',']', response)
    response = re.sub(r'""','"', response)

    return response
