from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import context
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from main.models import *
from main.forms import *
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


class UserListView(generic.ListView):
    model = User
    template_name = 'main/user_list.html'


class UserCreateView(View):

    def get(self, request):
        return TemplateResponse(request, 'main/user_form.html', {
            'form': UserForm()
        })

    def post(self, request):
        form = UserForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password2'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                #club=form.cleaned_data['club'],
            )

            Manager.objects.create(
                my_user=u,
                club=form.cleaned_data['club'],
            )

            return redirect('login_view')
        return TemplateResponse(request, 'main/user_form.html', ctx)


class ResetPasswordView(PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request, user_id):
        return TemplateResponse(request, 'main/reset_password_form.html', {
            'form': ResetPasswordForm()
        })

    def post(self, request, user_id):
        form = ResetPasswordForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(form.cleaned_data['new_password2'])
            return redirect('login')
        return TemplateResponse(request, 'main/reset_password_form.html', ctx)


class LoginView(View):

    def get(self, request):
        return TemplateResponse(request, 'main/login_form.html', {
            'form': LoginForm()
        })

    def post(self, request):
        form = LoginForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            login(request, form.user)
            return redirect(to='/list_users/')
        return TemplateResponse(request, 'main/login_form.html', ctx)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(to='login_view')


class ManagerDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user-list')


class ClubsListView(View):
    #  model = Clubs

    def get(self, request):
        return render(request, 'main/clubs_list.html', {"form": ClubListForm()})

    def post(self, request):
        form = ClubListForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            search_res = Clubs.objects.filter(league=phrase)
            res = search_res.order_by('club_name')
            ctx = {
                'results': res,
            }
        return render(request, 'main/clubs_list.html', ctx)


class ClubDetailView(View):
    def get(self, request, pk):
        club = Clubs.objects.get(pk=pk)
        manager = Manager.objects.filter(club=club)
        ctx = {
            'club_details': club,
            'manager': manager,
        }
        return render(request, 'main/club_info.html', ctx)


class SquadListView(View):

    def get(self, request, pk):
        club = Clubs.objects.get(pk=pk)
        all_players = Players.objects.filter(club=club)
        player = all_players.order_by('position', 'name')
        goals = Goals.objects.filter(player=player)
        assist = Assists.objects.filter(player=player)
        yellow_cards = YellowCards.objects.filter(player=player)
        red_cards = RedCards.objects.filter(player=player)
        appearance = FirstEleven.objects.filter(player=player)
        from_the_bench = BenchPlayers.objects.filter(player=player)
        motm = ManOfTheMatch.objects.filter(player=player)

        ctx = {
            'club': club,
            'players': player,
            'goals': goals,
            'assists': assist,
            'yellow_cards': yellow_cards,
            'red_cards': red_cards,
            'appearance': appearance,
            'bench': from_the_bench,
            'motm': motm,
        }
        return render(request, 'main/squad.html', ctx)


class PlayerDetailView(View):
    def get(self, request, pk):
        player = Players.objects.get(pk=pk)
        goals = Goals.objects.filter(player=player)
        assist = Assists.objects.filter(player=player)
        yellow_cards = YellowCards.objects.filter(player=player)
        red_cards = RedCards.objects.filter(player=player)
        appearance = FirstEleven.objects.filter(player=player)
        from_the_bench = BenchPlayers.objects.filter(player=player)
        motm = ManOfTheMatch.objects.filter(player=player)
        #  shirt_num = PlayerShirtNumber.objects.filter(player__pk__in=player)

        ctx = {
            'player': player,
            'goals': goals,
            'assists': assist,
            'yellow_cards': yellow_cards,
            'red_cards': red_cards,
            'appearance': appearance,
            'bench': from_the_bench,
            'motm': motm,
            #  'shirt': shirt_num,
        }
        return render(request, 'main/player_view.html', ctx)


class LeaguesListView(View):
    def get(self, request):
        leagues = Leagues.objects.all()
        ctx = {
            'leagues': leagues,
        }
        return render(request, 'main/leagues_list.html', ctx)


class LeagueDetailView(View):
    def get(self, request, pk):
        league = Leagues.objects.get(pk=pk)
        clubs = Clubs.objects.filter(league=league)
        club = clubs.order_by('club_name')
        manager = Manager.objects.filter(club=club)
        ctx = {
            'league': league,
            'club_details': club,
            'manager': manager,
        }
        return render(request, 'main/league_details_view.html', ctx)


class PlayerSearchView(View):

    def get(self, request):
        return render(request, 'main/search_player.html', {"form": PlayerSearchForm()})

    def post(self, request):
        form = PlayerSearchForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            players = Players.objects.filter(name__icontains=phrase)
            ctx = {
                'results': players,
            }
        return render(request, 'main/search_player.html', ctx)


class ClubSearchView(View):

    def get(self, request):
        return render(request, 'main/search_club.html', {"form": ClubSearchForm()})

    def post(self, request):
        form = ClubSearchForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            club = Clubs.objects.filter(club_name__icontains=phrase)
            ctx = {
                'results': club,
            }
        return render(request, 'main/search_club.html', ctx)


class UserDetailView(View):
    def get(self, request, pk):
        manager = Manager.objects.get(my_user=pk)
        ctx = {
            'manager': manager,
        }
        return render(request, 'main/user_details.html', ctx)


class ScheduleView(View):
    def get(self, request, pk):
        club = Clubs.objects.get(pk=pk)
        matches = Matches.objects.filter(Q(home_team=club) | Q(away_team=club))
        ctx = {
            'matches': matches,
            'club': club,
        }
        return render(request, 'main/schedule-list.html', ctx)


class ComposeMessageView(View):

    def get(self, request):
        return TemplateResponse(request, 'main/message_form.html', {
            'form': MessageForm()
        })

    def post(self, request):
        form = MessageForm(data=request.POST)
        current_user = request.user
        manager = Manager.objects.get(my_user=current_user)
        ctx = {'form': form}
        if form.is_valid():
            Message.objects.create(sender=manager,
                                   recipient=form.cleaned_data['recipient'],
                                   content=form.cleaned_data['content'],
                                   subject=form.cleaned_data['subject'])
            return redirect(to='/message_sent/')
        return TemplateResponse(request, 'main/message_form.html', ctx)


class SentMessageView(View):
    def get(self, request):
        return TemplateResponse(request, 'main/message_sent.html')


class InboxListView(View):
    def get(self, request):
        current_user = request.user
        manager = Manager.objects.get(my_user=current_user)
        message = Message.objects.filter(recipient=manager)
        ctx = {
            'manager': manager,
            'messages': message,
        }
        return render(request, 'main/inbox_list.html', ctx)


class InboxDetailView(View):
    def get(self, request, pk):
        message = Message.objects.get(pk=pk)
        ctx = {
            'messages': message,
        }
        return render(request, 'main/inbox_detail.html', ctx)


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('inbox-list')


class PlayersShirtNumberUpdateView(View):

    def get(self, request, pk):
        club = Clubs.objects.get(pk=pk)
        all_players = Players.objects.filter(club=club)
        player = all_players.order_by('position', 'name')
        form = PlayersShirtNumberForm(player)
        form.fields["player"].queryset = player
        #  shirt_num = PlayerShirtNumber.objects.filter(player__in=player)
        ctx = {'form': form,
               'player_list': player,
               'club': club,
               #  'shirt': shirt_num,
               }
        return render(request, 'main/player_shirt_number_update.html', ctx)

    def post(self, request, pk):

        club = Clubs.objects.get(pk=pk)
        all_players = Players.objects.filter(club=club)
        player = all_players.order_by('position', 'name')
        form = PlayersShirtNumberForm(event=player, data=request.POST)
        form.fields["player"].queryset = player
        ctx = {'form': form,
               'player_list': player,
               'club': club,
               }
        if form.is_valid():
            player = request.POST['player']
            play = Players.objects.filter(id=player)
            play.update(shirt_number=form.cleaned_data['number'],)
            obj = '/clubs/{}/squad'.format(pk)
            return redirect(to=obj)
        return render(request, 'main/player_shirt_number_update.html', ctx)


class MatchView(View):
    def get(self, request, pk):
        match = Matches.objects.get(pk=pk)
        ctx = {
            'match': match,
        }
        return render(request, 'main/match_view.html', ctx)


class MatchUpdateView(UpdateView):
    model = Matches
    fields = ['home_team_score', 'away_team_score', 'possession_home_team', 'possession_away_team',
              'shots_on_target_home_team', 'shots_on_target_away_team', 'all_shots_home_team', 'all_shots_away_team',
              'corners_home_team', 'corners_away_team', 'offsides_home_team', 'offsides_away_team',
              'yellow_cards_home_team', 'yellow_cards_away_team', 'red_cards_home_team', 'red_cards_away_team',
              'fouls_conceded_home_team', 'fouls_conceded_away_team']
    template_name_suffix = '_update'


class MainView(View):
    pass
