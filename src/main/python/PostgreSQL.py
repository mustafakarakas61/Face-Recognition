import pickle
import psycopg2

from src.resources.Environments import dbName, dbUser, dbPass, dbHost, dbPort, pathFaceResultsMap


def createTable(modelName):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE " + modelName.replace(".h5",
                                            "") + " (id serial PRIMARY KEY, no integer NOT NULL, student VARCHAR(50) NOT NULL, attendance BOOLEAN NOT NULL)")

    with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as f:
        resultsMap = pickle.load(f)

    for ids, values in resultsMap.items():
        cur.execute("INSERT INTO " + modelName.replace(".h5",
                                                       "") + " (no, student, attendance) VALUES (%s, %s, %s)",
                    (ids, values, False))

    conn.commit()
    conn.close()


# createTable("face_myset_v2_18_50_128_swc.h5")


def updateAttendance(tableName, studentNo, studentName):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    cur.execute("SELECT attendance FROM " + tableName + " WHERE no=%s", (int(studentNo),))
    attendance = cur.fetchone()[0]

    if not attendance:
        cur.execute("UPDATE " + tableName + " SET attendance=true WHERE no=%s", (int(studentNo),))
        conn.commit()
        print(studentName + " adlı öğrencinin yoklaması güncellendi.")
    conn.close()


def printAttendance(tableName):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    cur.execute("SELECT no, name FROM " + tableName + " WHERE attendance=true")

    rows = cur.fetchall()

    if len(rows) == 0:
        print("Kaydedilmiş yoklama bulunmamaktadır.")
    else:
        print("Yoklaması True Olan Öğrenciler:\n")
        for row in rows:
            print("No: {} - İsim: {}".format(row[0], row[1]))

    conn.close()
