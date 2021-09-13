from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validator_field(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exits'] = "Email ya registrado"
        else:
            if len(postData['nombre'].strip()) < 2 or len(postData['nombre'].strip()) > 30:
                errors['nombre_len'] = "Nombre debe tener entre 2 y 30 caracteres"

            if len(postData['alias'].strip()) < 2 or len(postData['alias'].strip()) > 15:
                errors['alias_len'] = "Alias debe tener entre 2 y 15 caracteres"
            
            #if not JUST_LETTERS.match(postData['nombre']) or not JUST_LETTERS.match(postData['alias']):
            #    errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y alias"
                
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Formato correo no válido"
            
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido" 

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Contraseñas no coinciden"

        return errors


class User(models.Model):
    nombre = models.CharField(max_length=100)
    alias = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["alias",]

    def __str__(self):
            return self.nombre  


    def __repr__(self):
        return self.alias + " " + self.nombre
        



