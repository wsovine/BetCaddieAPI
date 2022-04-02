import numpy as np
from django.conf import settings


def new_rating_basic(winner_rating, loser_rating, k=20, drawn=False):
    winner_rating_weight = 10 ** (winner_rating / 400)
    loser_rating_weight = 10 ** (loser_rating / 400)

    expected_win = winner_rating_weight / float(winner_rating_weight + loser_rating_weight)
    expected_lose = loser_rating_weight / float(winner_rating_weight + loser_rating_weight)

    actual_win = .5 if drawn else 1
    actual_lose = .5 if drawn else 0

    new_winner_rating = winner_rating + k * (actual_win - expected_win)
    new_loser_rating = loser_rating + k * (actual_lose - expected_lose)

    return new_winner_rating, new_loser_rating


def elo_win_probability(elo1: int, elo2: int):
    diff = elo1 - elo2
    p = 1 - 1 / (1 + 10 ** (diff / 400.0))
    return p


def implied_probability(odds: int):
    if odds < 0:
        o = abs(odds)
        return o / (o + 100)
    else:
        o = odds
        return 100 / (o + 100)


def new_ratings(winner_rating, loser_rating, drawn: bool = False, mov: int = 1):
    k = settings.NCAAF_ELO_K

    # MARGIN OF VICTORY MULTIPLIERS
    big_margin = settings.NCAAF_BIG_MARGIN
    k_mult = np.log(mov - (big_margin - 1)) if mov > big_margin else 1
    corr_m = 2.2 / ((winner_rating - loser_rating) * .001 + 2.2) if mov > big_margin else 1

    winner_rating_weight = 10 ** (winner_rating / 400)
    loser_rating_weight = 10 ** (loser_rating / 400)

    expected_win = winner_rating_weight / float(winner_rating_weight + loser_rating_weight)
    expected_lose = loser_rating_weight / float(winner_rating_weight + loser_rating_weight)

    actual_win = .5 if drawn else 1
    actual_lose = .5 if drawn else 0

    new_winner_rating = winner_rating + corr_m * k_mult * k * (actual_win - expected_win)
    new_loser_rating = loser_rating + corr_m * k_mult * k * (actual_lose - expected_lose)

    return new_winner_rating, new_loser_rating


def bayes_prob(prior, model, vegas):
    return (prior * model) / ((prior * model) + (vegas * (1 - prior)))


def odds_profit_mult(odds: int):
    if odds < 0:
        return (1 - 100 / odds) - 1
    else:
        return (1 + odds / 100) - 1
