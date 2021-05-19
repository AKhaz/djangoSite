from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from .models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polling/index.html"
    context_object_name = "latestQuestions"

    def checkLogIn(self, request):
        return request.user.is_authenticated

    def post(self, request):
        userLoggedIn = self.checkLogIn(request)
        if userLoggedIn == True:
            if "Like" in request.POST.keys():
                #Gets id of question using hidden input tag name
                id = request.POST.get("questionID")
                #Makes a variable corresponding with the question's ID
                question = get_object_or_404(Question, pk = id)
                #Adds one like to the question and saves
                question.likes += 1
                question.save()
                questions = self.get_queryset()
                return HttpResponseRedirect(reverse('polling:detail', args = (id)))
        if "Username" in request.POST.keys():
            print(request.POST.keys())
            if "Login" in request.POST.keys():
                user = authenticate(username = request.POST['Username'], password = request.POST['Password'])
                if user is not None:
                    print("Logged in successfully")
                    login(request, user)
                else:
                    print("User not found")
                    print(user)
                    pass
            if "Register" in request.POST.keys():
                newUser = User(username = request.POST['Username'], password = make_password(request.POST['Password']))
                newUser.save()
                login(request, newUser)
            # If the user is logged in, variable is true
            userLoggedIn = self.checkLogIn(request)
            print(userLoggedIn)
            questions = self.get_queryset()
            return render(request, "polling/index.html", {"latestQuestions": questions, "userLoggedIn": userLoggedIn})


    def get(self, request):
        if "Tag" in request.GET.keys():
            # print(request.GET)
            # Finds tag value
            tag = request.GET.get("Tag")
            questions = self.get_queryset(tag)
        else:
            questions = self.get_queryset()
        # print("QUESTIONS", questions)
        return render(request, "polling/index.html", {"latestQuestions": questions})


    def get_queryset(self, tag = None):
        if tag == None:
            return Question.objects.filter(
                publicationDate__lte=timezone.now()
            ).order_by('publicationDate')[:10]
        else:
            return Question.objects.filter(
                publicationDate__lte=timezone.now()
            ).filter(tag__tagText=tag).order_by('publicationDate')[:10]

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

def userPage(request, id):
    user = User.objects.filter(id=id)
    userPosts = Question.objects.filter(userPosted = id)
    latestPosts = userPosts.order_by('-publicationDate')[:5]
