import sqlite3
import pandas as pd
import Risk_Scoring


def SQL_Populator_Questionnaire(input_list):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE questionnaire (
                    VariableName text,
                    Value real
                    )""")
    except: pass

    for i in range(len(input_list)):
        try:
            c.execute(f"DELETE FROM questionnaire WHERE VariableName='Question_{i}'")
            connection.commit()
        except: pass
        try:
            c.execute("INSERT INTO questionnaire VALUES (:VariableName,:Value)",
                      {'VariableName': f'Question_{i}', 'Value': input_list[i]})
            connection.commit()
        except: pass

    try:
        c.execute("""CREATE TABLE risk_scores (
                    VariableName text,
                    Value real
                    )""")
    except: pass

    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_willingness_score'")
        connection.commit()
    except: pass
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_willingness_score', 'Value': Risk_Scoring.risk_willingness_scoring()[0]})
        connection.commit()
    except: pass

    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_capacity_score'")
        connection.commit()
    except: pass
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_capacity_score', 'Value': Risk_Scoring.risk_capacity_scoring()[0]})
        connection.commit()
    except: pass
    connection.commit()
    connection.close()


def SQL_Populator_Constraints_Assets(value_list):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    try:
        c.execute("""DROP TABLE asset_constraints""")
    except: pass
    try:
        c.execute("""CREATE TABLE asset_constraints (
                    VariableName text,
                    Value real
                    )""")
    except: pass
    for i in range(len(value_list)):
        try:
            c.execute("INSERT INTO asset_constraints VALUES (:VariableName,:Value)",
                      {'VariableName': f'Asset_{i}', 'Value': value_list[i]})
            connection.commit()
        except: pass
    connection.commit()
    connection.close()


def SQL_Populator_Constraints_Minimums(value_list):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    try:
        c.execute("""DROP TABLE asset_minimums""")
    except: pass
    try:
        c.execute("""CREATE TABLE asset_minimums (
                    VariableName text,
                    Value real
                    )""")
    except: pass
    for i in range(len(value_list)):
        try:
            c.execute("INSERT INTO asset_minimums VALUES (:VariableName,:Value)",
                      {'VariableName': f'Asset_{i}', 'Value': value_list[i]})
            connection.commit()
        except: pass
    connection.commit()
    connection.close()


def questionnaire_answers(question):
    c = sqlite3.connect('Test.db')
    cur = c.cursor()
    cur.execute(f"SELECT Value FROM questionnaire WHERE VariableName='{question}'")
    one = cur.fetchone()
    try:
        return one[0]
    except:
        return "None"


def selected_assets():
    full_asset_list = ['CA', 'BO', 'BOFC', 'SE', 'GE', 'GES', 'EME', 'RE']
    selected_list = []
    c = sqlite3.connect('Test.db')
    cur = c.cursor()
    for i in range(8):
        try:
            cur.execute(f"SELECT Value FROM asset_constraints WHERE VariableName='Asset_{i}'")
            one = cur.fetchone()
            selected_list.append(one[0])
        except: pass
    in_list = []
    for i in full_asset_list:
        is_in = i in selected_list
        in_list.append(is_in)
    full_asset_name_list = [
        "Cash", "Bonds", "Bonds FC (hedged)", "Swiss Equity",
        "Global Equity", "Global Equity Small Cap", "Emerging Markets Equity", "Real Estate"
    ]
    data = {"Asset Class": full_asset_name_list,
            "Selected": in_list}
    data_table = pd.DataFrame(data)
    return data_table, in_list


def selected_assets_minimums():
    selected_list = []
    c = sqlite3.connect('Test.db')
    cur = c.cursor()
    for i in range(8):
        try:
            cur.execute(f"SELECT Value FROM asset_minimums WHERE VariableName='Asset_{i}'")
            one = cur.fetchone()
            selected_list.append(one[0])
        except:
            selected_list.append("")
    full_asset_name_list = [
        "min. Cash", "min. Bonds", "min. Bonds FC (hedged)", "min. Swiss Equity",
        "min. Global Equity", "min. Global Equity Small Cap", "min. Emerging Markets Equity", "min. Real Estate"
    ]
    data = {"Asset Class": full_asset_name_list,
            "Selected": selected_list}
    data_table = pd.DataFrame(data)
    return data_table, selected_list


def selected_portfolio_weights():
    selected_list = []
    c = sqlite3.connect('Test.db')
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
    connection = sqlite3.connect('Test.db')
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
    connection = sqlite3.connect('Test.db')
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


def show_table_x():
    conn = sqlite3.connect('Test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolioWeights")
    colnames = cur.description
    for row in colnames:
        print(row[0])
    rows = cur.fetchmany(size=20)
    for row in rows:
        print(row[1])