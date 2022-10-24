# Lingua
Own ru-eng dictionary

Used in the project:
- Django 4.1
- Python 3.8.10
- HTML, CSS, JS, AJAX
- MySQL

## Description
There are 2 apps in the project:
- "dictionary" - main functionality 
- "account" - user registration and authorization

The service allows you to add, edit, delete, train words. Implemented registration and authorization.  
Working with folders is organized through Django Base views and MySQL database. Implemented pagination

Sliding Menu
implemented with AJAX

![myimg](https://github.com/KurhanovichPy/Lingua/blob/master/folders.png)

Adding, updating, deleting words organized through Django Base views and MySQL database.
Data entry is carried out through a modal window with JS.

![myimg](https://github.com/KurhanovichPy/Lingua/blob/master/words.png)

Every word has a state of learning  

 4 states in total:  
- new word (indicated by a red star)  
- learning word (indicated by a yellow star)  
- learned word (indicated by a green star)  
- word to be repeated (indicated by a purple star)

Training changes the status from new to learned, the word is sent for repetition if it has not been in training for more than two weeks.  

![myimg](https://github.com/KurhanovichPy/Lingua/blob/master/quiz.png)

Training is implemented with JS + CSS.

Language switcher is made with JS + CSS.

![myimg](https://github.com/KurhanovichPy/Lingua/blob/master/quiz_eng.png)

### Registration and authorization:
- Django authentication

### Frontend:
- HTML
- CSS
- JS
- AJAX
- Jinja
- Working with static and links
