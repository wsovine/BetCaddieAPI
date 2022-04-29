from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ncaaf.calcs import elo_win_probability, new_ratings, implied_probability, bayes_prob, odds_profit_mult


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
    AwayTeam = models.ForeignKey(FantasyDataLeagueHierarchy, on_delete=models.DO_NOTHING, related_name='away_team',
                                 db_constraint=False)
    HomeTeam = models.ForeignKey(FantasyDataLeagueHierarchy, on_delete=models.DO_NOTHING, related_name='home_team',
                                 db_constraint=False)
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

    def create_game_bet_calcs(self):
        # If the mapping does not exist then it is likely because the teams are not in FBS
        # we won't calculate these
        try:
            away_team_mapping = TeamMappings.objects.get(fd_team=self.AwayTeam)
        except TeamMappings.DoesNotExist:
            return
        try:
            home_team_mapping = TeamMappings.objects.get(fd_team=self.HomeTeam)
        except TeamMappings.DoesNotExist:
            return

        away_team, away_created = TeamCalculatedRatings.objects.get_or_create(mapping=away_team_mapping,
                                                                              defaults={'elo': 1500})
        home_team, home_created = TeamCalculatedRatings.objects.get_or_create(mapping=home_team_mapping,
                                                                              defaults={'elo': 1500})

        game, game_created = CeloBetCalcs.objects.get_or_create(fd_game=self)
        game.away_elo_pre = away_team.elo
        game.home_elo_pre = home_team.elo

        # PRE SCORING ADJUSTMENTS
        # Move team halfway to 1500 if it's a new season
        if self.Week == 1 and self.SeasonType == 1:
            game.away_elo_pre = (game.away_elo_pre + 1500) / 2
            game.home_elo_pre = (game.home_elo_pre + 1500) / 2

        # Factor in home field advantage
        game.home_hfa_elo_adj = 46 if not self.NeutralVenue else 0

        # Matchup difference
        away_of_plus = away_team_mapping.fo_team.OF_plus
        home_of_plus = home_team_mapping.fo_team.OF_plus
        away_df_plus = away_team_mapping.fo_team.DF_plus
        home_df_plus = home_team_mapping.fo_team.DF_plus

        game.away_scoring_matchup = away_of_plus - home_df_plus
        game.away_matchup_elo_adj = game.away_scoring_matchup * 200
        game.home_scoring_matchup = home_of_plus - away_df_plus
        game.home_matchup_elo_adj = game.home_scoring_matchup * 200

        # Add up all the adjustments
        game.away_elo_adj = game.away_elo_pre + game.away_matchup_elo_adj
        game.home_elo_adj = game.home_elo_pre + game.home_hfa_elo_adj + game.home_matchup_elo_adj

        # Fetch the win probability for each team
        game.away_elo_prob = elo_win_probability(game.away_elo_adj, game.home_elo_adj)
        game.home_elo_prob = elo_win_probability(game.home_elo_adj, game.away_elo_adj)

        # Calculate new elos
        if self.Status in ('Final', 'F/OT') and (self.AwayTeamScore and self.HomeTeamScore):
            # What is the margin of victory?
            mov = abs(self.AwayTeamScore - self.HomeTeamScore)
            # Away team wins
            if self.AwayTeamScore > self.HomeTeamScore:
                away_elo_post, home_elo_post = new_ratings(game.away_elo_pre, game.home_elo_pre, drawn=False, mov=mov)
            # Home team wins
            else:
                home_elo_post, away_elo_post = new_ratings(game.home_elo_pre, game.away_elo_pre, drawn=False, mov=mov)
        # Tie (not possible, game most likely hasn't been played)
        else:
            away_elo_post, home_elo_post = game.away_elo_pre, game.home_elo_pre

        game.away_elo_post = away_elo_post
        game.home_elo_post = home_elo_post

        away_team.elo = away_elo_post
        home_team.elo = home_elo_post

        if self.AwayTeamMoneyLine:
            game.away_ml_implied_prob = implied_probability(self.AwayTeamMoneyLine)
        elif self.PointSpread and self.PointSpread > 0:
            game.away_ml_implied_prob = 1
        else:
            game.away_ml_implied_prob = 0

        if self.HomeTeamMoneyLine:
            game.home_ml_implied_prob = implied_probability(self.HomeTeamMoneyLine)
        elif self.PointSpread and self.PointSpread < 0:
            game.home_ml_implied_prob = 1
        else:
            game.home_ml_implied_prob = 0

        game.ml_overround = (game.away_ml_implied_prob + game.home_ml_implied_prob) - 1
        game.ml_vig = 1 - (1 / ((game.ml_overround * 100) + 100)) * 100 if game.ml_overround != -1 else 0

        game.away_ml_prob_less_vig = game.away_ml_implied_prob - (game.ml_vig / 2) if self.AwayTeamMoneyLine \
            else game.away_ml_implied_prob
        game.home_ml_prob_less_vig = game.home_ml_implied_prob - (game.ml_vig / 2) if self.HomeTeamMoneyLine \
            else game.home_ml_implied_prob

        game.away_ml_bayes_prob = bayes_prob(game.away_ml_prob_less_vig, game.away_elo_prob, game.away_ml_prob_less_vig) \
            if self.AwayTeamMoneyLine else game.away_ml_prob_less_vig
        game.home_ml_bayes_prob = bayes_prob(game.home_ml_prob_less_vig, game.home_elo_prob, game.home_ml_prob_less_vig) \
            if self.HomeTeamMoneyLine else game.home_ml_prob_less_vig

        game.away_ml_diff = game.away_ml_bayes_prob - game.away_ml_implied_prob
        game.home_ml_diff = game.home_ml_bayes_prob - game.home_ml_implied_prob

        game.away_ml_er = (game.away_ml_bayes_prob * odds_profit_mult(self.AwayTeamMoneyLine)) - (1 - game.away_ml_bayes_prob) if self.AwayTeamMoneyLine else -1
        game.home_ml_er = (game.home_ml_bayes_prob * odds_profit_mult(self.HomeTeamMoneyLine)) - (1 - game.home_ml_bayes_prob) if self.HomeTeamMoneyLine else -1

        away_team.save()
        home_team.save()
        game.save()


@receiver(post_save, sender=FantasyDataGames)
def game_update_bet_calcs(sender: FantasyDataGames, instance: FantasyDataGames, **kwargs):
    instance.create_game_bet_calcs()


class FootballOutsidersFPlusRatings(models.Model):
    Team = models.CharField(max_length=120, primary_key=True)
    F_plus = models.FloatField()
    OF_plus = models.FloatField()
    DF_plus = models.FloatField()
    FEI = models.FloatField()
    SP_plus = models.FloatField()


class TeamMappings(models.Model):
    fd_team = models.ForeignKey(FantasyDataLeagueHierarchy, to_field='TeamID', db_column='fd_team',
                                null=True, blank=True, on_delete=models.DO_NOTHING, related_name='fd_team',
                                db_constraint=False)
    fo_team = models.ForeignKey(FootballOutsidersFPlusRatings, to_field='Team', db_column='fo_team',
                                null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cfbd_team_id = models.IntegerField(null=True, blank=True)


class CeloBetCalcs(models.Model):
    fd_game = models.OneToOneField(FantasyDataGames, primary_key=True, on_delete=models.CASCADE)
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
    away_ml_implied_prob = models.FloatField(null=True)
    home_ml_implied_prob = models.FloatField(null=True)
    away_ml_bayes_prob = models.FloatField(null=True)
    home_ml_bayes_prob = models.FloatField(null=True)
    away_ml_diff = models.FloatField(null=True)
    home_ml_diff = models.FloatField(null=True)
    ml_overround = models.FloatField(null=True)
    ml_vig = models.FloatField(null=True)
    away_ml_prob_less_vig = models.FloatField(null=True)
    home_ml_prob_less_vig = models.FloatField(null=True)
    away_ml_er = models.FloatField(null=True)
    home_ml_er = models.FloatField(null=True)


class TeamCalculatedRatings(models.Model):
    mapping = models.ForeignKey(TeamMappings, on_delete=models.CASCADE)
    elo = models.IntegerField()


class ArmBetCalcs(models.Model):
    cfbd_game_id = models.BigIntegerField(primary_key=True)
    away_ml = models.IntegerField(null=True)
    home_ml = models.IntegerField(null=True)
    away_ml_prob = models.FloatField(null=True)
    home_ml_prob = models.FloatField(null=True)
    away_ml_implied_prob = models.FloatField(null=True)
    home_ml_implied_prob = models.FloatField(null=True)
    away_ml_bayes_prob = models.FloatField(null=True)
    home_ml_bayes_prob = models.FloatField(null=True)
    ml_overround = models.FloatField(null=True)
    ml_vig = models.FloatField(null=True)
    away_ml_prob_less_vig = models.FloatField(null=True)
    home_ml_prob_less_vig = models.FloatField(null=True)
    away_ml_er = models.FloatField(null=True)
    home_ml_er = models.FloatField(null=True)

    def bet_calcs(self):
        self.away_ml_implied_prob = implied_probability(self.away_ml)
        self.home_ml_implied_prob = implied_probability(self.home_ml)

        self.ml_overround = (self.away_ml_implied_prob + self.home_ml_implied_prob) -1
        self.ml_vig = 1 - (1 / ((self.ml_overround * 100) + 100)) * 100 if self.ml_overround != -1 else 0

        self.away_ml_prob_less_vig = self.away_ml_implied_prob - (self.ml_vig / 2) if self.away_ml \
            else self.away_ml_implied_prob
        self.home_ml_prob_less_vig = self.home_ml_implied_prob - (self.ml_vig / 2) if self.home_ml \
            else self.home_ml_implied_prob

        self.away_ml_bayes_prob = bayes_prob(self.away_ml_prob_less_vig, self.away_ml_prob, self.away_ml_prob_less_vig) \
            if self.away_ml else self.away_ml_prob_less_vig
        self.home_ml_bayes_prob = bayes_prob(self.home_ml_prob_less_vig, self.home_ml_prob, self.home_ml_prob_less_vig) \
            if self.home_ml else self.home_ml_prob_less_vig

        self.away_ml_er = (self.away_ml_bayes_prob * odds_profit_mult(self.away_ml)) - (
                    1 - self.away_ml_bayes_prob) if self.away_ml else -1
        self.home_ml_er = (self.home_ml_bayes_prob * odds_profit_mult(self.home_ml)) - (
                    1 - self.home_ml_bayes_prob) if self.home_ml else -1


@receiver(pre_save, sender=ArmBetCalcs)
def game_update_bet_calcs(sender: ArmBetCalcs, instance: ArmBetCalcs, **kwargs):
    instance.bet_calcs()
