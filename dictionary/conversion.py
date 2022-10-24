from gtts import gTTS
from django.conf import settings


def text_conversion(text, language):
    myobj = gTTS(text=text, lang=language, slow=False)
    new_path = settings.BASE_DIR
    print(new_path)
    myobj.save(f"{new_path}\\dictionary\\static\\dictionary\\mp3\\{text}.mp3")

