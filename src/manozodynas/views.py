from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import LoginForm, AddTranslationForm
from .models import Word, Translation
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
    return render(request, 'manozodynas/wordlist.html',
                  {'words': Word.objects.all()})


def translationlist_view(request):
    if request.method == "POST":
        translation_vote = Translation.objects.get(pk=request.POST.get('id'))
        if request.POST.get('plus'):
            translation_vote.vote += 1
        if request.POST.get('minus'):
            translation_vote.vote -= 1
        translation_vote.save()

    return render(request, 'manozodynas/translationlist.html',
                  {'translations': Translation.objects.all()})


class AddWordView(CreateView):
    model = Word
    template_name = 'manozodynas/addword.html'
    success_url = reverse_lazy('word_list')


class AddTranslationView(CreateView):
    form_class = AddTranslationForm
    template_name = 'manozodynas/addtranslation.html'
    success_url = reverse_lazy('translation_list')
