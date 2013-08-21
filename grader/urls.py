from django.conf.urls import patterns, url
from django.conf import settings

from grader import views

urlpatterns = patterns('',
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^contest-gateway/$', views.ContestGatewayView.as_view(), name='contest-gateway'),
                       
    url(r'^/contest/$', views.ContestGatewayView.as_view(), name='contest'),
    url(r'^contest/(?P<contest>[\w-]+)/$', views.ContestView.as_view(), name='contest-page'),
    url(r'^contest/(?P<contest>[\w-]+)/scoreboard/$', views.ScoreboardView.as_view(), name='scoreboard'),
    url(r'^contest/(?P<contest>[\w-]+)/submit/$', views.SubmitView.as_view(), name='submit'),
    url(r'^contest/(?P<contest>[\w-]+)/problem/(?P<problem>[\w-]+)/$', views.ProblemView.as_view(), name='problem'),

    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
)
