# cricket/admin.py

from django.contrib import admin
from .models import Team, Player, Match, PlayerMatchPerformance, Ball
from django.db.models import Sum # Import Sum for aggregation

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'get_total_runs', 'get_total_wickets') # Updated list_display
    list_filter = ('team', 'role')
    search_fields = ('name',)

    # Custom methods to display aggregated runs and wickets in the admin
    # These methods calculate the totals from PlayerMatchPerformance
    def get_total_runs(self, obj):
        # Sums all runs_scored for this player across all their performances
        return obj.performances.aggregate(Sum('runs_scored'))['runs_scored__sum'] or 0
    get_total_runs.short_description = 'Total Runs' # Column header in admin

    def get_total_wickets(self, obj):
        # Sums all wickets_taken for this player across all their performances
        return obj.performances.aggregate(Sum('wickets_taken'))['wickets_taken__sum'] or 0
    get_total_wickets.short_description = 'Total Wickets' # Column header in admin

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'team1', 'team2', 'date', 'venue', 'status', 'winner')
    list_filter = ('status', 'date', 'team1', 'team2')
    search_fields = ('name', 'venue')
    date_hierarchy = 'date' # Adds date drilldown navigation

@admin.register(PlayerMatchPerformance)
class PlayerMatchPerformanceAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'runs_scored', 'wickets_taken', 'balls_faced', 'overs_bowled')
    list_filter = ('player__team', 'match__date') # Filter by player's team and match date
    search_fields = ('player__name', 'match__name')
    raw_id_fields = ('player', 'match') # Use raw_id_fields for FKs to improve performance with many records

@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ('match', 'over', 'batsman', 'bowler', 'runs', 'is_wicket', 'is_wide', 'is_no_ball')
    list_filter = ('match', 'is_wicket', 'is_wide', 'is_no_ball')
    search_fields = ('match__name', 'batsman__name', 'bowler__name', 'commentary')
    raw_id_fields = ('match', 'batsman', 'bowler')
