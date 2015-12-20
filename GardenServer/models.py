from __future__ import unicode_literals

from django.db import models


class User ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    name        = models.CharField( max_length = 255 )
    password    = models.CharField( max_length = 64 )
    description = models.CharField( blank = True , max_length = 255 )
    created     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier

class Device ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    name        = models.CharField( max_length = 255 )
    description = models.CharField( blank = True , max_length = 255 )
    created     = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey( User , on_delete=models.CASCADE )

    def __str__(self):
        return self.identifier

class DataType ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    name        = models.CharField( max_length = 255 )
    description = models.CharField( blank = True , max_length = 255 )
    processor   = models.CharField( max_length = 255 )

    def __str__(self):
        return self.identifier

class Data ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    created     = models.DateTimeField(auto_now=True)
    value       = models.TextField()
    device      = models.ForeignKey( Device , on_delete=models.CASCADE )
    datatype    = models.ForeignKey( DataType , on_delete=models.CASCADE )

    def __str__(self):
        return self.identifier

class Response ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    created     = models.DateTimeField(auto_now=True)
    value       = models.TextField()
    device      = models.ForeignKey( Device , on_delete=models.CASCADE )
    datatype    = models.ForeignKey( DataType , on_delete=models.CASCADE )

    def __str__(self):
        return self.identifier

class ProcessorInstance ( models.Model ):
    identifier  = models.CharField( max_length = 64 , primary_key=True )
    node        = models.CharField( max_length = 255 )
    device      = models.ForeignKey( Device , on_delete=models.CASCADE )
    datatype    = models.ForeignKey( DataType , on_delete=models.CASCADE )
    response    = models.ForeignKey( Response , on_delete=models.CASCADE )
    created     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier


