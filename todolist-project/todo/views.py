from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import TodoList
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def signupuser(request):
    if request.method == 'GET': #means that user just entered the url without entering any data
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else: #means that it is a POST
        #create a new user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            raw_password2 = form.cleaned_data.get('password2')
            if(raw_password == raw_password2):
                user = authenticate(username=username, password=raw_password)
                login(request,user)
                return redirect('currenttodos')
        else:
            errors = list(form.errors.values())
            print(errors)
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm()
                , 'errors': errors})



@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET': #means that user just entered the url without entering any data
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(),
                'error':'Username and Password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def currenttodos(request):
    todolist = TodoList.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/currenttodos.html',
            {'todolist':todolist})

@login_required
def todoview(request,todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/todoview.html',
                {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/todoview.html',
                    {'todo':todo, 'form':form, 'error':'Bad data entered. Try again.'})

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False) #It will save the form but not insert into database because commit is false
            newTodo.user = request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(),
                'error':'Bad data entered. Try again.'})

@login_required
def completetodoview(request, todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.completedFlag = True
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodoview(request, todo_pk):
    todo = get_object_or_404(TodoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todolist = TodoList.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completedtodos.html',
            {'todolist':todolist})
