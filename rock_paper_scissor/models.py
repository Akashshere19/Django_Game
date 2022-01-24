from django.db import models
from django.contrib.auth.models import User #this is add line
# Create your models here.
class Player(models.Model):
    # Create Player's Model
    name =models.CharField(max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='player')
    def __str__(self):
        return self.name

class Result(models.Model):
    #result model in which all player  will be stored

    player=models.ForeignKey('Player',on_delete=models.CASCADE,related_name='score')
    bot_move = models.CharField(max_length=50,blank =True)
    user_move= models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return 'status --'+' '+self.player.name
