import sqlite3
import pandas as pd
import Risk_Scoring
import numpy as np


# This function populates the database with the answers to the respective questions of the questionnaire as well as
# Inserts the risk scores of the Risk Scoring into another table.
def SQL_Populator_Questionnaire(input_list):
    # Firstly, connect to the database file and create a cursor to be able to execute queries.
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    # Create a table called 'questionnaire'. If this table already exists, the try and except statement will return a
    # pass and just continue with the next operation.
    try:
        c.execute("""CREATE TABLE questionnaire (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass
    # Whenever this function is called to populate the respective answer to a question to the database, we want to
    # remove the previous answers from the table. The try and except clause allows the function to continue in case
    # there are no previous answers.
    # We have used DELETE and INSERT actions instead of UPDATE actions because if there is no previous value, the
    # UPDATE statement would return an error.
    for i in range(len(input_list)):
        try:
            # Delete previous answers.
            c.execute(f"DELETE FROM questionnaire WHERE VariableName='Question_{i}'")
            connection.commit()
        except:
            pass
        try:
            # Insert the new answers.
            c.execute("INSERT INTO questionnaire VALUES (:VariableName,:Value)",
                      {'VariableName': f'Question_{i}', 'Value': input_list[i]})
            connection.commit()
        except:
            pass

    # Same routine as in the action with the questionnaire table: Create a table and if it already exists the try and
    # except clause will just move on to the next operation.
    try:
        c.execute("""CREATE TABLE risk_scores (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass

    # This is perhaps not very clean code, but it works.
    # For both, risk willingness score and the risk capacity score, delete the previous values and populate them
    # with the new scores created in the module Risk Scoring.
    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_willingness_score'")
        connection.commit()
    except:
        pass
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_willingness_score', 'Value': Risk_Scoring.risk_willingness_scoring()[0]})
        connection.commit()
    except:
        pass

    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_capacity_score'")
        connection.commit()
    except:
        pass
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_capacity_score', 'Value': Risk_Scoring.risk_capacity_scoring()[0]})
        connection.commit()
    except:
        pass
    connection.commit()
    connection.close()


def SQL_Populator_Constraints_Assets(value_list):
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    try:
        c.execute("""DROP TABLE asset_constraints""")
    except:
        pass
    try:
        c.execute("""CREATE TABLE asset_constraints (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass
    for i in range(len(value_list)):
        try:
            c.execute("INSERT INTO asset_constraints VALUES (:VariableName,:Value)",
                      {'VariableName': f'Asset_{i}', 'Value': value_list[i]})
            connection.commit()
        except:
            pass
    connection.commit()
    connection.close()


def selected_assets():
    # --> The list of all the assets that could be included.
    full_asset_list = ['CA', 'BO', 'BOFC', 'SE', 'GE', 'GES', 'EME', 'RE']
    selected_list = []
    c = sqlite3.connect('Database.db')
    cur = c.cursor()
    # Loop over the entries in the database table. If an asset is selected in will be appended to the 'selected_list'
    # and if not the loop will go to the exception, pass here, and continue with the next iteration of the loop
    # without including the asset that is not selected.
    for i in range(8):
        try:
            cur.execute(f"SELECT Value FROM asset_constraints WHERE VariableName='Asset_{i}'")
            one = cur.fetchone()
            selected_list.append(one[0])
        except:
            pass
    in_list = []

    # Loop generates a true or false value if the possible asset is within the list of all asset. If the asset is
    # not selected, it will not show up in the list and thus generate a value of false.
    for i in full_asset_list:
        is_in = i in selected_list
        in_list.append(is_in)

    # Give the assets properly readable names for the GUI interface, so that the user can understand the weightings
    # of each asset class.
    full_asset_name_list = [
        "Cash", "Bonds", "Bonds FC (hedged)", "Swiss Equity",
        "Global Equity", "Global Equity Small Cap", "Emerging Markets Equity", "Real Estate"
    ]
    data = {"Asset Class": full_asset_name_list,
            "Selected": in_list}
    data_table = pd.DataFrame(data)
    return data_table, in_list


def selected_portfolio_weights():
    selected_list = []
    c = sqlite3.connect('Database.db')
    cur = c.cursor()
    for i in range(8):
        try:
            cur.execute(f"SELECT Value FROM portfolioWeights WHERE VariableName='{i}'")
            one = cur.fetchone()
            selected_list.append(one[0])
        except:
            selected_list.append("")
    full_asset_name_list = [
        "Cash", "Bonds", "Bonds FC (hedged)", "Swiss Equity",
        "Global Equity", "Global Equity Small Cap", "Emerging Markets Equity", "Real Estate"
    ]
    data = {"Asset Class": full_asset_name_list,
            "Selected": selected_list}
    data_table = pd.DataFrame(data)
    return data_table, selected_list


def populate_weights(index, values):
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE portfolioWeights (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass

    for i in range(len(index)):
        try:
            c.execute(f"DELETE FROM portfolioWeights WHERE VariableName='{i}'")
            connection.commit()
        except:
            pass
        try:
            c.execute("INSERT INTO portfolioWeights VALUES (:VariableName,:Value)",
                      {'VariableName': f'{i}', 'Value': values[i]})
            connection.commit()
        except:
            pass


def populate_volatility_AND_return(index, values):
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE portfolio_volatility_AND_return (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass

    for i in range(len(index)):
        try:
            c.execute(f"DELETE FROM portfolio_volatility_AND_return WHERE VariableName='{i}'")
            connection.commit()
        except:
            pass
        try:
            c.execute("INSERT INTO portfolio_volatility_AND_return VALUES (:VariableName,:Value)",
                      {'VariableName': f'{i}', 'Value': values[i]})
            connection.commit()
        except:
            pass


def populate_historical_volatility(vola):
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE portfolio_historical_volatility (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass

    # Delete the entries of possible previous portfolio generations. If no previous entries are present the try and
    # except loop makes sure that the operation continues without interruption.
    try:
        c.execute(f"DELETE FROM portfolio_historical_volatility WHERE VariableName='volatility'")
        connection.commit()
    except:
        pass

    # Insert the values into the table and commit to save the action.
    try:
        c.execute("INSERT INTO portfolio_historical_volatility VALUES (:VariableName,:Value)",
                  {'VariableName': 'volatility', 'Value': vola})
        connection.commit()
    except:
        pass


def historical_volatility():
    # Connect to the DB and create a curser.
    c = sqlite3.connect('Database.db')
    cur = c.cursor()
    try:
        cur.execute(f"SELECT Value FROM portfolio_historical_volatility WHERE VariableName='volatility'")
        one = cur.fetchone()
    except:
        pass
    # As this function only retrieves one value, we simply return it as is.
    return one[0]


def portfolio_backtesting_values_lists():
    # Read the data into a Pandas DataFrame
    df = pd.read_csv('data.csv')
    # As in the .csv sheet, the data is sorted newest to oldest, we reverse the order. Works better in my opinion.
    df = df.iloc[::-1]
    # Generate a list of all the dates in order to display those dates along with the outcome of the backtesting
    # in the visualization on the result page.
    dateList = df['Date'].to_list()
    # Initiate an empty list to populate it with the data from the database.
    backtesting_values = []
    # Connect to the database and generate a curser to execute queries.
    c = sqlite3.connect('Database.db')
    cur = c.cursor()

    # Loop over all the existing entries in the table to get the backtesting values. Try and except to make sure that
    # a possible error does not stop the whole operation.
    for i in range(len(df.index)):
        try:
            cur.execute(f"SELECT Value FROM backtesting_portfolio_values WHERE VariableName='{i}'")
            one = cur.fetchone()
            backtesting_values.append(one[0])
        except:
            pass
    # Return both the list of all the dates and the backtesting values to generate a graph with these values.
    return dateList, backtesting_values


def forward_looking_expected_return(scenario):
    # The scenario expected returns described in the paper.
    # --> positioning: [CA, BO, BOFC, SE, GE, GES, EME, RE]
    # --> Scenario can be: ['bull', 'bear', 'neutral']
    if scenario == 'bull':
        expected_return = [0.0000, 0.0228, 0.0242, 0.0782, 0.0931, 0.1244, 0.1154, 0.0412]
    elif scenario == 'neutral':
        expected_return = [0.0000, 0.0166, 0.0177, 0.0605, 0.0755, 0.1048, 0.0810, 0.0336]
    elif scenario == 'bear':
        expected_return = [0.0000, 0.0108, 0.0126, 0.0433, 0.0595, 0.0810, 0.0504, 0.0248]

    # The weights of the constructed portfolio
    asset_weights = selected_portfolio_weights()[1]

    # Numpy's dot formula is a sumproduct of two arrays, equivalent to Excel's =SUMPRODUCT(X, Y)
    forward_looking_return = np.dot(expected_return, asset_weights)
    return forward_looking_return


# This function is designed to retrieve the answer of a question.
# The function is called with the argument 'question' and collects the respective answer to the defined question from
# the database.
def Answer(question):
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()
    c.execute(f"SELECT Value FROM questionnaire WHERE VariableName='{question}'")
    one = c.fetchone()
    try:
        return one[0]
    except:
        return "No Answer"
