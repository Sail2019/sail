import pymysql

class Database:
    def __init__(self,host = 'localhost',
                 port = 3306 ,
                 user = 'root',
                 password ='123456',
                 database = 'dict',
                 charset = 'utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_database()

    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.password,
                                  database=self.database,
                                  charset=self.charset)

    def close(self):
        self.db.close()

    def create_cursor(self):
        self.cur = self.db.cursor()

    def select(self,data):
        sql = "select password from user where name =%s"
        self.cur.execute(sql,data[1])
        one_row = self.cur.fetchall()
        return one_row

    def insert(self,data):
        sql = 'insert into user (name,password) value (%s,%s);'
        a=self.select(data)
        if a:
            return False
        elif not a:
            try:
                self.cur.execute(sql,[data[1],data[-1]])
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                return False
            return True

    def select_dict(self,data):
        sql = "select 解释 from words where 单词=%s"
        self.cur.execute(sql,data[1])
        one_row = self.cur.fetchall()
        return one_row

    def insert_record(self,name,data):
        sql = 'insert into record (name,word) value (%s,%s);'
        try:
            self.cur.execute(sql,[name,data[1]])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e
        return True

    def select_record(self,name):
        sql = "select * from record where name=%s order by time;"
        self.cur.execute(sql,name)
        one_row = self.cur.fetchmany(10)
        return one_row












