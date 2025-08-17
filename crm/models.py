from django.db import models
from django.utils import timezone
import uuid
from accounts.models import User

# Content models
class Event(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event/image/', null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=200, blank=True)
    video_url = models.FileField(upload_to='videos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}" 

class Music(models.Model):
    music = models.FileField(upload_to='music/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    
    def __str__(self):
        return f"{self.title}"  

class Book_File(models.Model):
    book_file = models.FileField(upload_to="books/path/", blank=True, null=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    file_url = models.ForeignKey(Book_File, on_delete=models.CASCADE, related_name='file_url')
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    cover_image_url = models.ImageField(upload_to="books/images/", blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.file_url.book_file} - {self.title}"
    

class About(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.content}" 

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}" 
    
    
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=200, blank=True)
    image_url = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Testimonial by {self.name}"
