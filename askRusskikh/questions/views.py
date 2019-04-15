from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Tag, Like, Profile
from .forms import *
from django.db.models.aggregates import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login as login_auth, authenticate, logout
from django.contrib import auth
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def get_page(objects, page_size, page_number):
    paginator = Paginator(objects, page_size)
    try:
        result = paginator.page(page_number)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result

def get_best_members():
    return Profile.objects.order_by('-raiting')[:5]


def get_popular_tags():
    return Tag.objects.annotate(col_questions=Count('question')).order_by('-col_questions')[:16]


def questions(request):
    questions = get_page(Question.manager.all_new(), 3,
                         request.GET.get('page') or 1)
    return render(request, 'question_list.html', {'questions': questions,
                                                  'members': get_best_members(),
                                                  'popular_tags': get_popular_tags()})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=int(question_id))
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                print("Not auth")
                return HttpResponseRedirect(request.GET.get('login', '/login'))
            a_id = form.save(question, request.user)
            return HttpResponseRedirect(request.GET.get('answer', '/' + str(question_id) + '/' '#' + str(a_id)))

    answers = Answer.manager.filter(question=question)
    form = AnswerForm(request.POST)
    return render(request, 'question_detail.html', {'question_detail': question,
                                                    'answers': answers,
                                                    'best_members': get_best_members(),
                                                    'popular_tags': get_popular_tags(),
                                                    'form' : form,
                                                    'members' : get_best_members()
                                                    })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.GET.get('continue', '/'))


def settings(request):
    return render(request, 'settings.html', {'members': get_best_members(),
                                             'popular_tags': get_popular_tags()})


def hot_questions(request):
    questions = get_page(Question.manager.all_rate(), 3,
                         int(request.GET.get('page', 1)))
    return render(request, 'hot_questions.html', {'questions': questions,
                                                  'members': get_best_members(),
                                                  'popular_tags': get_popular_tags()})


def tag(request, tag_id):
    tag_name = get_object_or_404(Tag, pk=int(tag_id))
    questions = get_page(Question.manager.all_questions_by_tag(tag_name), 3,
                         int(request.GET.get('page', 1)))
    return render(request, 'tag.html', {'questions': questions,
                                        'tag_name': tag_name,
                                        'members': get_best_members(),
                                        'popular_tags': get_popular_tags()})


def new_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                print("Not auth")
                return HttpResponseRedirect(request.GET.get('login', '/login'))
            q_id = form.save(request.user)
            return HttpResponseRedirect(request.GET.get('question', '/' + str(q_id)))
        return render(request, 'new_question.html', {'form': form,
                                                     'members': get_best_members(),
                                                     'popular_tags': get_popular_tags()}, )
    return render(request, 'new_question.html', {'form' : QuestionForm(),
                                                 'members': get_best_members(),
                                                 'popular_tags': get_popular_tags()},)

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login_auth(self.request, self.user)
        print("\nlogin\n")
        return super(LoginFormView, self).form_valid(form)


