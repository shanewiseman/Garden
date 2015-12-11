from __future__ import unicode_literals

from django.db import models

class Device ( models.Model ):
    name        = models.CharField( max_length = 255 )
    password    = models.CharField( max_length = 32 )
    description = models.CharField( blank = True , max_length = 255 )
    created     = models.DateTimeField(auto_now=True)

class DataType ( models.Model ):
    name        = models.CharField( max_length = 255 )
    description = models.CharField( blank = True , max_length = 255 )

class Data ( models.Model ):
    created     = models.DateField()
    value       = models.TextField()
    device      = models.ForeignKey( Device , on_delete=models.CASCADE )
    datatype    = models.ForeignKey( DataType , on_delete=models.CASCADE )

class Response ( models.Model ):
    created     = models.DateTimeField(auto_now=True)
    value       = models.TextField()
    device      = models.ForeignKey( Device , on_delete=models.CASCADE )


