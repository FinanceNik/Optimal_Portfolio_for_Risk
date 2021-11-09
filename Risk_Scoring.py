import sqlite3
import pandas as pd


def Weights(Variable):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    c.execute(f"SELECT Value FROM questionnaire WHERE VariableName='{Variable}'")
    one = c.fetchone()
    return one[0]


def risk_willingness_scoring():

    def knowledge_FM():
        answer = Weights('Question_1')
        if answer == 'never':
            return 1
        elif answer == 'seldom':
            return 2
        elif answer == 'sometimes':
            return 3
        elif answer == 'often':
            return 4
        elif answer == 'very often':
            return 5

    def knowledge_FI():
        answer = Weights('Question_2')
        if answer == '< 1':
            return 1
        elif answer == '1 - 3':
            return 2
        elif answer == '3 - 5':
            return 3
        elif answer == '4 - 8':
            return 4
        elif answer == '> 8':
            return 5

    def risk_return_pref():
        answer = Weights('Question_3')
        if answer == '-2 to +2%':
            return 1
        elif answer == '-5 to +5%':
            return 2
        elif answer == '-10 to +10%':
            return 3
        elif answer == '-15 to +15%':
            return 4
        elif answer == '-20 to +20%':
            return 5

    def behavior_falling_prices():
        answer = Weights('Question_4')
        if answer == 'Liquidate all positions.':
            return 1
        elif answer == 'Liquidate all negative positions.':
            return 2
        elif answer == 'Change my investing strategy.':
            return 3
        elif answer == 'Do nothing. Markets can be volatile.':
            return 4
        elif answer == 'I would by the dip.':
            return 5

    def risk_return_distribution():
        answer = Weights('Question_5')
        if answer == 'First and foremost, I want safety and stability.':
            return 1
        elif answer == 'I would take slight risk to increase my return.':
            return 2
        elif answer == 'I take considerable risk to get higher return.':
            return 3
        elif answer == 'I want high return, therefore I accept great risk.':
            return 4
        elif answer == 'All I care about is return, no matter the risk.':
            return 5

    def numeric_score():
        Q1 = knowledge_FM()
        Q2 = knowledge_FI()
        Q3 = risk_return_pref()
        Q4 = behavior_falling_prices()
        Q5 = risk_return_distribution()

        num_score = sum([Q1, Q2, Q3, Q4, Q5])
        return num_score

    rw_score = numeric_score()
    if rw_score <= 7:
        return 'very low', 1
    elif rw_score <= 12:
        return 'low', 2
    elif rw_score <= 17:
        return 'medium', 3
    elif rw_score <= 22:
        return 'high', 4
    elif rw_score > 22:
        return 'very high', 5
