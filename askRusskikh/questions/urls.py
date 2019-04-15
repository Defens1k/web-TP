from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.questions, name='question_list'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^(?P<question_id>[0-9]+)/$', views.question_detail, name='question_detail'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^hot_questions/$', views.hot_questions, name='hot_questions'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag, name='tag'),
    url(r'^new_question/$', views.new_question, name='new_question'),
    url(r'^logout/', views.logout, name="logout"),
]
