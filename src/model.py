import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def to_long(matches: pd.DataFrame) -> pd.DataFrame:
    """One row per team per match."""
    home = pd.DataFrame({
        "team": matches["HomeTeam"], "opponent": matches["AwayTeam"],
        "goals": matches["FTHG"], "home": 1,
    })
    away = pd.DataFrame({
        "team": matches["AwayTeam"], "opponent": matches["HomeTeam"],
        "goals": matches["FTAG"], "home": 0,
    })
    return pd.concat([home, away], ignore_index=True)


def fit_poisson(matches: pd.DataFrame):
    long = to_long(matches)
    return smf.glm(
        "goals ~ home + team + opponent",
        data=long,
        family=sm.families.Poisson(),
    ).fit()