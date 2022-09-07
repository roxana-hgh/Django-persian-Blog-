from pyexpat import model
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from PIL import Image



class Post(models.Model):

    CATEGORY = (
			('سفر', 'سفر'),
			('سرگرمی', 'سرگرمی'),
            ('تکنولوژی', 'تکنولوژی'),
            ('محیط زیست', 'محیط زیست'),
            ('زیبایی و پوشاک','زیبایی و پوشاک'),
            ('سلامتی','سلامتی'),
			) 

    author = models.ForeignKey(User,
            on_delete=models.CASCADE,
            related_name='blog_posts')
    title = models.CharField(max_length=500)        
    body = RichTextField(blank=True, null=True)
    date = models.DateTimeField(default = timezone.now)
    image = models.ImageField(upload_to ='uplodes',blank = False)
    category = models.CharField(max_length=200, choices=CATEGORY)
    likes = ManyToManyField(User, related_name='post_like', blank=True)
    
    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    body =  models.TextField(max_length = 600, default='')

    def __str__(self):
        return self.body



class Profile(models.Model):
    user = OneToOneField(User, on_delete = models.CASCADE, null=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True, upload_to ='uplodes/profiles', default='uplodes/profiles/default-profile-pic.jpg' )
    instagram_url = models.CharField(max_length=350, blank=True, null=True)
    twitter_url = models.CharField(max_length=350, blank=True, null=True)
    linkedin_url = models.CharField(max_length=350, blank=True, null=True)
    website_url = models.CharField(max_length=350, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):

        if not self.profile_pic:  #here
            self.profile_pic = 'uplodes/profiles/default-profile-pic.jpg'
        super(Profile, self).save(*args, **kwargs)
        
        super().save()
        img = Image.open(self.profile_pic.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.profile_pic.path)



class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    another_user = models.ManyToManyField(User, related_name='following',symmetrical=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



