import datetime
import pickle
import psycopg2

from src.main.python.services.SecurityService import check_password, hash_password
from src.resources.Environments import dbName, dbUser, dbPass, dbHost, dbPort, pathFaceResultsMap


def createTable(modelName: str, trainPercentage: float, dropoutRate: float):
    trainPercentage = trainPercentage * 100
    validationPercentage = 100 - trainPercentage

    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()
    # face_faceset_v1_20_4_1_128x128_xbc
    mType, mName, mVersion, mDataCount, mBatchSize, mEpochsCount, mInputSize, mRandomString = modelName.replace(".h5",
                                                                                                                "").split(
        "_")

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


def removeFromDB(modelId: int):
    sql: str = "DELETE FROM attendance WHERE model_id = " + modelId + "; DELETE FROM statistics WHERE model_id = " + modelId + "; DELETE FROM models_data WHERE models_id = " + modelId + "; DELETE FROM models_results WHERE models_id = " + modelId + "; DELETE FROM models WHERE id = " + modelId + ";"
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost, port=dbPort)
    cur = conn.cursor()
    cur.execute(sql)

    conn.commit()
    conn.close()


def listModels():
    sql = "SELECT m.id as \"m_id\", m.type, m.name, m.version, m.data_count, m.batch_size, m.epochs_count, m.input_size, m.random_string, m.dropout_rate, m.data_train_percentage, m.data_validation_percentage, m.create_date_time, mr.id as \"mr_id\", mr.total_time, mr.train_loss, mr.train_acc, mr.validation_loss, mr.validation_acc FROM models as m LEFT JOIN models_results as mr on mr.models_id = m.id"
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost, port=dbPort)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    models = []
    for row in rows:
        model = {
            "m_id": row[0],
            "type": row[1],
            "name": row[2],
            "version": row[3],
            "data_count": row[4],
            "batch_size": row[5],
            "epochs_count": row[6],
            "input_size": row[7],
            "random_string": row[8],
            "dropout_rate": row[9],
            "data_train_percentage": row[10],
            "data_validation_percentage": row[11],
            "create_date_time": str(row[12]).split(".")[0],
            "mr_id": row[13],
            "total_time": "0" + str(row[14]) if len(str(row[14]).split(":")[0]) == 1 else row[14],
            "train_loss": row[15],
            "train_acc": row[16],
            "validation_loss": row[17],
            "validation_acc": row[18],
            "model_name": row[1] + "_" + row[2] + "_v" + str(row[3]) + "_" + str(row[4]) + "_" + str(
                row[5]) + "_" + str(row[6]) + "_" + row[
                              7] + "_" + row[8] + ".h5"
        }
        models.append(model)

    return models


def executeSql(sql: str, params: tuple = ()):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()
    cur.execute(sql, params)

    conn.commit()
    conn.close()


def compareUser(username: str, password: str):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    selectQuery = "SELECT u.id, u.name, u.password, u.surname, er.name FROM \"user\" as u left join enum_role as er on er.id = u.role_id WHERE u.username = %s"
    cur.execute(selectQuery, (username,))

    row = cur.fetchone()
    if row:
        id, name, hashedPassword, surname, role = row
        if check_password(password=password, hashed_password=hashedPassword):
            currentTime = datetime.datetime.now()
            updateQuery = "UPDATE \"user\" SET last_login = %s WHERE id = %s"
            cur.execute(updateQuery, (currentTime, id))

            conn.commit()
            cur.close()
            conn.close()
            return id, name, surname, role
        else:
            cur.close()
            conn.close()
            return None, None, None, None
    else:
        cur.close()
        conn.close()
        return None, None, None, None


def getUserPass(username: str):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    selectQuery = "SELECT u.id, u.password, u.mail, u.name, u.surname, er.name FROM \"user\" as u left join enum_role as er on er.id = u.role_id WHERE u.username = %s"
    cur.execute(selectQuery, (username,))

    row = cur.fetchone()
    if row:
        user_id, password, mail, name, surname, role = row
        cur.close()
        conn.close()
        return user_id, password, mail, name, surname, role
    else:
        cur.close()
        conn.close()
        return None, None, None, None, None, None


def findUser(username: str):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    selectQuery = "SELECT u.id, u.mail, u.name, u.surname, er.name FROM \"user\" as u left join enum_role as er on er.id = u.role_id WHERE u.username = %s"
    cur.execute(selectQuery, (username,))

    row = cur.fetchone()
    if row:
        user_id, mail, name, surname, role = row
        cur.close()
        conn.close()
        return user_id, mail, name, surname, role
    else:
        cur.close()
        conn.close()
        return None, None, None, None, None


def findUserMail(userMail: str):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)

    cur = conn.cursor()

    selectQuery = "SELECT u.id, u.mail, u.name, u.surname, er.name FROM \"user\" as u left join enum_role as er on er.id = u.role_id WHERE u.mail = %s"
    cur.execute(selectQuery, (userMail,))

    row = cur.fetchone()
    if row:
        user_id, mail, name, surname, role = row
        cur.close()
        conn.close()
        return user_id, mail, name, surname, role
    else:
        cur.close()
        conn.close()
        return None, None, None, None, None


def insertUser(user_username, user_password, user_name, user_surname, user_mail):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost, port=dbPort)
    cur = conn.cursor()

    query = "INSERT INTO \"user\" (username, password, name, surname, role_id, mail) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    values = (user_username, hash_password(user_password), user_name, user_surname, 2, user_mail)

    cur.execute(query, values)

    lastId = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return lastId


def updateUserPass(username, password):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)
    cur = conn.cursor()

    cur.execute("UPDATE \"user\" SET password=%s WHERE username=%s", (hash_password(password), username))
    conn.commit()
    cur.close()
    conn.close()


def updateSecurityCode(userId, securityCode):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)
    cur = conn.cursor()

    cur.execute("UPDATE \"user\" SET security_code=%s WHERE id=%s", (hash_password(securityCode), userId))
    conn.commit()
    cur.close()
    conn.close()


def updateAttendance(tableName, studentNo, studentName):
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost,
                            port=dbPort)
    #
    # cur = conn.cursor()
    #
    # cur.execute("SELECT attendance FROM " + tableName + " WHERE no=%s", (int(studentNo),))
    # attendance = cur.fetchone()[0]
    #
    # if not attendance:
    #     cur.execute("UPDATE " + tableName + " SET attendance=true WHERE no=%s", (int(studentNo),))
    #     conn.commit()
    #     print(studentName + " adlı öğrencinin yoklaması güncellendi.")
    # conn.close()
