from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q as Query
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# ---------------------------------------------------->  logg In/Out/Register User
def loginPage(request):
    """
    Maneja la página de inicio de sesión.

    Si el usuario ya está autenticado, se redirige a la página de inicio.
    Si el método de solicitud es POST, intenta autenticar al usuario y redirigirlo si es válido.
    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'El usuario/contraseña incorrecta')

    context = {'page': page}
    return render(request, 'BASE/login_register.html', context)

def registerPage(request):
    """
    Maneja la página de registro de usuarios.

    Si el método de solicitud es POST, intenta crear un nuevo usuario y redirigirlo si el formulario es válido.
    """
    page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ha ocurrido un error durante el registro')
    
    context = {'form': form}
    return render(request, 'BASE/login_register.html', context)


@login_required(login_url='login')
def updateUser(request):
    """
    Permite a los usuarios autenticados actualizar su perfil.

    Si el método de solicitud es POST y el formulario es válido, actualiza la información del usuario y redirige a la página de perfil del usuario.
    """
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'BASE/update-user.html', {'form': form})

def logoutUser(request):
    """
    Maneja el cierre de sesión de usuarios y redirige a la página de inicio.
    """
    logout(request)
    return redirect('home')


# ----------------------------------------------------> User
def userProfile(request, pk):
    """
    Muestra el perfil de un usuario junto con las salas y mensajes asociados.

    :param pk: El ID del usuario cuyo perfil se va a mostrar.
    """
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'BASE/profile.html', context)

def home(request):
    """

    Muestra la página principal (dashboard) con las salas, temas y mensajes filtrados.

    """
    query = request.GET.get('query') if request.GET.get('query') is not None else ''
    rooms = Room.objects.filter(
        Query(topic__name__icontains=query) |
        Query(name__icontains=query) |
        Query(description__icontains=query)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(Query(room__topic__name__icontains=query))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'BASE/home.html', context)


# ---------------------------------------------------->  Room
def room(request, pk):
    """
    Muestra una sala específica con mensajes y participantes.

    :param request: La solicitud HTTP recibida.
    :param pk: El ID de la sala que se va a mostrar.
    :return: Renderiza la plantilla 'BASE/room.html' con los detalles de la sala, los mensajes y los participantes.
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body')
        if not body:
            messages.error(request, 'El mensaje está vacío!')
        else:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'BASE/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    """
    Crea una nueva sala.

    :param request: La solicitud HTTP recibida.
    :return: Si el formulario es válido, crea una nueva sala y redirige a la página de inicio.
    """
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    """
    Actualiza los detalles de una sala existente.

    :param request: La solicitud HTTP recibida.
    :param pk: El ID de la sala que se va a actualizar.
    :return: Si el formulario es válido, actualiza los detalles de la sala y redirige a la página de inicio.
    """
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('No perteneces aquí!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'BASE/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    """
    Elimina una sala existente.

    :param request: La solicitud HTTP recibida.
    :param pk: El ID de la sala que se va a eliminar.
    :return: Si la solicitud es POST, elimina la sala y redirige a la página de inicio.
    """
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('No perteneces aquí!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'BASE/delete.html', {'obj': room})

# ---------------------------------------------------->  Messages
@login_required(login_url='/login')
def deleteMessage(request, pk):
    """
    Elimina un mensaje existente.

    :param request: La solicitud HTTP recibida.
    :param pk: El ID del mensaje que se va a eliminar.
    :return: Si la solicitud es POST, elimina el mensaje y redirige a la página de inicio.
    """
    message = Message.objects.get(id=pk)
    room = Message.room
    if request.user != message.user:
        return HttpResponse('No perteneces aquí!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'BASE/delete.html', {'obj': message})

# ---------------------------------------------------->  Views Mobile
def topicsPage(request):
    """
    Muestra la página de temas.

    :param request: La solicitud HTTP recibida.
    :return: Renderiza la plantilla 'BASE/topics.html' con los temas filtrados.
    """
    query = request.GET.get('query') if request.GET.get('query') is not None else ''
    topics = Topic.objects.filter(name__contains=query)
    context = {'topics': topics}
    return render(request, 'BASE/topics.html', context)

def activityPage(request):
    """
    Muestra la página de actividad.

    :param request: La solicitud HTTP recibida.
    :return: Renderiza la plantilla 'BASE/activity.html' con todos los mensajes.
    """
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'BASE/activity.html', context)
