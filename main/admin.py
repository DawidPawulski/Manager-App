from django.contrib import admin
from main.models import Players, Clubs, Leagues, Matches, Manager, Goals, Assists, YellowCards, RedCards, \
    ManOfTheMatch, FirstEleven, BenchPlayers, User

# Register your models here.
#  Root
#  root123456


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('name', 'club')


@admin.register(Clubs)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ('club_name',)


@admin.register(Leagues)
class LeaguesAdmin(admin.ModelAdmin):
    list_display = ('league_name',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('club', )


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id',)


