from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polling/index.html"
    context_object_name = "latestQuestions"
    def get_queryset(self):
        return Question.objects.filter(
            publicationDate__lte=timezone.now()
        ).order_by('publicationDate')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polling/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(publicationDate__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polling/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polling/detail.html', {'question' : question, 'error_message' : "No answer was selected."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polling:results', args = (question.id,)))
