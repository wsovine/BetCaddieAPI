from django.db import models


class FantasyDataLeagueHierarchy(models.Model):
    TeamID = models.IntegerField(primary_key=True)
    Key = models.CharField(max_length=120)
    Active = models.BooleanField()
    School = models.CharField(max_length=120)
    Name = models.CharField(max_length=120)
    StadiumID = models.IntegerField()
    ApRank = models.IntegerField()
    Wins = models.IntegerField()
    Losses = models.IntegerField()
    ConferenceWins = models.IntegerField()
    ConferenceLosses = models.IntegerField()
    TeamLogoUrl = models.URLField()
    ConferenceID = models.IntegerField()
    Conference = models.CharField(max_length=120)
    ShortDisplayName = models.CharField(max_length=120)
    RankWeek = models.IntegerField()
    RankSeason = models.IntegerField()
    RankSeasonType = models.IntegerField()


class FantasyDataGames(models.Model):
    GameID = models.IntegerField(primary_key=True)
    Season = models.IntegerField()
    SeasonType = models.IntegerField()
    Week = models.IntegerField()
    Status = models.CharField(max_length=120)
    Day = models.DateField()
    DateTime = models.DateTimeField()
    AwayTeam = models.CharField(max_length=120)
    HomeTeam = models.CharField(max_length=120)
    AwayTeamID = models.ForeignKey(FantasyDataLeagueHierarchy, on_delete=models.DO_NOTHING)
    HomeTeamID = models.ForeignKey(FantasyDataLeagueHierarchy, on_delete=models.DO_NOTHING)
    AwayTeamName = models.CharField(max_length=120)
    HomeTeamName = models.CharField(max_length=120)
    AwayTeamScore = models.IntegerField()
    HomeTeamScore = models.IntegerField()
    PointSpread = models.IntegerField()
    OverUnder = models.IntegerField()
    AwayTeamMoneyLine = models.IntegerField()
    HomeTeamMoneyLine = models.IntegerField()
    StadiumID = models.IntegerField()
    Title = models.CharField(max_length=120)
    HomeRotationNumber = models.BigIntegerField()
    AwayRotationNumber = models.BigIntegerField()
    NeutralVenue = models.BooleanField()
    AwayPointSpreadPayout = models.IntegerField()
    HomePointSpreadPayout = models.IntegerField()
    OverPayout = models.IntegerField()
    UnderPayout = models.IntegerField()
    Periods = models.JSONField()
    Stadium_StadiumID = models.IntegerField()
    Stadium_Active = models.BooleanField()
    Stadium_Name = models.CharField(max_length=120)
    Stadium_Dome = models.BooleanField()
    Stadium_City = models.CharField(max_length=120)
    Stadium_State = models.CharField(max_length=2)
    Stadium_GeoLat = models.FloatField()
    Stadium_GeoLong = models.FloatField()


class TeamMappings(models.Model):
    fd_team_id = models.IntegerField()
    fd_team_key = models.ForeignKey(FantasyDataLeagueHierarchy, on_delete=models.SET_NULL, null=True)
    fo_team = models.CharField(max_length=120)
    cfbd_team_id = models.IntegerField()

