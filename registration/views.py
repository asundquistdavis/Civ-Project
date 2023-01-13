from django.shortcuts import render, redirect
from .forms import NewUserForm

def newuser(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = NewUserForm()
    return render(request, 'registration/newuser.html', {'form': form})

def logoutnext(request):
    return render(request, 'registration/logoutnext.html')
