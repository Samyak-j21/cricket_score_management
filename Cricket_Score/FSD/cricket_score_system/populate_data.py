# populate_data.py
# Run this script from Django shell: python manage.py shell
# Then: exec(open('populate_data.py').read())

import os
import django
from django.utils import timezone
from datetime import timedelta

# Set up Django environment if running as a standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricket_score_system.settings')
django.setup()

from cricket.models import Team, Player, Match, PlayerMatchPerformance, Ball

print("Starting data population script for Mavericks and Hurricanes with new player names...")

# --- 1. Create Teams ---
team_mavericks, created = Team.objects.get_or_create(
    name="Mavericks",
    defaults={'country': 'USA', 'logo': None} # Fictional country for these teams
)
if created:
    print(f"Created Team: {team_mavericks.name}")

team_hurricanes, created = Team.objects.get_or_create(
    name="Hurricanes",
    defaults={'country': 'West Indies', 'logo': None} # Fictional country
)
if created:
    print(f"Created Team: {team_hurricanes.name}")

# --- 2. Create Players (Updated Names and expanded lists) ---
# Players for Mavericks (11 players)
players_mavericks_data = [
    {'name': 'Pandey', 'role': 'Batsman'},
    {'name': 'Ajinkya', 'role': 'Batsman'},
    {'name': 'Venkatesh', 'role': 'Batsman'},
    {'name': 'A.Raghuvanshi', 'role': 'Batsman'},
    {'name': 'Quinton', 'role': 'Wicketkeeper'}, # Assuming Quinton is the wicketkeeper
    {'name': 'Harshit', 'role': 'Bowler'},
    {'name': 'Chakaravarthy', 'role': 'Bowler'},
    {'name': 'Mayank', 'role': 'Bowler'},
    {'name': 'Vaibhav', 'role': 'Bowler'}, # Mavericks Vaibhav
    {'name': 'R.singh', 'role': 'All-Rounder'},
    {'name': 'Anukul Roy', 'role': 'All-Rounder'},
]
mavericks_players = []
for p_data in players_mavericks_data:
    player, created = Player.objects.get_or_create(
        name=p_data['name'],
        team=team_mavericks,
        defaults={'role': p_data['role']}
    )
    mavericks_players.append(player)
    if created:
        print(f"Created Player: {player.name} ({player.team.name})")

# Players for Hurricanes (11 players)
players_hurricanes_data = [
    {'name': 'Aman', 'role': 'Batsman'}, # Assuming Aman is a batsman
    {'name': 'A.Joshi', 'role': 'Batsman'},
    {'name': 'Riyan', 'role': 'Batsman'},
    {'name': 'Vaibhav', 'role': 'Batsman'}, # Hurricanes Vaibhav
    {'name': 'Yashasvi', 'role': 'Batsman'},
    {'name': 'Tom Blocker', 'role': 'Wicketkeeper'}, # Keeping one original name for a distinct role
    {'name': 'S.Singh', 'role': 'Bowler'},
    {'name': 'Maheesh', 'role': 'Bowler'},
    {'name': 'S.Sharma', 'role': 'Bowler'},
    {'name': 'S.Sarkar', 'role': 'All-Rounder'},
    {'name': 'Dhruv', 'role': 'All-Rounder'},
]
hurricanes_players = []
for p_data in players_hurricanes_data:
    player, created = Player.objects.get_or_create(
        name=p_data['name'],
        team=team_hurricanes,
        defaults={'role': p_data['role']}
    )
    hurricanes_players.append(player)
    if created:
        print(f"Created Player: {player.name} ({player.team.name})")

# --- 3. Create Sample Matches (as in previous version) ---
# Match 1: Mavericks vs Hurricanes (Completed, Mavericks won)
match_date_1 = timezone.now() - timedelta(days=7)
match_venue_1 = "Arena Oval"
match_name_1 = "League Cup Final"

sample_match_1, created_1 = Match.objects.get_or_create(
    name=match_name_1,
    team1=team_mavericks,
    team2=team_hurricanes,
    defaults={
        'date': match_date_1,
        'venue': match_venue_1,
        'status': 'Completed',
        'winner': team_mavericks
    }
)
if created_1:
    print(f"Created Match: {sample_match_1.name}")

# Match 2: Hurricanes vs Mavericks (Completed, Hurricanes won)
match_date_2 = timezone.now() - timedelta(days=15)
match_venue_2 = "Coastal Stadium"
match_name_2 = "Championship Semifinal"

sample_match_2, created_2 = Match.objects.get_or_create(
    name=match_name_2,
    team1=team_hurricanes,
    team2=team_mavericks,
    defaults={
        'date': match_date_2,
        'venue': match_venue_2,
        'status': 'Completed',
        'winner': team_hurricanes
    }
)
if created_2:
    print(f"Created Match: {sample_match_2.name}")

# Match 3: Upcoming Match (Mavericks vs Hurricanes)
match_date_3 = timezone.now() + timedelta(days=3)
match_venue_3 = "Central Ground"
match_name_3 = "Friendly Warm-up"

sample_match_3, created_3 = Match.objects.get_or_create(
    name=match_name_3,
    team1=team_mavericks,
    team2=team_hurricanes,
    defaults={
        'date': match_date_3,
        'venue': match_venue_3,
        'status': 'Upcoming',
        'winner': None
    }
)
if created_3:
    print(f"Created Match: {sample_match_3.name}")


# --- 4. Populate Ball-by-Ball Data ---
# Select specific players from the NEW lists for ball data
# Mavericks players (using indices after re-mapping based on roles)
mavericks_batsman_1 = mavericks_players[0]  # Pandey
mavericks_batsman_2 = mavericks_players[1]  # Ajinkya
mavericks_bowler_1 = mavericks_players[5]   # Harshit
mavericks_bowler_2 = mavericks_players[6]   # Chakaravarthy
mavericks_allrounder = mavericks_players[9] # R.singh (for a single in an over)

# Hurricanes players
hurricanes_batsman_1 = hurricanes_players[0]  # Aman
hurricanes_batsman_2 = hurricanes_players[1]  # A.Joshi
hurricanes_bowler_1 = hurricanes_players[6]   # S.Singh
hurricanes_bowler_2 = hurricanes_players[7]   # Maheesh

balls_data_1 = [
    # Over 1 (Mavericks batting, Hurricanes bowling)
    {'over': 0.1, 'batsman': mavericks_batsman_1, 'bowler': hurricanes_bowler_1, 'runs': 1, 'is_wicket': False, 'commentary': 'Pandey starts with a quick single.'},
    {'over': 0.2, 'batsman': mavericks_batsman_2, 'bowler': hurricanes_bowler_1, 'runs': 0, 'is_wicket': False, 'commentary': 'Dot ball by S.Singh. Good line.'},
    {'over': 0.3, 'batsman': mavericks_batsman_2, 'bowler': hurricanes_bowler_1, 'runs': 4, 'is_wicket': False, 'commentary': 'FOUR! Ajinkya punches it through covers.'},
    {'over': 0.4, 'batsman': mavericks_batsman_2, 'bowler': hurricanes_bowler_1, 'runs': 2, 'is_wicket': False, 'commentary': 'Two runs taken. Good running.'},
    {'over': 0.5, 'batsman': mavericks_batsman_2, 'bowler': hurricanes_bowler_1, 'runs': 0, 'is_wicket': True, 'commentary': 'WICKET! Ajinkya is caught! Brilliant catch!'},
    {'over': 0.6, 'batsman': mavericks_players[2], 'bowler': hurricanes_bowler_1, 'runs': 1, 'is_wicket': False, 'commentary': 'Venkatesh gets off the mark with a single.'},

    # Over 2 (Mavericks batting, Hurricanes bowling)
    {'over': 1.1, 'batsman': mavericks_batsman_1, 'bowler': hurricanes_bowler_2, 'runs': 6, 'is_wicket': False, 'commentary': 'SIX! Pandey pulls it over square leg!'},
    {'over': 1.2, 'batsman': mavericks_batsman_1, 'bowler': hurricanes_bowler_2, 'runs': 0, 'is_wicket': False, 'commentary': 'Dot ball. Tightly bowled.'},
    {'over': 1.3, 'batsman': mavericks_batsman_1, 'bowler': hurricanes_bowler_2, 'runs': 4, 'is_wicket': False, 'commentary': 'FOUR! Elegant drive from Pandey.'},
    {'over': 1.4, 'batsman': mavericks_batsman_1, 'bowler': hurricanes_bowler_2, 'runs': 0, 'is_wicket': True, 'commentary': 'BOWLED! Maheesh gets his first! Pandey gone!'},
    {'over': 1.5, 'batsman': mavericks_allrounder, 'bowler': hurricanes_bowler_2, 'runs': 1, 'is_wicket': False, 'commentary': 'R.singh takes a single.'},
    {'over': 1.6, 'batsman': mavericks_players[4], 'bowler': hurricanes_bowler_2, 'runs': 2, 'is_wicket': False, 'commentary': 'Quinton gets a couple to end the over.'},
]

balls_data_2 = [
    # Over 1 (Hurricanes batting, Mavericks bowling)
    {'over': 0.1, 'batsman': hurricanes_batsman_1, 'bowler': mavericks_bowler_1, 'runs': 0, 'is_wicket': False, 'commentary': 'Aman defends the first ball.'},
    {'over': 0.2, 'batsman': hurricanes_batsman_1, 'bowler': mavericks_bowler_1, 'runs': 4, 'is_wicket': False, 'commentary': 'FOUR! Aman finds the gap!'},
    {'over': 0.3, 'batsman': hurricanes_batsman_1, 'bowler': mavericks_bowler_1, 'runs': 1, 'is_wicket': False, 'commentary': 'Quick single for Aman.'},
    {'over': 0.4, 'batsman': hurricanes_batsman_2, 'bowler': mavericks_bowler_1, 'runs': 0, 'is_wicket': False, 'commentary': 'A.Joshi defends stoutly.'},
    {'over': 0.5, 'batsman': hurricanes_batsman_2, 'bowler': mavericks_bowler_1, 'runs': 6, 'is_wicket': False, 'commentary': 'SIX! A.Joshi goes aerial!'},
    {'over': 0.6, 'batsman': hurricanes_batsman_2, 'bowler': mavericks_bowler_1, 'runs': 0, 'is_wicket': False, 'commentary': 'Dot ball to end the over.'},
]


# Populate balls for sample_match_1
for b_data in balls_data_1:
    Ball.objects.get_or_create(
        match=sample_match_1,
        over=b_data['over'],
        batsman=b_data['batsman'],
        bowler=b_data['bowler'],
        defaults={
            'runs': b_data['runs'],
            'is_wicket': b_data['is_wicket'],
            'commentary': b_data['commentary'],
            'is_wide': False, 'is_no_ball': False
        }
    )
print(f"Populated balls for {sample_match_1.name}")

# Populate balls for sample_match_2
for b_data in balls_data_2:
    Ball.objects.get_or_create(
        match=sample_match_2,
        over=b_data['over'],
        batsman=b_data['batsman'],
        bowler=b_data['bowler'],
        defaults={
            'runs': b_data['runs'],
            'is_wicket': b_data['is_wicket'],
            'commentary': b_data['commentary'],
            'is_wide': False, 'is_no_ball': False
        }
    )
print(f"Populated balls for {sample_match_2.name}")

# --- 5. Populate PlayerMatchPerformance Data ---
# Adjust based on the runs/wickets from the balls above for realism
performance_data = [
    # For sample_match_1 (Mavericks batting first)
    {'player': mavericks_players[0], 'match': sample_match_1, 'runs_scored': 11, 'wickets_taken': 0, 'balls_faced': 5, 'overs_bowled': 0}, # Pandey
    {'player': mavericks_players[1], 'match': sample_match_1, 'runs_scored': 7, 'wickets_taken': 0, 'balls_faced': 4, 'overs_bowled': 0}, # Ajinkya
    {'player': mavericks_players[5], 'match': sample_match_1, 'runs_scored': 0, 'wickets_taken': 0, 'balls_faced': 0, 'overs_bowled': 1}, # Harshit (bowled)
    {'player': mavericks_players[9], 'match': sample_match_1, 'runs_scored': 1, 'wickets_taken': 0, 'balls_faced': 1, 'overs_bowled': 0}, # R.singh
    {'player': hurricanes_players[6], 'match': sample_match_1, 'runs_scored': 0, 'wickets_taken': 1, 'balls_faced': 0, 'overs_bowled': 1}, # S.Singh (1 wicket)
    {'player': hurricanes_players[7], 'match': sample_match_1, 'runs_scored': 0, 'wickets_taken': 1, 'balls_faced': 0, 'overs_bowled': 1}, # Maheesh (1 wicket)

    # For sample_match_2 (Hurricanes batting first)
    {'player': hurricanes_players[0], 'match': sample_match_2, 'runs_scored': 5, 'wickets_taken': 0, 'balls_faced': 3, 'overs_bowled': 0}, # Aman
    {'player': hurricanes_players[1], 'match': sample_match_2, 'runs_scored': 6, 'wickets_taken': 0, 'balls_faced': 2, 'overs_bowled': 0}, # A.Joshi
    {'player': mavericks_players[5], 'match': sample_match_2, 'runs_scored': 0, 'wickets_taken': 0, 'balls_faced': 0, 'overs_bowled': 1}, # Harshit (bowled in this match)
]

for p_data in performance_data:
    PlayerMatchPerformance.objects.get_or_create(
        player=p_data['player'],
        match=p_data['match'],
        defaults={
            'runs_scored': p_data['runs_scored'],
            'wickets_taken': p_data['wickets_taken'],
            'balls_faced': p_data['balls_faced'],
            'overs_bowled': p_data['overs_bowled']
        }
    )
print("Populated player match performances.")

print("Data population script finished.")
