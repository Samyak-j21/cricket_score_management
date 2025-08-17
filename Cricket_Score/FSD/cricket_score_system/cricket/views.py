# cricket/views.py

from django.shortcuts import render, get_object_or_404
from .models import Team, Player, Match, PlayerMatchPerformance, Ball
from django.db.models import Sum
from django.utils import timezone

def home(request):
    """
    Renders the home page of the cricket score system,
    displaying upcoming and recently completed matches.
    """
    upcoming_matches = Match.objects.filter(
        date__gte=timezone.now().date(),
        status__in=['Upcoming', 'Live']
    ).order_by('date')[:5]

    completed_matches = Match.objects.filter(
        date__lt=timezone.now().date(),
        status='Completed'
    ).order_by('-date')[:5]

    context = {
        'upcoming_matches': upcoming_matches,
        'completed_matches': completed_matches,
    }
    return render(request, 'cricket/home.html', context)

def team_list(request):
    """
    Fetches all teams from the database and displays them.
    """
    teams = Team.objects.all().order_by('name')
    context = {
        'teams': teams
    }
    return render(request, 'cricket/team_list.html', context)

def team_detail(request, team_id):
    """
    Displays the details of a specific team, including its players.
    """
    team = get_object_or_404(Team, pk=team_id)
    players = team.players.all().order_by('name')

    context = {
        'team': team,
        'players': players,
    }
    return render(request, 'cricket/team_detail.html', context)

def match_detail(request, match_id):
    """
    Displays the details of a specific match.
    """
    match = get_object_or_404(Match, pk=match_id)
    context = {
        'match': match
    }
    return render(request, 'cricket/match_detail.html', context)

def player_stats(request, player_id):
    """
    Displays detailed statistics for a specific player, including a performance graph
    and recent match performances.
    """
    player = get_object_or_404(Player, pk=player_id)

    total_runs = 0
    wickets_taken = 0
    player_stats_data = {'labels': [], 'runs': [], 'wickets': []}
    player_matches = []

    recent_performances = PlayerMatchPerformance.objects.filter(player=player).order_by('-match__date')[:5]

    for p in recent_performances:
        total_runs += p.runs_scored
        wickets_taken += p.wickets_taken
        match_label = p.match.name if p.match.name and p.match.name != "Unnamed Match" else f"{p.match.team1.name} vs {p.match.team2.name}"
        player_stats_data['labels'].append(match_label)
        player_stats_data['runs'].append(p.runs_scored)
        player_stats_data['wickets'].append(p.wickets_taken)
        player_matches.append({
            'match_name': match_label,
            'runs_scored': p.runs_scored,
            'wickets_taken': p.wickets_taken,
            'match_date': p.match.date
        })

    player_stats_data['labels'].reverse()
    player_stats_data['runs'].reverse()
    player_stats_data['wickets'].reverse()
    player_matches.reverse()

    return render(request, 'cricket/player_stats.html', {
        'player': player,
        'total_runs': total_runs,
        'wickets_taken': wickets_taken,
        'player_stats_data': player_stats_data,
        'player_matches': player_matches,
    })

def player_full_match_history(request, player_id):
    """
    Displays the complete match history for a specific player.
    """
    player = get_object_or_404(Player, pk=player_id)

    all_player_matches = PlayerMatchPerformance.objects.filter(player=player).order_by('-match__date')

    context = {
        'player': player,
        'all_player_matches': all_player_matches,
    }
    return render(request, 'cricket/player_full_match_history.html', context)

def all_matches(request):
    """
    Displays a list of all matches, both upcoming and completed.
    """
    all_cricket_matches = Match.objects.all().order_by('-date')
    context = {
        'all_cricket_matches': all_cricket_matches
    }
    return render(request, 'cricket/all_matches.html', context)
