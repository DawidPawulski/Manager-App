"""ManagerApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', MainView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logut/', LogoutView.as_view(), name='logout_view'),
    path('list_users/', UserListView.as_view(), name="user-list"),
    path('add_user/', UserCreateView.as_view(), name="user-create"),
    path('reset_password/<int:user_id>/', ResetPasswordView.as_view(), name="reset-password"),
    path('user/delete/<int:pk>', ManagerDeleteView.as_view(), name='user_delete'),
    path('clubs/list', ClubsListView.as_view(), name='clubs-list'),
    path('clubs/<int:pk>', ClubDetailView.as_view(), name='club-info'),
    path('clubs/<int:pk>/squad', SquadListView.as_view(), name='squad-list'),
    path('player/<int:pk>', PlayerDetailView.as_view(), name='player-details'),
    path('leagues/', LeaguesListView.as_view(), name='league-list'),
    path('leagues/<int:pk>', LeagueDetailView.as_view(), name='league-details'),
    path('search_player/', PlayerSearchView.as_view(), name='player_search'),
    path('search_club/', ClubSearchView.as_view(), name='club_search'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user-details'),
    path('clubs/<int:pk>/schedule', ScheduleView.as_view(), name='schedule-view'),
    path('schedule/<int:pk>', MatchView.as_view(), name='match-view'),
    path('schedule/<int:pk>/edit', MatchUpdateView.as_view(), name='match-edit-view'),
    path('compose_message/', ComposeMessageView.as_view(), name="compose-message"),
    path('message_sent/', SentMessageView.as_view(), name="sent-message"),
    path('inbox', InboxListView.as_view(), name='inbox-list'),
    path('inbox/<int:pk>', InboxDetailView.as_view(), name='inbox-detail'),
    path('inbox/<int:pk>/delete', MessageDeleteView.as_view(), name='message-delete'),
    path('clubs/<int:pk>/squad/shirts', PlayersShirtNumberUpdateView.as_view(), name='shirt-update'),
]