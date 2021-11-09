import sqlite3
import Risk_Scoring


def SQL_populator(input_list):
    connection = sqlite3.connect('Test.db')
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE questionnaire (
                    VariableName text,
                    Value real
                    )""")
    except:
        None

    for i in range(len(input_list)):
        try:
            c.execute(f"DELETE FROM questionnaire WHERE VariableName='Question_{i}'")
            connection.commit()
        except:
            None
        try:
            c.execute("INSERT INTO questionnaire VALUES (:VariableName,:Value)",
                      {'VariableName': f'Question_{i}', 'Value': input_list[i]})
            connection.commit()
        except:
            None

    try:
        c.execute("""CREATE TABLE risk_scores (
                    VariableName text,
                    Value real
                    )""")
    except:
        None

    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_willingness_score'")
        connection.commit()
    except:
        None
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_willingness_score', 'Value': Risk_Scoring.risk_willingness_scoring()[0]})
        connection.commit()
    except:
        None

    try:
        c.execute(f"DELETE FROM risk_scores WHERE VariableName='risk_capacity_score'")
        connection.commit()
    except:
        None
    try:
        c.execute("INSERT INTO risk_scores VALUES (:VariableName,:Value)",
                  {'VariableName': 'risk_capacity_score', 'Value': Risk_Scoring.risk_capacity_scoring()[0]})
        connection.commit()
    except:
        None


    connection.commit()
    connection.close()


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