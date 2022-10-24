from django.db import models


class Directory(models.Model):
    user = models.CharField(max_length=40)
    name = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user} - {self.name}'

    class Meta:
        ordering = ['id']


class Dictionary(models.Model):
    user = models.CharField(max_length=40)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    native_word = models.CharField(max_length=40)
    translate_word = models.CharField(max_length=40)
    add_data = models.DateTimeField()
    last_training_data = models.DateTimeField()
    status = models.IntegerField()

    def __str__(self):
        return f'{self.native_word} - {self.translate_word}'


class DictionaryVoice(models.Model):
    word = models.CharField(max_length=20)
    voice_path = models.CharField(max_length=40)


class EnglishWords(models.Model):
    word = models.CharField(max_length=40)


class RussianWords(models.Model):
    word = models.CharField(max_length=40)
