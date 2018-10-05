from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

# Create your models here.
from django.urls import reverse

POSITION_CHOICES = [
    (0, 'Goalkeeper'),
    (1, 'Defender'),
    (2, 'Midfielder'),
    (3, 'Forward'),
]
# RATING_CHOICES = (
#     (1, 'Poor'),
#     (2, 'Average'),
#     (3, 'Good'),
#     (4, 'Very Good'),
#     (5, 'Excellent')
# )


class Leagues(models.Model):
    league_name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    level = models.IntegerField()

    def __str__(self):
        return self.league_name

    class Meta:
        verbose_name = "league"
        verbose_name_plural = "leagues"


class Clubs(models.Model):
    club_name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    stadium_name = models.CharField(max_length=64)
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE)

    def __str__(self):
        return self.club_name

    class Meta:
        verbose_name = "club"
        verbose_name_plural = "clubs"


class Players(models.Model):
    name = models.CharField(max_length=128)
    position = models.IntegerField(choices=POSITION_CHOICES)
    injury = models.BooleanField(default=False)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=64)
    height = models.IntegerField()
    date_of_birth = models.DateField()
    shirt_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "player"
        verbose_name_plural = "players"


class Manager(models.Model):
    my_user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.OneToOneField(Clubs, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.my_user.first_name, self.my_user.last_name)

    objects = UserManager()

    class Meta:
        verbose_name = "manager"
        verbose_name_plural = "managers"
        db_table = u'manager'


class Matches(models.Model):
    home_team = models.ManyToManyField(Clubs, related_name='HomeTeam')
    away_team = models.ManyToManyField(Clubs, related_name='AwayTeam')
    home_team_score = models.IntegerField(null=True, blank=True)
    away_team_score = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE)
    possession_home_team = models.FloatField()
    possession_away_team = models.FloatField()
    shots_on_target_home_team = models.IntegerField()
    shots_on_target_away_team = models.IntegerField()
    all_shots_home_team = models.IntegerField()
    all_shots_away_team = models.IntegerField()
    corners_home_team = models.IntegerField()
    corners_away_team = models.IntegerField()
    offsides_home_team = models.IntegerField()
    offsides_away_team = models.IntegerField()
    yellow_cards_home_team = models.IntegerField()
    yellow_cards_away_team = models.IntegerField()
    red_cards_home_team = models.IntegerField()
    red_cards_away_team = models.IntegerField()
    fouls_conceded_home_team = models.IntegerField()
    fouls_conceded_away_team = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.home_team, self.away_team)

    class Meta:
        verbose_name = "match"
        verbose_name_plural = "matches"

    def get_absolute_url(self):
        return reverse('match-view', kwargs={'pk': self.pk})




class Goals(models.Model):
    goals = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class Assists(models.Model):
    assists = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class YellowCards(models.Model):
    yellow_cards = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class RedCards(models.Model):
    red_cards = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class ManOfTheMatch(models.Model):
    motm = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class FirstEleven(models.Model):
    match_played = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class BenchPlayers(models.Model):
    matches_from_the_bench = models.IntegerField()
    player = models.ManyToManyField(Players)
    match = models.ManyToManyField(Matches)


class Message(models.Model):
    recipient = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='Recipient')
    subject = models.CharField(max_length=256)
    content = models.TextField()
    sender = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='Sender')
    date_sent = models.DateTimeField(auto_now_add=True)