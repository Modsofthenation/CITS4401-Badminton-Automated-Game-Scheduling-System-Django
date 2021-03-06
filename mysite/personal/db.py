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

    def get_teamTable_decent():
        team = models.Team.objects.all().order_by("-leaderboard_position")
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
        Sql.get_common_availbility_for_players(4,5)
        return game_sorted

    def get_latest_game(request):
        game = models.Game.objects.latest('date')
        print(game)
        return game

    """
       Retrieve availibilities for current user
    """
    def get_user_availbility(request):
        player_instance = User.objects.get(pk = request.user.id)
        availability = models.Availability.objects.filter(player = player_instance).values('availability')
        availList = []
        for avail in availability:
            availList.append(avail["availability"].date())

        return availList

    """
       Retrieve the availibilties for player id matching p1_id 
       Retrieve the avalibilities for player id matching p2_ide

       Find and return a common set of availbilities amongst players
       Based on assumption where a player is a availble for the whole day
    """
    def get_common_availbility_for_players(p1_id, p2_id):
        player1_instance = User.objects.get(pk = p1_id)
        player2_instance = User.objects.get(pk = p2_id)

        availabilityP1 = models.Availability.objects.filter(player = player1_instance).values('availability')
        availabilityP2 = models.Availability.objects.filter(player = player2_instance).values('availability')

        common_avail = []
        for availP1 in availabilityP1:
            for availP2 in availabilityP2:
                dateP1 = availP1["availability"].date()
                dateP2 = availP2["availability"].date()
                if dateP1 == dateP2:
                    common_avail.append(dateP1)

        return common_avail

    """
       Get common availbilities between teams given there ids
    """
    def get_common_availbility_for_teams(t1_id, t2_id):
        team1_object = models.Team.objects.get(id = t1_id)
        team2_object = models.Team.objects.get(id = t2_id) 

        team1_common_avail = Sql.get_common_availbility_for_players(team1_object.player1.id, team1_object.player2.id)
        team2_common_avail = Sql.get_common_availbility_for_players(team2_object.player1.id, team2_object.player2.id)

        game_common_avail = []
        for availT1 in team1_common_avail:
            for availT2 in team2_common_avail:
                if availT1 == availT2:
                    game_common_avail.append(availT1)

        return game_common_avail

    def schedule(week):
        if week == False:
            print("Week is odd - Play team above - Top Team doesn't Play")
        else:
            print("Week is odd - Play team below - Bottom Team doesn't Play")

        teams = Sql.get_teamTable_decent()

        numberTeams = 0
        team1_id = -1
        team2_id = -1
        for index, team in enumerate(teams):
            if week == False:
                if index == 0:
                    None
                else:
                    if numberTeams == 0:
                        team1_id = team.id
                    elif numberTeams == 1:
                        team2_id = team.id
                    numberTeams = numberTeams + 1
                    if numberTeams == 2:
                        commonSet = Sql.get_common_availbility_for_teams(team1_id, team2_id)
                        print("Common set",commonSet)
                        numberTeams = 0
                    print(index, team.id, team.total_wins, team.leaderboard_position)     
            else:
                if index == len(teams)-1:
                    None
                else:
                    print(index, team.id)

            
            


        return None



class Other:
	def get_date_time():
		return timezone.now()

 



	
