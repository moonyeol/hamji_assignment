# Hamji

Welcome to Tridge sandbox project!

We'd love to collaborate with amazing developers as we drive the development of "Global Sourcing Hub of Food & Agriculture" into the future.

## Guidelines
- Setup project on your local computer
- Achieve TODO items one by one
- Mark an item as done in the TODO list
    - [x] Like this
- After completion, please send it in a zip file


## Setup
- Install PIP packages
```
pip install -r requirements.txt
```
- Run server
```
python manage.py runserver
```
- Now that the server’s running, visit http://127.0.0.1:8000/polls/ with your Web browser


## TODO
1.  [x] Raise 404 if no matching question
    * `polls/templates/polls/index.html`
        * Add fake question link
2.  [x] Show only questions that are published and not yet closed
    * `polls/models.py`
        * Add `closed_at` filed into Question class
    * `polls/serializers.py`
        * Add `closed_at` filed
    * `polls/views.py`
        * IndexView.get_queryset()
            * add filter to get only questions that `closed_at` is after timezone.now()
3.  [x] Enable to comment on question
    * `polls/models.py`
        * Add `Comment` class
    *  `polls/admin.py`
        * Add `Comment`
    * `polls/forms.py`
        * Add CommentForm class
    * `polls/urls.py`
        * Add path comment
    * `polls/views.py`
        * Add comment()
    * `polls/templates/polls/detail.html`
        * Print comments and comment form
4.  [x] Enable to comment on comment
    * `polls/models.py`
        * Add `parent` field into `Comment` class
    * `polls/views.py`
        * Add logic to handle `parent` field into comment()
    * `polls/templates/polls/detail.html`
        * Print reply comments and reply comment form
5.  [x] Enable to suggest new choice for question
    * `polls/forms.py`
        * Add ChoiceForm class
    * `polls/urls.py`
        * Add path choice
    * `polls/views.py`
        * Add choice()
    * `polls/templates/polls/detail.html`
        * Add suggest new choice form
6.  [x] Limit the number of choices that can be suggested on one question
    * `polls/apps.py`
        * Add signal import into ready method
    * `polls/__init__.py`
        * Add default_app_config
    * `polls/signals.py`
        * Add logic to check how many choices that question has.
          if the count is over than 10, throw ValueError.        
    * `polls/views.py`
        * Add try-catch on `choice()`
    * `polls/templates/polls/detail.html`
        * Don't show suggest new choice form when number of choices is over than 10.
7.  [x] Extends `Question.closed_at` by one day, when new choice is suggested for that question
    - Requirements:
        - Use Django signal/receiver system
    * `polls/signals.py`
    * Add extend_closed_at().
        * if the question has closed_at, extends `closed_at` by one day.
8.  [x] In `/polls/`, fetch only 5 questions through REST API
    * This task has already been set in `polls/views.py`. I'm confused if I didn't understand the task.
9.  [x] Handle race condition on handling "vote" action
    * `polls/views.py`
        * Add `F()` to increment `vote`
10. [x] Implement login system
    * Add app 'users'
    * `hamji/urls.py`
        * Add path 'django.contrib.auth.urls', 'users.urls'
    * `hamji/settings.py`
        * Add INSTALLED_APPS
        * Add LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL to '/polls/'
    * `polls/templates/polls/detail.html`
        * Add login, logout, signup link
    * Add templates `users/templates/registration/login.html`,`users/templates/registration/signup.html`
    * `users/views.py`
        * Add SignUpView class
    * `users/urls.py`
        * Add path signup 
    
11. [ ] Implement system that a question creator can approve suggested choices
12. [ ] Implement global search for questions and choices

