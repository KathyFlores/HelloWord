from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from word.models import UserProfile, WordSet, Example, Paraphrase, Word, Learn, Test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
import re
from datetime import date
# Create your views here.
today = date.today()
def index(request):
    word_sets = WordSet.objects.all()
    return render(request, 'word/index.html', {'word_sets':word_sets})

def word(request):
    if request.user.is_authenticated():
        request.user.get_today_tasks()
        return render(request, 'word/word.html', {})
    else:
        return render(request, 'word/pleaselogin.html', {})
def learn(request):
    user = request.user
    if user.is_authenticated():
        words = user.get_today_tasks()       
        return render(request, 'word/learn.html', {'words':words})
    else:
        return render(request, 'word/pleaselogin.html', {})
def progress(request):
    if request.user.is_authenticated():
        return render(request, "word/progress.html",{})
    else:
        return render(request, 'word/pleaselogin.html', {})   
def test_entry(request):
    if request.user.is_authenticated():
        return render(request, "word/test_entry.html",{})
    else:
        return render(request, 'word/pleaselogin.html', {}) 
def wordsets(request):
    word_sets = WordSet.objects.all()
    return render(request, "word/wordsets.html", {'word_sets':word_sets})

def mywords(request):
    if request.user.is_authenticated():
        user = request.user
        words = user.my_words.all()
        return render(request, 'word/mywords.html',{'words':words})
    else:
        return render(request, 'word/pleaselogin.html', {}) 
def test(request):
    if request.user.is_authenticated():
        try:
            test = Test.objects.get(user=request.user,complete__lt=50)
        except:
            test = Test.objects.create(user=request.user)
            words_ = Word.objects.all().order_by('?')[:50]
            for word in words_:
                test.words.add(word)
            test.save()
        words = test.words.all()
        user = request.user

        if request.POST:
            if request.POST['oper'] == 'choose':
                res={'code':0,'msg':'','complete':0, 'grade':0}
                print(request.POST)
                word=Word.objects.get(text=request.POST['word'])
                paraphrase=request.POST['paraphrase']
                if paraphrase == word.get_paraphrases():
                    res['code']=200
                    res['msg']='correct'
                    test.grade += 1
                else:
                    res['code']=200
                    res['msg']='wrong'
                test.complete+=1
                test.save()
                res['complete']=test.is_complete()
                res['grade']=test.grade * 2
                return JsonResponse(res)
            else:
                res = {
                    'code':0,
                    'word':'',
                    'word_id': 0,
                    'paraphrase':[],
                    'confuse_para':[],
                    'right_para':'',
                }
                word_id = int(request.POST['word_id']) 
                while test.complete > word_id:
                    word_id = (word_id + 1) % 50
                    word = words[word_id]
                
                res['word_id']=word_id
                word = words[word_id]
                res['word']=word.text
                res['right_para']=word.get_paraphrases()
                paraphrases = Paraphrase.objects.filter(word=word)
                for paraphrase in paraphrases:
                    para = {'meaning':'','example':[]}    
                    para['meaning']=paraphrase.meaning
                    examples = paraphrase.examples.all()
                    for example in examples:
                        exa = {'sentence':'','translation':''}
                        exa['sentence']=example.sentence
                        exa['translation']=example.translation
                        para['example'].append(exa)
                    res['paraphrase'].append(para)
                    
                confuse_words = Word.objects.all().exclude(text=word.text).order_by('?')[:3]
                for confuse_word in confuse_words:
                    res['confuse_para'].append(confuse_word.get_paraphrases())
                res['code']=200

                return JsonResponse(res)
        return render(request, "word/test.html", {'test':test})
    else:
        return render(request, 'word/pleaselogin.html', {})
def review(request):
    if request.user.is_authenticated():
        return render(request, 'word/review.html',{})
    else:
        return render(request, 'word/pleaselogin.html', {})

def word_per_day(request):
    if request.user.is_authenticated():
        if request.POST:
            user = request.user
            user.word_per_day = int(request.POST['word_per_day'])
            user.save()
            res = {'code':200,'msg':'修改成功！'}
            print(res)
            return JsonResponse(res)
        else:
            return render(request, 'word/word_per_day.html',{})
    else:
        return render(request, 'word/pleaselogin.html', {})
  

def my_login(request):
    res = {'msg':'','code':0}
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            res['msg']='登录成功'
            res['code']=200
            return JsonResponse(res)
        else:
            res['msg']='账号无效'
            res['code']=500
            # 返回'无效账号'页面
            return JsonResponse(res)
    else:
        # 返回'无效登录'错误页面
        res['msg']='账号不存在'
        res['code']=500
        return JsonResponse(res)

def my_validate_email(email):  
    from django.core.validators import validate_email  
    from django.core.exceptions import ValidationError  
    try:  
        validate_email(email)  
        return True  
    except ValidationError:  
        return False

def my_signup(request):
    res = {'msg':'','code':0}
    username_pattern = re.compile(r'^[\w\.\+\-@]+$')
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    print(request.POST)
    if len(username) < 6:
        res['code']=500
        res['msg']='用户名长度少于6位'
    elif re.match(username_pattern, username) is None:
        res['code']=500
        res['msg']='用户名格式错误'
    elif UserProfile.objects.filter(username=username).count() > 0:
        res['code']=500
        res['msg']='用户名已经被占用'
    elif UserProfile.objects.filter(email=email).count() > 0:   
        res['code']=500
        res['msg']='该邮箱已被注册'
    elif len(password1) < 6:
        res['code']=500
        res['msg']='密码少于6位'
    elif len(password2) < 6:
        res['code']=500
        res['msg']='密码少于6位'
    elif password1 != password2:
        res['code']=500
        res['msg']='两次输入密码不一致'
    elif my_validate_email(email) == False:
        res['code']=500
        res['msg']='邮箱格式错误'
    else:
        user = authenticate(username = username, password = password1)
        if user:
            res['code']=500
            res['msg']='用户已存在'
        else:
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')
                user0 = authenticate(username=user.username, password=raw_password)
                login(request, user0)
                res['code']=200
                res['msg']='注册成功'
    return JsonResponse(res)

def my_logout(request):
    logout(request)
    return redirect('index')

def get_a_word(request):
    res = {
        'code':0,
        'word':'',
        'word_id': 0,
        'star':0,
        'paraphrase':[],
        'confuse_para':[],
        'right_para':'',
        'complete':0
    }
    user = request.user
    words = user.get_today_tasks()
    word_id = (int(request.GET.get('word_id')) ) % user.word_num_today()
    res['word_id']=word_id
    word = words[word_id]
    while user.get_word_familiar_level(word) == 5:
        word_id = (word_id + 1) % user.word_num_today()
        word = words[word_id]
        if user.is_complete_today_task():
            return JsonResponse({
                'code':200,
                'word':'',
                'word_id': 0,
                'star':0,
                'paraphrase':[],
                'confuse_para':[],
                'right_para':'',
                'complete':1
            }) 

    res['word']=word.text
    mywords = user.my_words.all()
    if mywords and word in mywords:
        res['star']=1
    res['right_para']=word.get_paraphrases()
    paraphrases = Paraphrase.objects.filter(word=word)
    for paraphrase in paraphrases:
        para = {'meaning':'','example':[]}    
        para['meaning']=paraphrase.meaning
        examples = paraphrase.examples.all()
        for example in examples:
            exa = {'sentence':'','translation':''}
            exa['sentence']=example.sentence
            exa['translation']=example.translation
            para['example'].append(exa)
        res['paraphrase'].append(para)

    confuse_words = Word.objects.all().exclude(text=word.text).order_by('?')[:3]
    for confuse_word in confuse_words:
        res['confuse_para'].append(confuse_word.get_paraphrases())
    res['code']=200
    
    return JsonResponse(res)

def get_a_master_word(request):
    res = {
        'code':0,
        'word':'',
        'word_id': 0,
        'star': 0,
        'paraphrase':[],
        'confuse_para':[],
        'right_para':'',
        'complete':0
    }
    user = request.user
    word_id = int(request.GET.get('word_id')) 
    res['word_id']=word_id
    words = Word.objects.filter(todaytask__user=user,todaytask__date=today,learn__familiar_level__gte=5)
    if word_id == words.count():
        return JsonResponse({
            'code':200,
            'word':'',
            'word_id': 0,
            'star': 0,
            'paraphrase':[],
            'confuse_para':[],
            'right_para':'',
            'complete':1
        }) 
      
    word = words[word_id]
    res['word']=word.text
    mywords = user.my_words.all()
    if mywords and word in mywords:
        res['star']=1
    res['right_para']=word.get_paraphrases()
    paraphrases = Paraphrase.objects.filter(word=word)
    for paraphrase in paraphrases:
        para = {'meaning':'','example':[]}    
        para['meaning']=paraphrase.meaning
        examples = paraphrase.examples.all()
        for example in examples:
            exa = {'sentence':'','translation':''}
            exa['sentence']=example.sentence
            exa['translation']=example.translation
            para['example'].append(exa)
        res['paraphrase'].append(para)
        
    confuse_words = Word.objects.all().exclude(text=word.text).order_by('?')[:3]
    for confuse_word in confuse_words:
        res['confuse_para'].append(confuse_word.get_paraphrases())
    res['code']=200
    
    return JsonResponse(res)
def unknow(request):
    res={'code':0,'msg':''}
    word=Word.objects.get(text=request.POST['word'])
    user = request.user
    learn = Le
    arn.objects.get(user=user,word=word)
    learn.unknow()
    res['code']=200
    return JsonResponse(res)

def star(request):
    res={'code':0,'star':1}
    word=Word.objects.get(text=request.POST['word'])
    user = request.user
    mywords = user.my_words.all()
    print(mywords)
    print(word)
    print(mywords and word in mywords)
    if mywords and word in mywords:
        user.delete_from_my_words(word)
        res['star']=0
    else:
        user.add_to_my_words(word)
        res['star']=1
    res['code']=200
    
    return JsonResponse(res)

def choose(request):
    res={'code':0,'msg':'','familiar_level':''}
    word=Word.objects.get(text=request.POST['word'])
    paraphrase=request.POST['paraphrase']
    user = request.user
    learn = Learn.objects.get(user=user,word=word)
    print(paraphrase)
    print(word.get_paraphrases())
    if paraphrase == word.get_paraphrases():
        learn.know()
        res['code']=200
        res['msg']='correct'
        res['familiar_level']=learn.familiar_level
    else:
        res['code']=200
        res['msg']='wrong'
        res['familiar_level']=learn.familiar_level

    return JsonResponse(res)

def set_wordset(request):
    res={'code':0,'msg':''}
    wordset_id = request.POST['wordset_id']
    user = request.user
    wordset = WordSet.objects.get(pk=wordset_id)
    
    user.update_learning_wordset(wordset)
    
    if user.learning_word_set == wordset:
        res['code']=200
        res['msg']='设置成功'
    else:
        res['code']=500
        res['msg']='设置失败'
    user.get_today_tasks()
    return JsonResponse(res)