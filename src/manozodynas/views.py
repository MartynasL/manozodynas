from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import LoginForm
from .models import Word
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy


def index_view(request):
    return render(request, 'manozodynas/index.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    #import ipdb; ipdb.set_trace()
    return render(request, 'manozodynas/login.html', {'form': form})


def wordlist_view(request):
    return render(request, 'manozodynas/wordlist.html', {'words':
                                                             Word.objects.all()})


class AddWordView(CreateView):
    model = Word
    template_name = 'manozodynas/addword.html'
    success_url = reverse_lazy('wordlist')