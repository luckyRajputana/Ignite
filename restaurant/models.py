from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Board(models.Model):
#     name = models.CharField(max_length = 30, unique = True)
#     desciption = models.CharField(max_length = 100)
#     def __str__(self):
#         return self.name

# class Topic(models.Model):
#     subject = models.CharField(max_length=255)
#     last_updated = models.DateTimeField(auto_now_add=True)
#     board = models.ForeignKey(Board,on_delete=None, related_name='topics')
#     starter = models.ForeignKey(User,on_delete=None, related_name='topics')
#     def __str__(self):
#         return self.subject

# class Post(models.Model):
#     message = models.TextField(max_length=4000)
#     topic = models.ForeignKey(Topic,on_delete=None, related_name='posts')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True)
#     created_by = models.ForeignKey(User,on_delete=None, related_name='posts')
#     updated_by = models.ForeignKey(User,on_delete=None, null=True, related_name='+')


class Assembly(models.Model):
    assemblyLineNO = models.CharField(max_length=20)
    binId = models.CharField(max_length=20)
    binName =  models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return "Id:{} {}  binID:{} {}  binName:{} {}  Time:{} {}  ".format('  ',self.assemblyLineNO,'  ', self.binId,'  ',self.binName,'  ', self.timestamp)
        
