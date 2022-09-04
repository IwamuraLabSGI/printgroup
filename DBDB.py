# MySQLdbのインポート
import MySQLdb
import collections


def get_connection():
    return MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='dragonash',
        db='mydb')


def Register(color, ID, cx, cy):
    # データベースへの接続とカーソルの生成
    connection = get_connection()
    cursor = connection.cursor()
    dot = ","
    n = 1
    # ここに実行したいコードを入力します
    for i in range(len(cx)):
        if (color == 1):
            Usedb = "CyanDB"
        elif (color == 2):
            Usedb = "MagendaDB"
        else:
            Usedb = "YellowDB"
        if (cx[i] != 0):
            sql = "INSERT INTO " + Usedb + "(ID,Pointnumber,Xpoint,Ypoint) VALUES(" + str(ID) + dot + str(
                n) + dot + str(cx[i]) + dot + str(cy[i]) + ");"
            n = n + 1
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            # 保存を実行

    # 接続を閉じる
    connection.close()


def register_feature(color, ID, descriptors):
    # データベースへの接続とカーソルの生成
    connection = get_connection()
    cursor = connection.cursor()
    dot = ","
    n = 1
    # ここに実行したいコードを入力します
    for i in range(len(descriptors)):
        if color == 1:
            Usedb = "FeatureLLAHCyanDB"
        elif color == 2:
            Usedb = "FeatureLLAHMagendaDB"
        else:
            Usedb = "FeatureLLAHYellowDB"
        if descriptors[i] != 0:
            Q = int(descriptors[i] / 1086)
            index = descriptors[i] % 1086
            sql = "INSERT INTO " + Usedb + "(Indexnumber,ID,Featurenumber,Q) VALUES(" + str(index) + dot + str(
                ID) + dot + str(n) + dot + str(Q) + ");"
            n = n + 1
            cursor.execute(sql)
            connection.commit()
            cursor.close()
    connection.close()


def retrieveFeature(color, descriptors):
    # データベースへの接続とカーソルの生成
    connection = get_connection()
    cursor = connection.cursor()
    dot = ","
    n = 1
    p = 0
    Q = 0
    index = 0
    answer = []
    search = [[0, 0], [0, 0], [0, 0]]
    # ここに実行したいコードを入力します
    for i in range(len(descriptors)):
        if (color == 1):
            Usedb = "FeatureLLAHCyanDB"
        elif (color == 2):
            Usedb = "FeatureLLAHMagendaDB"
        else:
            Usedb = "FeatureLLAHYellowDB"
        if (descriptors[i] != 0):
            Q = int(descriptors[i] / (1086))
            index = descriptors[i] % (1086)
            sql = "SELECT * FROM  " + Usedb + "  WHERE Indexnumber=" + str(index) + " and Q=" + str(Q) + ";"
            n = n + 1
            cursor.execute(sql)
            connection.commit()
            rows = cursor.fetchall()
            kk = 0
            for i in rows:
                answer.append(i[1])
            cursor.close()
            # 保存を実行
    c = collections.Counter(answer)
    for i in range(len(c)):
        search[i][0] = c.most_common()[i][0]
        search[i][1] = c.most_common()[i][1]
    # 接続を閉じる
    connection.close()
    return search


def NewID():
    # データベースへの接続とカーソルの生成
    connection = get_connection()
    cursor = connection.cursor()
    # ここに実行したいコードを入力します
    sql = "select max(id) from Cyandb;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print("Newid: ", row[0] + 1)
    # 保存を実行
    # 接続を閉じる
    connection.close()
    return row[0] + 1
