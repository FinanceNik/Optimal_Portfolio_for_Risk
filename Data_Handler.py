import sqlite3
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
        c.execute("""CREATE TABLE asset_constraints (
                    VariableName text,
                    Value real
                    )""")
    except: pass
    for i in range(len(value_list)):
        try:
            c.execute(f"DELETE FROM questionnaire WHERE VariableName='Asset_{i}'")
            connection.commit()
        except: pass
        try:
            c.execute("INSERT INTO questionnaire VALUES (:VariableName,:Value)",
                      {'VariableName': f'Asset_{i}', 'Value': value_list[i]})
            connection.commit()
        except: pass
    connection.commit()
    connection.close()


def SQL_Populator_Constraints_Minimums(value_list):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE asset_minimums (
                    VariableName text,
                    Value real
                    )""")
    except: pass
    for i in range(len(value_list)):
        try:
            c.execute(f"DELETE FROM asset_minimums WHERE VariableName='Asset_{i}'")
            connection.commit()
        except: pass
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


def show_table_x():
    conn = sqlite3.connect('Test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM questionnaire")
    colnames = cur.description
    for row in colnames:
        print(row[0])
    rows = cur.fetchmany(size=20)
    for row in rows:
        print(row)


# show_table_x()