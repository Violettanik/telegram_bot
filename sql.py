class SQL:
    import sqlite3
    def __init__(self,name_sql,name_table):
        """
        Initializes an object with certain parameters: name of sql-file 'name_sql' and name of table 'name_table'.

        :param name_sql: name of sql-file
        :type name_sql: string
        :param name_table: name of table in sql-file
        :type name_table: string
        """
        self.name_sql=name_sql
        """
        name of sql-file
        """
        self.name_table=name_table
        """
        name of table in sql-file
        """
    def create(self,columns):
        """
        Creates table with certain columns.

        :param columns: names columns
        :type name_sql: string
        """
        conn=self.sqlite3.connect(self.name_sql)
        cur=conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {self.name_table} ({columns})')
        conn.commit()
        cur.close()
        conn.close()
    def select(self,search,argument_name,argument_value):
        """
        Gets information from table in sql-file.

        :param search: name of parameter of searching information
        :type search: string
        :param argument_name: name of parameter by which value we chose the row with searching information
        :type argument_name: string
        :param argument_value: value of parameter by which value we chose the row with searching information
        :type argument_value: string
        :returns: searching information
        :rtype: string
        """
        conn=self.sqlite3.connect(self.name_sql)
        cur=conn.cursor()
        cur.execute(f'SELECT {search} FROM {self.name_table} WHERE {argument_name}=="{argument_value}"')
        result=cur.fetchall()
        cur.close()
        conn.close()
        return result
    def insert(self,argument_name,argument_value):
        """
        Inserts information into the table in sql-file.

        :param argument_name: name of parameter which value we want to insert
        :type argument_name: string
        :param argument_value: value which we want to insert
        :type argument_value: string
        """
        conn=self.sqlite3.connect(self.name_sql)
        cur=conn.cursor()
        cur.execute(f'INSERT INTO {self.name_table} ({argument_name}) VALUES({argument_value})')        
        conn.commit()
        cur.close()
        conn.close()
    def update(self,change_name,change_value,argument_name,argument_value):
        """
        Changes information in the table in sql-file.

        :param change_name: name of parameter which value we want to change
        :type change_name: string
        :param change_value: new value
        :type change_value: string
        :param argument_name: name of parameter by which value we chose the row with information that we want to change
        :type argument_name: string
        :param argument_value: value of parameter by which value we chose the row with information that we want to change
        :type argument_value: string
        """
        conn=self.sqlite3.connect(self.name_sql)
        cur=conn.cursor()
        cur.execute(f'UPDATE {self.name_table} SET {change_name}={change_value} WHERE {argument_name}={argument_value}')        
        conn.commit()
        cur.close()
        conn.close()
    def getInfForBot(self,id,index):
        """
        Gets information for correct work of bot with index = 'index' for user with id = 'id' from sql-file.

        :param id: id of user, which information for correct work of bot we are searching
        :type id: string
        :param index: index of information for correct work of bot we are searching
        :type index: string
        :returns: searching information
        :rtype: string
        """
        return self.select('infForBot','id',id)[0][0].split("/")[index]
    def changeInfForBot(self,id,index,argument):
        """
        Changes information information for correct work of bot with index = 'index' for user with id = 'id' from sql-file.

        :param id: id of user, which information for correct work of bot we are changing
        :type id: string
        :param index: index of information for correct work of bot we are changing
        :type index: string
        :param argument: new value of information information for correct work of bot with index = 'index'
        :type argument: string
        """
        inforamationForCorrectBotWork=self.select('infForBot','id',id)[0][0].split("/")
        inforamationForCorrectBotWork[index]=argument
        iFB=''
        for i in range(len(inforamationForCorrectBotWork)):
            iFB+=inforamationForCorrectBotWork[i]+"/"
        self.update('infForBot',"'%s'"%(iFB),'id',id)
