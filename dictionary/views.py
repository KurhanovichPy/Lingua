import datetime
import json
import random
import requests
from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from dictionary.models import Dictionary, Directory, DictionaryVoice, EnglishWords, RussianWords
from .conversion import text_conversion

NUM_PAGES = 1


class DictionaryListView(ListView):
    model = Dictionary

    template_name = 'dictionary/dict.html'

    def get_context_data(self, **kwargs):
        directory = Directory.objects.get(user=self.request.user, id=self.kwargs['pk'])
        word_count = Dictionary.objects.filter(user=self.request.user, directory=self.kwargs['pk']).count()
        context = super().get_context_data(**kwargs)
        context['pk'] = directory.id
        context['dir_name'] = directory.name
        context['word_count'] = word_count
        return context

    def get_queryset(self):
        queryset = Dictionary.objects.filter(user=self.request.user, directory=self.kwargs['pk'])
        return queryset


class DirectoryListView(ListView):
    model = Directory
    template_name = 'dictionary/directory.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        dir_count = Directory.objects.filter(user=self.request.user).count()
        context = super().get_context_data(**kwargs)
        context['dir_count'] = dir_count
        return context

    def get_queryset(self):
        queryset = Directory.objects.filter(user=self.request.user)
        return queryset

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        if queryset.count() != 0:
            global NUM_PAGES
            NUM_PAGES = paginator.num_pages
        return super().paginate_queryset(queryset, page_size)


class DirectoryCreateView(CreateView):
    model = Directory
    fields = ['name']

    def get_success_url(self):
        link = f'/?page={NUM_PAGES}'
        return link

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DictionaryCreateView(CreateView):
    model = Dictionary
    fields = ['native_word', 'translate_word']

    def form_valid(self, form):
        translate_word = self.request.POST['translate_word']
        words_with_voices = DictionaryVoice.objects.all()
        words_with_voices_list = [word.word for word in words_with_voices]
        if translate_word not in words_with_voices_list:
            text_conversion(translate_word, 'en')
            DictionaryVoice.objects.create(word=translate_word,
                                           voice_path=f'dictionary/mp3/{translate_word}.mp3')
        form.instance.user = self.request.user
        form.instance.directory = Directory.objects.get(user=self.request.user, id=self.kwargs['pk'])
        form.instance.voice_path = f'dictionary/mp3/{translate_word}.mp3'
        form.instance.status = 1
        form.instance.add_data = datetime.datetime.now()
        form.instance.last_training_data = datetime.datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('words', kwargs={'pk': self.kwargs['pk']})


class DirectoryDeleteView(DeleteView):
    model = Directory

    def get_success_url(self):
        if NUM_PAGES == 1:
            link = f'/?page={NUM_PAGES}'
        else:
            link = f'/?page={NUM_PAGES - 1}'
        return link


class DictionaryDeleteView(DeleteView):
    model = Dictionary

    def get_success_url(self):
        word_id = self.kwargs['pk']
        pk = Dictionary.objects.get(id=word_id).directory.id
        return reverse('words', kwargs={'pk': pk})


class DictionaryUpdateView(UpdateView):
    model = Dictionary

    fields = ['native_word', 'translate_word']

    def form_valid(self, form):
        translate_word = self.request.POST['translate_word']
        words_with_voices = DictionaryVoice.objects.all()
        words_with_voices_list = [word.word for word in words_with_voices]
        if translate_word not in words_with_voices_list:
            text_conversion(translate_word, 'en')
            DictionaryVoice.objects.create(word=translate_word,
                                           voice_path=f'dictionary/mp3/{translate_word}.mp3')
        return super().form_valid(form)

    def get_success_url(self):
        word_id = self.kwargs['pk']
        pk = Dictionary.objects.get(id=word_id).directory.id
        return reverse('words', kwargs={'pk': pk})


def quiz(request, pk):
    current_method = request.method
    template = loader.get_template('dictionary/quiz.html')
    # Select a set of words for training
    if pk == 'new':
        words = Dictionary.objects.filter(user=request.user, status=1)
    elif pk == 'learning':
        words = Dictionary.objects.filter(user=request.user, status__in=[2, 3, 4])
    elif pk == 'learned':
        words = Dictionary.objects.filter(user=request.user, status=5)
    elif pk == 'repeat':
        words = Dictionary.objects.filter(user=request.user, status=6)
    else:
        directory = Directory.objects.get(id=pk)
        words = Dictionary.objects.filter(user=request.user, directory=directory)
    answers_list = []
    for word in words:
        # The key 'switch_eng' is passed from JS
        # If the key is passed, the training is ENG-RU, else RU-ENG
        if request.POST.get('switch_eng', 0) == '1':
            answers_list.append(word.native_word)
        else:
            answers_list.append(word.translate_word)
        if word.status < 5 and datetime.datetime.now() != word.last_training_data:
            word.status += 1
            word.save(update_fields=["status"])
        elif word.status == 6:
            word.status = 5
            word.save(update_fields=["status"])
        word.last_training_data = datetime.datetime.now()
        word.save(update_fields=["last_training_data"])
    answers_count = words.count() * 3

    for _ in range(answers_count):
        if request.POST.get('switch_eng', 0) == '1':
            word_id = random.randint(1, 51301)
            rand_word = RussianWords.objects.get(id=word_id)
        else:
            word_id = random.randint(1, 1771)
            rand_word = EnglishWords.objects.get(id=word_id)
        answers_list.append(rand_word.word)
    if request.POST.get('switch_eng', 0) == '1':
        words_dict = {word.translate_word: word.native_word for word in words}
    else:
        words_dict = {word.native_word: word.translate_word for word in words}
    random.shuffle(answers_list)
    context = {
        'words': json.dumps(words_dict),
        'answers': json.dumps(answers_list),
        'current_method': current_method
    }
    return HttpResponse(template.render(context, request))


def statistic(request):
    user = request.user
    words = Dictionary.objects.filter(user=user)
    for word in words:
        if (datetime.datetime.now() - word.last_training_data).days > 14:
            word.status = 6
            word.save(update_fields=["status"])
    new = Dictionary.objects.filter(user=user, status=1).count()
    learning = Dictionary.objects.filter(user=request.user, status__in=[2, 3, 4]).count()
    learned = Dictionary.objects.filter(user=request.user, status=5).count()
    repeat = Dictionary.objects.filter(user=request.user, status=6).count()
    data = {
        "new": new,
        "learning": learning,
        "learned": learned,
        "repeat": repeat
    }
    return render(request, 'dictionary/statistic.html', {'data': data})
