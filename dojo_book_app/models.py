from dojo_login_app.models import User
from django.db import models
import re

# Create your models here.
class AuthorManager(models.Manager):
    def validator_field(self, postData):
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')

        errors = {}

        if postData['name'] == postData['name']:
                errors['name'] = "Autor ya existe"
        else:
            if len(postData['name'].strip()) < 2 or len(postData['name'].strip()) > 30:
                errors['first_name_len'] = "Nombre debe tener entre 2 y 30 caracteres"

            if not JUST_LETTERS.match(postData['name']) or not JUST_LETTERS.match(postData['name']):
                errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
            
        return errors
        

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()
    

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, related_name="authors", on_delete = models.CASCADE)
    users = models.ForeignKey(User, related_name='users_book', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title 
    

class Reviews(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_reviews", on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name="book_reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    


    def __str__(self):
            return self.comment 