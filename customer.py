import pymysql

class customerList:
    #this is the assignment
    def __init__(self):
        self.data=[]
        self.tempdata = {}
        self.tn='palmerba_customers'
        self.fnl = ['fname','lname', 'email', 'password', 'subscribed']
        self.pk = 'id'
        self.conn = None
        self.errorlist= []
    def connect(self):
        import config
        self.conn=pymysql.connect(host=config.DB['host'], port=config.DB['port'],
        user=config.DB['user'], passwd=config.DB['passwd'], db=config.DB['db'],
        autocommit=True)
    def add(self):
        self.data.append(self.tempdata)
    def set(self,fn,val):
        if fn in self.fnl:
            self.tempdata[fn]=val
        else:
            print('invalid field: ' + str(fn))
    def update(self,n,fn,val):
        if len(self.data)>=(n+1) and fn in self.fnl:
            self.data[n][fn] = val
        else:
            print('could not set value at row' +str(n) +'col' +str(fn))
    def insert (self, n=0):

        cols='`,`'.join(self.fnl)
        cols='`'+cols+'`'
        vals=('%s,' * len(self.fnl))[:-1]
        tokens=[]
        for fieldname in self.fnl:
            tokens.append(self.data[n][fieldname])

        sql='insert into' + self.tn+ ' ('+cols+') values ('+vals+');'
        self.connect()
        cur=self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tokens)

        self.data[n][self.pk] = cur.lastrowid()
    def delete(self, n=0):
        item = self.data.pop(n)
        self.deleteByID(item[self.pk])
    def deleteByID(self, id):
        sql = 'DELETE FROM `' + self.tn + '` WHERE `id` = %s'
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tokens)

    def verifyNew(self, n=0):
        self.errorList=[]

        if "fname" not in self.data[n].keys() or len(self.data[n]['fname'])==0:
            self.errorList.append("First name cannot be blank.")
        if "lname" not in self.data[n].keys() or len(self.data[n]['lname'])==0:
            self.errorList.append("Last name cannot be blank.")
        if "email" not in self.data[n].keys() or "@" not in self.data[n]["email"] or "." not in self.data[n]["email"]:
            self.errorList.append("Email not formatted correctly")
        if "password" not in self.data[n].keys() or len(self.data[n]["password"]) > 4:
            self.errorList.append("Password must be longer than 4 characters")
        if "subscribed" not in self.data[n].keys() or self.data[n]["subscribed"] != "True" or self.data[n]["subscribed"] != "False":
            self.errorList.append("Subscribed must be True or False")


        if len(self.errorList)>0:
            return False
        else:
            return True

    def getByID(self, id):
        sql = 'SELECT FROM `' + self.tn + '` WHERE `id` = %s'
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tokens)
        self.data = []
        for row in cur:
            self.data.append(row)

    def getAll(self, order = None):
        sql = 'SELECT FROM `' + self.tn + '`;'
        if order != None:
            sql += 'ORDER BY `' + order + '` '
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tokens)
        self.data = []
        for row in cur:
            self.data.append(row)

    def update(self, n=0):

        tokens=[]
        sql='UPDATE `' + self.tn+ '` SET'
        for fieldname in self.data[n].keys():
            if fieldname != self.pk:
                sql += '`' + fieldname + '` = %s, '
                tokens.append(self.data[n][fieldname])

        sql = sql[:-1]
        sql += ' WHERE `' + self.pk + '` = %s'
        tokens.append(self.pk)

        self.connect()
        cur=self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tokens)
