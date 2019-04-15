from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Question, User
from .views import *
from re import match


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=1)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        pass

class SettingsForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5, max_length=128)
    email = forms.EmailField(label='Email', min_length=5, max_length=128)
    nickname = forms.CharField(label='Nickname', min_length=8, max_length=34)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=128)
    avatar = forms.ImageField(required=False, label='Avatar')

class AnswerForm(forms.Form):
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'class': 'w-75', 'rows': '5', 'placeholder': 'Input answer', }),
        max_length=100000
    )

    def save(self, q, user):
        data = self.cleaned_data
        p = Profile()
        p.user = user
        a = Answer.manager.create(text = data.get('text'), question = q, author = p)
        return a.pk

class QuestionForm(forms.Form):
    short = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class':'w-75', 'placeholder': 'Enter question title here', }),
        max_length=100
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'class': 'w-75', 'rows': '13', 'placeholder': 'Add the question description here', }),
        max_length=100000
    )
    tags = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'class': 'w-75', 'placeholder': 'Tag1,Tag2,Tag3'}),
        required=False
    )

    def check_tag(self, tag):
        if (' ' in tag) or ('\n' in tag) or ('\t' in tag):
            raise forms.ValidationError('Tags contain spaces')
        if ('/' in tag) or ('\\' in tag) or ('?' in tag):
            raise forms.ValidationError('You can use only this symbols -+_~&@*%$')
        return tag

    def parse_tags(self, tags):
        self._tag_list = tags.split(',', 10)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        self.parse_tags(tags)
        for tag in self._tag_list:
            self.check_tag(tag)

    def save(self, user):
        data = self.cleaned_data
        p = Profile()
        p.user = user
        q = Question.manager.create(title=data.get('short'), text=data.get('text'),
                                        author=p)
        for tag_text in self._tag_list:
            if tag_text is not None and tag_text != '':
                tag = Tag.objects.get_or_create(name=tag_text)
                q.tag.add(tag[0])
        q.save()
        return q.pk

