from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name   = models.CharField(max_length=30)
    weight = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    description  = models.CharField(max_length=255)
    likes		 = models.IntegerField(default=0)
    dislikes	 = models.IntegerField(default=0)
    tags		 = models.ManyToManyField(Tag)
    date_created = models.DateField(auto_now_add=True)
 	
    def __str__(self):
        return ('{} created at {}'.format(self.description,self.date_created))

class Image(models.Model):
    post        = models.ForeignKey(Post,on_delete=models.CASCADE)
    post_image  = models.ImageField(upload_to='images/') 

    def __str__(self):
        return ('Image from {}'.format(self.post.description))
        
class Interest(models.Model):  
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    post     = models.ForeignKey(Post,on_delete=models.CASCADE)
    status   = models.BooleanField()
    
    def __str__(self):
        return ('{} by {} is {}'.format(self.post,self.user,self.status))

