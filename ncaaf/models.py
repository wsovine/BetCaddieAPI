from django.db import models


class FantasyDataLeagueHierarchy(models.Model):
    TeamID = models.IntegerField(primary_key=True)
    Key = models.CharField(max_length=120, null=True, blank=True)
    Active = models.BooleanField(null=True, blank=True)
    School = models.CharField(max_length=120, null=True, blank=True)
    Name = models.CharField(max_length=120, null=True, blank=True)
    StadiumID = models.IntegerField(null=True, blank=True)
    ApRank = models.IntegerField(null=True, blank=True)
    Wins = models.IntegerField(null=True, blank=True)
    Losses = models.IntegerField(null=True, blank=True)
    ConferenceWins = models.IntegerField(null=True, blank=True)
    ConferenceLosses = models.IntegerField(null=True, blank=True)
    TeamLogoUrl = models.URLField(null=True, blank=True)
    ConferenceID = models.IntegerField(null=True, blank=True)
    Conference = models.CharField(max_length=120, null=True, blank=True)
    ShortDisplayName = models.CharField(max_length=120, null=True, blank=True)
    RankWeek = models.IntegerField(null=True, blank=True)
    RankSeason = models.IntegerField(null=True, blank=True)
    RankSeasonType = models.IntegerField(null=True, blank=True)


class FantasyDataGames(models.Model):
    GameID = models.IntegerField(primary_key=True)
    Season = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)  # 1=Regular, 2=Pre, 3=Post, 4=Off, 5=AllStar
    Week = models.IntegerField(null=True, blank=True)
    Status = models.CharField(max_length=120, null=True, blank=True)
    Day = models.DateField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    AwayTeam = models.CharField(max_length=120, null=True, blank=True)
    HomeTeam = models.CharField(max_length=120, null=True, blank=True)
    AwayTeamID = models.IntegerField(null=True, blank=True)
    HomeTeamID = models.IntegerField(null=True, blank=True)
    AwayTeamName = models.CharField(max_length=120, null=True, blank=True)
    HomeTeamName = models.CharField(max_length=120, null=True, blank=True)
    AwayTeamScore = models.IntegerField(null=True, blank=True)
    HomeTeamScore = models.IntegerField(null=True, blank=True)
    PointSpread = models.IntegerField(null=True, blank=True)
    OverUnder = models.IntegerField(null=True, blank=True)
    AwayTeamMoneyLine = models.IntegerField(null=True, blank=True)
    HomeTeamMoneyLine = models.IntegerField(null=True, blank=True)
    StadiumID = models.IntegerField(null=True, blank=True)
    Title = models.CharField(max_length=120, null=True, blank=True)
    HomeRotationNumber = models.BigIntegerField(null=True, blank=True)
    AwayRotationNumber = models.BigIntegerField(null=True, blank=True)
    NeutralVenue = models.BooleanField(null=True, blank=True)
    AwayPointSpreadPayout = models.IntegerField(null=True, blank=True)
    HomePointSpreadPayout = models.IntegerField(null=True, blank=True)
    OverPayout = models.IntegerField(null=True, blank=True)
    UnderPayout = models.IntegerField(null=True, blank=True)
    Periods = models.JSONField(null=True, blank=True)
    Stadium_StadiumID = models.IntegerField(null=True, blank=True)
    Stadium_Active = models.BooleanField(null=True, blank=True)
    Stadium_Name = models.CharField(max_length=120)
    Stadium_Dome = models.BooleanField(null=True, blank=True)
    Stadium_City = models.CharField(max_length=120, null=True, blank=True)
    Stadium_State = models.CharField(max_length=2, null=True, blank=True)
    Stadium_GeoLat = models.FloatField(null=True, blank=True)
    Stadium_GeoLong = models.FloatField(null=True, blank=True)


class FootballOutsidersFPlusRatings(models.Model):
    Team = models.CharField(max_length=120, primary_key=True)
    F_plus = models.FloatField()
    OF_plus = models.FloatField()
    DF_plus = models.FloatField()
    FEI = models.FloatField()
    SP_plus = models.FloatField()


class TeamMappings(models.Model):
    fd_team_id = models.ForeignKey(FantasyDataLeagueHierarchy, to_field='TeamID', db_column='fd_team_id',
                                   null=True, blank=True, on_delete=models.DO_NOTHING, related_name='fd_team_id')
    fo_team = models.ForeignKey(FootballOutsidersFPlusRatings, to_field='Team', db_column='fo_team',
                                null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cfbd_team_id = models.IntegerField(null=True, blank=True)


class GameBetCalcs(models.Model):
    game_id = models.OneToOneField(FantasyDataGames, primary_key=True, on_delete=models.CASCADE)
    away_team = models.ForeignKey(FantasyDataLeagueHierarchy, null=True, on_delete=models.CASCADE,
                                  related_name='away_team')
    home_team = models.ForeignKey(FantasyDataLeagueHierarchy, null=True, on_delete=models.CASCADE,
                                  related_name='home_team')
    away_elo_pre = models.IntegerField(null=True)
    home_elo_pre = models.IntegerField(null=True)
    away_elo_prob = models.FloatField(null=True)
    home_elo_prob = models.FloatField(null=True)
    away_elo_post = models.IntegerField(null=True)
    home_elo_post = models.IntegerField(null=True)
    home_hfa_elo_adj = models.IntegerField(null=True)
    away_elo_adj = models.IntegerField(null=True)
    home_elo_adj = models.IntegerField(null=True)
    away_scoring_matchup = models.FloatField(null=True)
    home_scoring_matchup = models.FloatField(null=True)
    away_matchup_elo_adj = models.IntegerField(null=True)
    home_matchup_elo_adj = models.IntegerField(null=True)
