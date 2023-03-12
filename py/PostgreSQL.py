import pickle
import psycopg2

from Environments import dbName, dbUser, dbPass, dbHost, dbPort, pathResultsMap


def createTable(modelName):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE " + modelName.replace(".h5",
                                            "") + " (id serial PRIMARY KEY, no integer NOT NULL, student VARCHAR(50) NOT NULL, attendance BOOLEAN NOT NULL)")

    with open(pathResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as f:
        resultsMap = pickle.load(f)

    for id, values in resultsMap.items():
        cur.execute("INSERT INTO " + modelName.replace(".h5",
                                                       "") + " (no, student, attendance) VALUES (%s, %s, %s)",
                    (id, values, False))

    conn.commit()
    conn.close()
