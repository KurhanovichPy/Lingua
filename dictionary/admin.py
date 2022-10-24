from django.contrib import admin
from .models import (Dictionary,
                     Directory,
                     DictionaryVoice)

admin.site.register(Dictionary)
admin.site.register(Directory)
admin.site.register(DictionaryVoice)

