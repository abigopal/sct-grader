from django.conf.urls import patterns, url
from grader import views

urlpatterns = patterns('',
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^contest-gateway/$', views.ContestGateway.as_view(), name='contest-gateway'),

    url(r'^contest/(?P<contest>[\w-]+)/$', views.ContestPage.as_view(), name='contest'),
    url(r'^contest/(?P<contest>[\w-]+)/problem/(?P<problem>[\w-]+)/$', views.ProblemPage.as_view(), name='problem'),

)
