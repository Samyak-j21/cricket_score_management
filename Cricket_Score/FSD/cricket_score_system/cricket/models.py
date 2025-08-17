# cricket/models.py

from django.db import models

class Team(models.Model):
    """
    Represents a cricket team.
    """
    name = models.CharField(max_length=100, unique=True) # Ensure team names are unique
    country = models.CharField(max_length=100, blank=True, null=True) # Added country back for context
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # Records when the team was added

    def __str__(self):
        return self.name

class Player(models.Model):
    """
    Represents a cricket player.
    Removed aggregate stats (runs, wickets, matches_played) from here.
    These will be derived from PlayerMatchPerformance entries.
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(
        max_length=50,
        choices=[
            ('Batsman', 'Batsman'),
            ('Bowler', 'Bowler'),
            ('All-Rounder', 'All-Rounder'),
            ('Wicketkeeper', 'Wicketkeeper'), # Using 'Wicketkeeper' for consistency
        ],
        default='Batsman'
    )
    date_of_birth = models.DateField(null=True, blank=True) # Added date_of_birth for player detail
    # NEW FIELD: Player profile image
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.team.name})"

class Match(models.Model):
    """
    Represents a cricket match between two teams.
    Added a 'name' field for better identification.
    """
    name = models.CharField(max_length=255, default="Unnamed Match") # Useful for display, e.g., "India vs Australia - Final"
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    date = models.DateTimeField() # Stores date and time of the match
    venue = models.CharField(max_length=200) # Increased max_length for venue
    status = models.CharField(
        max_length=20,
        choices=[
            ('Upcoming', 'Upcoming'),
            ('Live', 'Live'),
            ('Completed', 'Completed')
        ],
        default='Upcoming' # Sensible default status
    )
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')

    def __str__(self):
        # Using the name if available, otherwise defaulting to teams and date
        if self.name and self.name != "Unnamed Match":
            return self.name
        return f"{self.team1.name} vs {self.team2.name} - {self.date.strftime('%Y-%m-%d')}" # Format date for string representation

class PlayerMatchPerformance(models.Model):
    """
    Records a player's individual performance in a specific match.
    This model is crucial for detailed match history and statistics.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='performances')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_performances')
    runs_scored = models.IntegerField(default=0)
    wickets_taken = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0) # Added for more detail
    overs_bowled = models.FloatField(default=0.0) # Added for more detail
    # Add other performance metrics like catches, stumpings, run_outs etc.

    class Meta:
        # Ensures that a player has only one performance record per match
        unique_together = ('player', 'match')
        # Default ordering for querying performances, e.g., by most recent match
        ordering = ['-match__date']

    def __str__(self):
        return f"{self.player.name}'s performance in {self.match.name or str(self.match)}"


class Ball(models.Model):
    """
    Represents a single ball bowled in a match, storing granular details.
    """
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='balls')
    over = models.FloatField() # e.g., 1.1 for 1st ball of 2nd over
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batsman_balls')
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowler_balls')
    runs = models.IntegerField(default=0) # Runs scored on this specific ball (excluding extras)
    is_wicket = models.BooleanField(default=False)
    is_wide = models.BooleanField(default=False)
    is_no_ball = models.BooleanField(default=False)
    commentary = models.TextField(blank=True) # Text commentary for the ball

    def __str__(self):
        return f"Match: {self.match.name}, Over: {self.over}, Batsman: {self.batsman.name}, Bowler: {self.bowler.name}"
