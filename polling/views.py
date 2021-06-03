from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polling/index.html"
    context_object_name = "latestQuestions"

    def checkLogIn(self, request):
        # Double checks if the user is signed in, returns bool
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
                return HttpResponseRedirect(reverse('polling:detail', args = (id,)))
            if "Logout" in request.POST.keys():
                # Logs out the user
                logout(request)
                # Obviously sets the check for login to false, since the user just signed out
                userLoggedIn = False
                questions = self.get_queryset()
                return render(request, "polling/index.html", {"latestQuestions": questions, "userLoggedIn": userLoggedIn})
        if "Username" in request.POST.keys():
            print(request.POST.keys())
            if "Login" in request.POST.keys():
                user = authenticate(username = request.POST['Username'], password = request.POST['Password'])
                if user is not None:
                    #print("Logged in successfully")
                    login(request, user)
                else:
                    questions = self.get_queryset()
                    return render(request, 'polling/index.html', {'latestQuestions' : questions, "userLoggedIn": userLoggedIn, 'error_message' : "Cannot find user with login info."})
            if "Register" in request.POST.keys():
                #Makes new user entry and saves it
                newUser = User(username = request.POST['Username'], password = make_password(request.POST['Password']))
                newUser.save()
                login(request, newUser)
            # If the user is logged in, variable is true
            userLoggedIn = self.checkLogIn(request)
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
        userLoggedIn = request.user.is_authenticated
        # print("QUESTIONS", questions)
        return render(request, "polling/index.html", {"latestQuestions": questions, "userLoggedIn": userLoggedIn})


    def get_queryset(self, tag = None):
        if tag == None:
            return Question.objects.filter(
                publicationDate__lte=timezone.now()
            ).order_by('publicationDate')[:10]
        else:
            #if there IS a tag, sort using the tag text
            return Question.objects.filter(
                publicationDate__lte=timezone.now()
            ).filter(tag__tagText=tag).order_by('publicationDate')[:10]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polling/detail.html'

    def get_queryset(self):
        # Excludes any questions that aren't published yet.
        return Question.objects.filter(publicationDate__lte=timezone.now())

class PostView(View):
    template_name = 'polling/createPost.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        # # Create a new question based on the keys in the request (which come from the template)
        newPost = Question(questionText = request.POST['BodyText'], publicationDate = timezone.now())
        newPost.save()
        # # loop through all option/choice keys and create corresponding choices to question
        # print(request.POST.keys())
        for key in request.POST.keys():
            #Create a new option for every key that has the word "option" (keys are made by template) and sent through form
            if "Option" in key:
                newOption = Choice(question = newPost, choiceText = request.POST[key])
                # print(newOption)
                newOption.save()
            # print(newPost)
        #sends the user to the detail view/template of the newly created question/post
        return HttpResponseRedirect(reverse('polling:detail', args = (newPost.id,)))


    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(publicationDate__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polling/results.html'

def vote(request, question_id):
    # Get the question ID
    question = get_object_or_404(Question, pk = question_id)
    try:
        # Gets the selected choice
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Returns with error message if no answer is selected
        return render(request, 'polling/detail.html', {'question' : question, 'error_message' : "No answer was selected."})
    else:
        # Otherwise, add one to the votes and send the user to the results screen
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polling:results', args = (question.id,)))
