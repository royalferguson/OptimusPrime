import pandas as pd
from os import path


def loggedToCsv(solverName, dataframe):
    dataframe.to_csv(solverName + "_intermvals.csv", index=False)

def readFromCsv(solverName):
    if path.exists(solverName + "_intermvals.csv"):
        try:
            return pd.read_csv(solverName + "_intermvals.csv")
        except:
            return False
    else:
        return False

def readBounds():
    if path.exists("bounds.csv"):
        return pd.read_csv("bounds.csv", header=None)
    else:
        return False

