import datetime
import operator
from itertools import chain
from . import views, models
from django.views.generic import ListView
from django.db.models import Q
from django.db import connection
from django.utils import timezone
from django.contrib.auth.models import User

class Sql:
    def get_teamTable():
    	team = models.Team.objects.all().order_by("leaderboard_position")
    	return team

    def get_gameTable(request):
    	user_id = request.user.id
    	user_user = request.user
    	# game = models.Game.object.filter(
    	# 	Q(team1.player1.id == user_id) |
    	# 	Q(team1.player2.id == user_id) |
    	# 	Q(team2.player1.id == user_id) |
    	# 	Q(team2.player2.id == user_id),
    	# )
    	# cursor.execute('SELECT id FROM personal_team WHERE player1 = %d OR player2 = %d', [user_id, user_id])
    	game = models.Game.objects.all()
    	#game = models.Game.objects.raw('SELECT * FROM personal_game')
    	return game

    def get_not_played_games(request):
        #count = models.Game.objects.filter(has_been_played = False).count()
        team = models.Team.objects.get(id = request.user.player.team.id)
        #count = models.Game.objects.filter(Q(has_been_played = False), Q(team1 = team) | Q(team2 = team)).count()
        count_team1 = models.Game.objects.filter(Q(has_been_played = False), Q(winning_team = None), Q(team1 = team))
        count_team2 = models.Game.objects.filter(Q(has_been_played = False), Q(winning_team = None), Q(team2 = team))
        count_total = count_team1 | count_team2
        count = count_total.count()
        print(count)
        return count

    def get_games_where_player_involved_have_been_played(request):
        team = models.Team.objects.get(id = request.user.player.team.id)
        game_hp_team1 = models.Game.objects.filter(Q(has_been_played = True), ~Q(winning_team = None), Q(team1 = team))
        game_hp_team2 = models.Game.objects.filter(Q(has_been_played = True), ~Q(winning_team = None), Q(team2 = team))
        game_hp = game_hp_team1 | game_hp_team2
        return game_hp

    def get_games_where_player_involved_not_been_played(request):
        team = models.Team.objects.get(id = request.user.player.team.id)
        #game_np = models.Game.objects.filter(Q(has_been_played = False), Q(team1 = team) | Q(team2 = team))
        game_np1 = models.Game.objects.filter(Q(has_been_played = False), Q(team2 = team))
        game_np2 = models.Game.objects.filter(Q(has_been_played = False), Q(team1 = team))
        game_unsorted = game_np1 | game_np2
        game_sorted = sorted(game_unsorted, key=operator.attrgetter('week'))
        Sql.get_common_availbility_for_players(4)
        return game_sorted

    def get_latest_game(request):
        game = models.Game.objects.latest('date')
        print(game)
        return game

    def get_common_availbility_for_players(p1_id):
        player1_instance = User.objects.get(pk = p1_id)
        #player2_instance = User.objects.get(pk = p2_id)

        availabilityP1 = models.Availability.objects.filter(player = player1_instance).values('availability')

        for value in availabilityP1:
            print(value)

        #print(availabilityP1)
        return None

    def schedule_game():
        return None


class Other:
	def get_date_time():
		return timezone.now()

 



	