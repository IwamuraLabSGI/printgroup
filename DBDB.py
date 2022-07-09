# MySQLdbのインポート
import MySQLdb
def Register(color,ID,cx,cy):
    # データベースへの接続とカーソルの生成
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='dragonash',
        db='mydb')
    cursor = connection.cursor()
    dot = ","
    n = 1
    # ここに実行したいコードを入力します
    for i in range(len(cx)):
        if(color==1):
            Usedb = "CyanDB"
        elif(color==2):
            Usedb = "MagendaDB"
        else:
            Usedb = "YellowDB"
        if(cx[i]!=0):
            sql = "INSERT INTO "+Usedb+"(ID,Pointnumber,Xpoint,Ypoint) VALUES(" +str(ID)+dot+str(n)+dot+str(cx[i])+dot+str(cy[i])+  ");"
            n = n+1
            cursor.execute(sql)
            connection.commit()
            cursor.close 

    
    # 保存を実行

    # 接続を閉じる
    connection.close()

def NewID():
    # データベースへの接続とカーソルの生成
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='dragonash',
        db='mydb')
    cursor = connection.cursor()
    # ここに実行したいコードを入力します
    sql = "select max(id) from Cyandb;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print("Newid: ",row[0]+1)
    # 保存を実行
    # 接続を閉じる
    connection.close()
    return row[0]+1

NewID()
