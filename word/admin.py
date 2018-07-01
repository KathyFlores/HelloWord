from django.contrib import admin
from .models import UserProfile,Word, WordSet, Example, Paraphrase, Learn, TodayTask, Test

# Register your models here.

admin.site.register(Word)
admin.site.register(WordSet)
admin.site.register(Example)
admin.site.register(Paraphrase)
admin.site.register(UserProfile)
admin.site.register(Learn)
admin.site.register(TodayTask)
admin.site.register(Test)