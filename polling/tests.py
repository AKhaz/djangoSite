import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

class QuestionModelTests(TestCase):
    def testWasPublishedRecentlyWithFutureQuestion(self):
        """If the publication date is set in the future, this test will
        make sure it is not listed as 'published recently' """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publicationDate=time)
        self.assertIs(future_question.was_published_recently(), False)

def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(publicationDate=time)
    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(publicationDate=time)
    self.assertIs(recent_question.was_published_recently(), True)

    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_question(questionText, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(questionText=questionText, publicationDate=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polling:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latestQuestions'], [])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(questionText='Future question.', days=5)
        url = reverse('polling:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(questionText='Past Question.', days=-5)
        url = reverse('polling:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.questionText)
