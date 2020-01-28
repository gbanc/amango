from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm
from rq import Queue
from worker import conn

q = Queue(connection=conn)

def count_stuff(range):
    return sum(range)

def signup(request):
    r = range(1,4)
    q.enqueue(count_stuff(), r)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

    