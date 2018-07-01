from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.utils import timezone
# Create your models here.
'''
单词集封面上传路径
'''
def wordset_cover_path(instance, filename):
    return 'wordset_cover/set_{0}/{1}'.format(instance.name, filename)

FAMILIAR_LEVEL_CHOICE = (
    (0,'不认识'),
    (1,'见过'),
    (2,'知道意思'),
    (3,'初步掌握'),
    (4,'完全掌握'),
    (5,'熟记')
)


class UserProfile(AbstractUser):
    tasks = models.ManyToManyField('Word',through='Learn',blank=True, null=True)
    word_sets = models.ManyToManyField('WordSet', blank=True, null=True)
    word_per_day = models.PositiveIntegerField(default=50)
    my_words = models.ManyToManyField('Word', related_name='my_words',blank=True, null=True)
    learning_word_set = models.ForeignKey('WordSet', related_name='learning_word_set', on_delete=models.SET_NULL,blank=True, null=True)
    def __str__(self):
        return self.username
    def learn_progress(self):
        total = self.task.all().count()
        learned = self.task.filter(familiar_level=5)
        return (1 - learned/total)
    def add_to_my_words(self, word):
        if word not in self.my_words.all():
            self.my_words.add(word)
            self.save()
            try:
                Learn.objects.create(user=self,word=word)
            except:
                None
    def delete_from_my_words(self, word):
        if word in self.my_words.all():
            self.my_words.remove(word)
            self.save()
            
            if self.learning_word_set and word not in self.learning_word_set.words.all():
                Learn.objects.get(user=self,word=word).delete()
    def update_learning_wordset(self, new_set):
        old_set = self.learning_word_set
        mywords = self.my_words.all()
        new_set_words = new_set.words.all()

        if old_set:
            old_set_words = old_set.words.all()
            for word in old_set_words:
                if ((not mywords) or (mywords and word not in mywords)) and (word not in new_set_words):
                    Learn.objects.get(user=self,word=word).delete()
            for word in new_set_words:
                print(word)
                print(new_set_words)
                print(old_set_words)
                print(((not mywords) or (mywords and word not in mywords)) and (word not in old_set_words))
                if ((not mywords) or (mywords and word not in mywords)) and (word not in old_set_words):
                    try:
                        Learn.objects.create(user=self,word=word)
                    except:
                        None
        else:
            for word in new_set_words:
                if (not mywords) or (mywords and word not in mywords):
                    print(mywords)
                    Learn.objects.create(user=self,word=word)
        self.learning_word_set = new_set
        self.save()
    def get_today_tasks(self):
        date_ = date.today()
        try:
            words = Word.objects.filter(todaytask__user=self,todaytask__date=date_)
            if words.count() == 0:
                remain = self.word_per_day
                words = Word.objects.filter(learn__user=self,learn__familiar_level__lt=5).exclude(user=self,word__todaytask__date=date).order_by('?')[:remain]
                if words:
                    for word in words:
                        TodayTask.objects.create(user=self,word=word,date=date_)
                words = Word.objects.filter(todaytask__user=self,todaytask__date=date_)
        except:
            words = Word.objects.filter(learn__user=self,learn__familiar_level__lt=5).order_by('?')[:self.word_per_day]
            for word in words:
                TodayTask.objects.create(user=self,word=word,date=date_)
        print(words)
        return words

    def word_num_today(self):
        words = self.get_today_tasks()
        return words.count()
    def get_today_master_count(self):
        words = self.get_today_tasks()
        count = 0
        for word in words:
            try:
                Learn.objects.get(user=self,word=word,familiar_level=5)
                count += 1
            except:
                None
        return count

    def get_task_count(self):  
        return Learn.objects.filter(user=self).count()
    def get_master_word_count(self):
        return Learn.objects.filter(user=self,familiar_level=5).count()
    def get_learning_word_count(self):
        return Learn.objects.filter(user=self,familiar_level__lt=5,familiar_level__gt=0).count()
        
    def get_word_familiar_level(self, word):
        return Learn.objects.get(user=self,word=word).familiar_level
    def is_complete_today_task(self):
        words = self.get_today_tasks()
        count = 0
        for word in words:
            try:
                Learn.objects.get(user=self,word=word,familiar_level=5)
                count += 1
            except:
                None
        if count == self.word_num_today():
            return True
        else:
            return False
    

class Word(models.Model):
    text = models.CharField(max_length=50, unique=True, blank=False)
    def __str__(self):
        return self.text
    def get_paraphrases(self):
        paraphrases = Paraphrase.objects.filter(word=self)
        ret = ''
        for paraphrase in paraphrases:
            ret += paraphrase.meaning+'；'
        return ret[:-1]
class Example(models.Model):
    sentence = models.CharField(max_length = 500)
    translation = models.CharField(max_length = 500)
    def __str__(self):
        return self.sentence

class Paraphrase(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning = models.CharField(max_length = 50)
    examples = models.ManyToManyField(Example, null=True, blank=True)
    def __str__(self):
        return self.word.text + self.meaning

class WordSet(models.Model):
    name = models.CharField(max_length=30, default='')
    cover = models.ImageField(upload_to=wordset_cover_path, blank=True)
    words = models.ManyToManyField(Word)
    def num(self):
        return self.words.all().count()
    def __str__(self):
        return self.name

class TodayTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    date = models.DateField()
    class Meta:
        unique_together = ('user', 'word', 'date')
    def __str__(self):
        return self.user.username+'/'+self.word.text+'/'+str(self.date)
    
class Learn(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    familiar_level = models.IntegerField(
        default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ], 
        choices=FAMILIAR_LEVEL_CHOICE
    )

    class Meta:
        unique_together = ('user', 'word')

    def unknow(self):
        self.familiar_level = 0
        self.save()

    def too_simple(self):
        self.familiar_level = 5
        self.save()

    def know(self):
        if (self.familiar_level<5 and self.familiar_level>=0):
            self.familiar_level += 1
            self.save()

class Test(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    words = models.ManyToManyField(Word)
    grade = models.IntegerField(default=0)
    complete = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + '/' +str(self.grade)
    def is_complete(self):
        return self.complete==50
