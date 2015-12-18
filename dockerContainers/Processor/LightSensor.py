import time

class LightSensor:

    # required function
    def process(self , data ):
        # current time module 24 hours of seconds, convert to hours, subtract EST
        hour = ( ( int( time.time() % 86400 ) / 3600 ) - 5 )

        if hour > self.lightOn and hour < self.lightOff:
            self.logger.info("Turning/Keeping Light On!")
            return 1

        self.logger.info("Turning/Keeping Light Off!")
        return 0


    #required function
    def defaultResponse( self ):
        return 0

    def __init__(self, logger):
            logger.info("INITTIALIZING OBJECT")
            # requred attributes
            self.request_points = 0
            self.request_time   = 0
            self.iterTime       = 360
            self.logger         = logger

            # class specific
            self.lightOn  = 5  #5am
            self.lightOff = 20 #8pm



