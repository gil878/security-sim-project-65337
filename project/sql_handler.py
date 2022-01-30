from MySQLdb import _mysql



def testSql():
    dbConncet = _mysql.connect("localhost","avivDBmaster","12345","db")
    dbConncet.query("select * from users")

