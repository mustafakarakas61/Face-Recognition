import pickle
import psycopg2

from src.resources.Environments import dbName, dbUser, dbPass, dbHost, dbPort, pathFaceResultsMap


def createTable(modelName: str, trainPercentage: float, dropoutRate: float):
    trainPercentage = trainPercentage * 100
    validationPercentage = 100 - trainPercentage

    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()
    # face_faceset_v1_20_4_1_128x128_xbc
    mType, mName, mVersion, mDataCount, mBatchSize, mEpochsCount, mInputSize, mRandomString = modelName.replace(".h5", "").split("_")

    cur.execute(
        "INSERT INTO models (type, name, version, data_count, batch_size, epochs_count, input_size, random_string, dropout_rate, data_train_percentage, data_validation_percentage) "
        "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) RETURNING id",
        (mType, mName, mVersion.replace("v", ""), mDataCount, mBatchSize, mEpochsCount, mInputSize, mRandomString,
         dropoutRate, str(trainPercentage).replace(".0", "") + "%", str(validationPercentage).replace(".0", "") + "%"))

    affectedId: int = cur.fetchone()[0]

    with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as f:
        resultsMap = pickle.load(f)

    for itemId, itemName in resultsMap.items():
        cur.execute(
            "INSERT INTO models_data (models_id, data_id, data_name) "
            "VALUES (%s, %s, %s)",
            (affectedId, itemId, itemName))

    conn.commit()
    conn.close()

    return affectedId


def executeSql(sql: str, params: tuple):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()
    cur.execute(sql, params)

    conn.commit()
    conn.close()


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
