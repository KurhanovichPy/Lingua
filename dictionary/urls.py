from django.urls import path
from .views import (DictionaryListView,
                    DirectoryListView,
                    DirectoryCreateView,
                    DictionaryCreateView,
                    DirectoryDeleteView,
                    DictionaryDeleteView,
                    DictionaryUpdateView,
                    quiz,
                    statistic)

urlpatterns = [
    path('', DirectoryListView.as_view(), name='directories'),
    path('directory/<pk>', DictionaryListView.as_view(), name='words'),
    path('create/', DirectoryCreateView.as_view()),
    path('<pk>/delete', DirectoryDeleteView.as_view()),
    path('<pk>/create', DictionaryCreateView.as_view()),
    path('word/<pk>/delete', DictionaryDeleteView.as_view()),
    path('<pk>/update', DictionaryUpdateView.as_view()),
    path('<pk>/quiz/', quiz),
    path('statistic/', statistic),

]
