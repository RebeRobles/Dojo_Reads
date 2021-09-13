from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        if request.method == 'POST':
            errors = User.objects.validator_field(request.POST)

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request,value)

                request.session['registro_nombre'] = request.POST['nombre']
                request.session['registro_alias'] = request.POST['alias']
                request.session['registro_email'] = request.POST['email']

            else:
                request.session['registro_nombre'] = ""
                request.session['registro_alias'] = ""
                request.session['registro_email'] = ""

                nombre = request.POST['nombre']
                alias = request.POST['alias']
                email = request.POST['email']
                password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

                obj = User.objects.create(nombre=nombre, alias=alias, email=email, password=password_hash)
                messages.success(request, "Usuario registrado con éxito")
            
            return redirect('/')

        return render(request, 'dojo_login_app/login.html')

def login(request):
    if request.method == 'GET':
        return redirect("/")
    else:
        if request.method == 'POST': 
            user = User.objects.filter(email=request.POST['email_login']) 
            if len(user) > 0 : 
                usuario_registrado = user[0]
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()): 
                    usuario = {
                        'id':usuario_registrado.id,
                        'nombre':usuario_registrado.nombre,
                        'alias':usuario_registrado.alias,
                        'email':usuario_registrado.email,
                    }

                    request.session['usuario'] = usuario
                    messages.success(request,"Ingreso correctamente")
                    return redirect('/book')
                else:
                    messages.error(request,"Datos erróneos o el usuario no existe")
                    return redirect('/')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                return redirect('/')

