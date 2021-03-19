from django.contrib import admin

from .models import Choice, Question, Tag

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class TagsInLine(admin.TabularInline):
    model = Tag
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fields = ["publicationDate", "questionText", "points"]
    inlines = [ChoiceInLine, TagsInLine]
    list_display = ("questionText", "publicationDate", "was_published_recently")
    list_filter = ["publicationDate"]
    search_fields = ["questionText"]

admin.site.register(Question, QuestionAdmin)
# Register your models here.
