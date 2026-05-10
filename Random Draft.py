import random

def create_draft_football(teams):
    #Creates a random draft order for a given list of teams.

    random.shuffle(teams)
    return teams

teams = ["Chuck", "Adrian", "Deuce", "Keary", "Rell", "Justin", "Kelvin", "Bankey", "Paris", "Rod", "Corey", "Brandon"]
draft_order = create_draft_football(teams)
print(draft_order)