import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F

from rest_framework import viewsets

from utils.url import restify

from .models import Choice, Question, Comment
from .serializers import QuestionSerializer

from .forms import CommentForm, ChoiceForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        response = requests.get(restify("/questions/"))
        questions = list(filter(lambda x: x['closed_at'] is None or x['closed_at'] >= str(timezone.now()), response.json()))
        questions.sort(key=lambda x: x['pub_date'], reverse=True)
        return questions[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = question.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            if 'parent_id' in request.POST:
                parent_id = int(request.POST['parent_id'])
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    new_comment.parent = parent_obj

            new_comment.question = question
            new_comment.save()
            return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    else:
        comment_form = CommentForm()
    return render(request,
                  'polls/detail.html',
                  {'question': question,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    new_choice = None
    if request.method == 'POST':
        choice_form = ChoiceForm(data=request.POST)
        if choice_form.is_valid():
            new_choice = choice_form.save(commit=False)
            new_choice.question = question
            try:
                new_choice.save()
            except ValueError as e:
                return render(request,
                              "polls/detail.html",
                              {"question": question,
                               "error_message": str(e)})
            return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    else:
        choice_form = ChoiceForm()
    return render(request,
                  'polls/detail.html',
                  {'question': question,
                   'new_choice': new_choice,
                   'choice_form': choice_form})


# API
# ===


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
