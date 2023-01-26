import sqlite3
import Portfolio_Creation as pc
import Data_Handler as dh

# --> A list of all the eight asset classes and their abbreviations used in the data.csv file
asset_list = ["CA", "BO", "BOFC", "SE", "GE", "GES", "EME", "RE"]


def dataframe_dateRefactoring():
    # To not recode an already working function, we just call the cleaned DataFrame off the Portfolio_Creation module
    df = pc.data_preparation()[0]
    # In this case, we do, however, need to clean the Date column to be able to split the date into a Month column
    # The for-loop iterates over the whole length of the DataFrame and cleans the Date.
    df.insert(1, 'Month', '')
    for i, _ in enumerate(df.index):
        # The split function is a Python built-in function to separate string. As our dates are in the format string
        # and deliminated as such 01/31/1999, we split the string on the / -character, which created the list, and
        # lastly we take the first (zeroth) element of the list as that is the desired date.
        month = df['Date'].str.split('/')[i][0]
        df['Month'][i] = month
    # Afterwards, we return the new, clean DataFrame to be used in the next function.
    return df


def dataframe_construction():
    # Call the DataFrame of the function above.
    df = dataframe_dateRefactoring()
    # Create new columns for each asset to be able to populate the DataFrame with each class' weight, share and value
    for asset in asset_list:
        df.insert(2, f"{asset}_weight", "")
    for asset in asset_list:
        df.insert(2, f"{asset}_share", "")
    for asset in asset_list:
        df.insert(2, f"{asset}_value", "")

    # Furthermore, we do of course also want the total portfolio value and return to be calculated, and thus we need
    # columns for that too.
    df.insert(2, "portfolio_value", "")
    df.insert(3, "period_return", "")
    return df


def dataframe_population_weights():
    # Get the newly adjusted DataFrame from the function above.
    df = dataframe_construction()
    # Retrieve the asset class weights of the optimal portfolio from the database.
    data = dh.selected_portfolio_weights()[1]
    # Create a tuple with the abbreviation of the asset class and its respective weight.
    data_weights = {"CA": data[0], "BO": data[1], "BOFC": data[2], "SE": data[3],
                    "GE": data[4], "GES": data[5], "EME": data[6], "RE": data[7]}
    # Loop over the whole DataFrame and insert the weights whenever the month is either January or July
    for i, _ in enumerate(df.index):
        if df['Month'][i] == '1' or df['Month'][i] == '7':
            for asset in asset_list:
                df[f'{asset}_weight'][i] = data_weights[f"{asset}"]
        else:
            pass
    return df


# This function populates the DataFrame with the starting value set to CHF 100k and calculated the number of shares
# That can be bought with the chose allocation and the starting value.
def dataframe_population_firstRow():
    df = dataframe_population_weights()
    df['portfolio_value'][177] = 100_000
    df['period_return'][177] = 0.0
    for asset in asset_list:
        df[f'{asset}_value'][177] = df[f'{asset}_weight'][177] * df['portfolio_value'][177]

    for asset in asset_list:
        df[f'{asset}_share'][177] = float(df[f'{asset}_value'][177]) / float(df[f'{asset}'][177])

    return df


# Now, the rest of the DataFrame is populated with data.
def dataframe_population():
    # Get the DataFrame with the populated first row.
    df = dataframe_population_firstRow()
    # As we have chosen to reverse the order to ascending dates earlier, we have to start the loop with the last row
    # and then loop in -1 steps from there. The first row used with data (last row in the DataFrame) is 177.
    markowitz_weights_line = 177
    # loop the whole dataset in 6er steps as after every 6 instances, the weights are already populated (Jan + Jul)
    for line in range(177, 2, -6):
        try:
            for i in range(line-1, line-6, -1):
                for asset in asset_list:
                    df[f'{asset}_value'][i] = float(df[f'{asset}_share'][line]) * float(df[f'{asset}'][i])

                # The portfolio value is the sum of the values of each asset class.
                df['portfolio_value'][i] = float(df['CA_value'][i]) + \
                                           float(df['BO_value'][i]) + \
                                           float(df['BOFC_value'][i]) + \
                                           float(df['SE_value'][i]) + \
                                           float(df['GE_value'][i]) + \
                                           float(df['GES_value'][i]) + \
                                           float(df['EME_value'][i]) + \
                                           float(df['RE_value'][i])
                # Rounding the portfolio value as more than 2 digits after the comma are unnecessary.
                df['portfolio_value'][i] = round(df['portfolio_value'][i], 2)

            # Calculating the newly rebalanced portfolio value
            portf_rebalancing_value = float(df['CA_share'][line]) * float(df['CA'][line-6]) + \
                                      float(df['BO_share'][line]) * float(df['BO'][line-6]) + \
                                      float(df['BOFC_share'][line]) * float(df['BOFC'][line-6]) + \
                                      float(df['SE_share'][line]) * float(df['SE'][line-6]) + \
                                      float(df['GE_share'][line]) * float(df['GE'][line-6]) + \
                                      float(df['GES_share'][line]) * float(df['GES'][line-6]) + \
                                      float(df['EME_share'][line]) * float(df['EME'][line-6]) + \
                                      float(df['RE_share'][line]) * float(df['RE'][line-6])
            # From the rebalanced portfolio value we calculate the value of each asset class position
            # This is done by taking the weight of each asset times the portfolio value
            for asset in asset_list:
                df[f'{asset}_value'][line-6] = float(df[f'{asset}_weight'][markowitz_weights_line]) * \
                                               portf_rebalancing_value

            # Now, calculate the number of shares that can be bought with that amount. For simplification purposes
            # we do purchase the exact number of shares as float, which would translate to fractional shares in the
            # real world in order to not having to deal with cash remainders that could not be invested.
            for asset in asset_list:
                df[f'{asset}_share'][line-6] = float(df[f'{asset}_value'][171]) / float(df[f'{asset}'][171])

            # Calculate the portfolio value.
            df['portfolio_value'][line-6] = float(df['CA_value'][line-6]) + \
                                            float(df['BO_value'][line-6]) + \
                                            float(df['BOFC_value'][line-6]) + \
                                            float(df['SE_value'][line-6]) + \
                                            float(df['GE_value'][line-6]) + \
                                            float(df['GES_value'][line-6]) + \
                                            float(df['EME_value'][line-6]) + \
                                            float(df['RE_value'][line-6])
            # Round the portfolio value to 2 digits after the comma.
            df['portfolio_value'][line-6] = round(df['portfolio_value'][line-6], 2)

        # due to the construction of the loop, there will be an error raised on the line nr. 3. This can be excepted
        # as it is not causing any problems.
        except:
            pass

    return df


# Afterwards, we are saving the backtesting portfolio values into a database in order to generate a graph in the Results
# section in the GUI_TOOL later.
def backtesting_SQL_population():
    df = dataframe_population()
    # Create a list of the portfolio values.
    portValue_list = df['portfolio_value'].to_list()

    # Connect to the database and create a cursor object to execute queries with.
    connection = sqlite3.connect('Database.db')
    c = connection.cursor()

    # The try and except clause is to create a table if it does not exist and to just pass if it does already exist.
    try:
        c.execute("""CREATE TABLE backtesting_portfolio_values (
                    VariableName text,
                    Value real
                    )""")
    except:
        pass

    # For the whole length of the dataset, populate a backtesting value into the database.
    for i, _ in enumerate(portValue_list):
        try:
            c.execute(f"DELETE FROM backtesting_portfolio_values WHERE VariableName='{i}'")
            connection.commit()
        except:
            pass
        try:
            c.execute("INSERT INTO backtesting_portfolio_values VALUES (:VariableName,:Value)",
                      {'VariableName': f'{i}', 'Value': portValue_list[i]})
            connection.commit()
        except:
            pass

    connection.commit()
    connection.close()




