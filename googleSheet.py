class GoogleSheet:
    import httplib2 
    import apiclient.discovery
    from oauth2client.service_account import ServiceAccountCredentials
    def __init__(self,CREDENTIALS_FILE):
        """
        Initializes an object with certain parameter credentials-file 'CREDENTIALS_FILE'.

        :param CREDENTIALS_FILE: name of file with creds-information
        :type name_sql: string
        """
        self.CREDENTIALS_FILE=CREDENTIALS_FILE
        """
        name of file with creds-information
        """
        self.credentials = self.ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        """
        credentials
        """
        self.httpAuth = self.credentials.authorize(self.httplib2.Http())
        """
        authoriation for tables
        """
        self.service = self.apiclient.discovery.build('sheets', 'v4', http = self.httpAuth)
        """
        service
        """
    def createTable(self):
        """
        Creates table with certain columns.

        :returns: id of table
        :rtype: string
        """
        spreadsheet = self.service.spreadsheets().create(body = {'properties': {'title': 'Финансовый учёт', 'locale': 'ru_RU'},'sheets': [{'properties': {'sheetType': 'GRID','sheetId': 0,'title': 'Лист номер один','gridProperties': {'rowCount': 3, 'columnCount': 3}}}]}).execute()
        spreadsheetId = spreadsheet['spreadsheetId']
        driveService = self.apiclient.discovery.build('drive', 'v3', http = self.httpAuth)
        access = driveService.permissions().create(fileId = spreadsheetId,body = {'type': 'user', 'role': 'writer', 'emailAddress': 'Violettanik27@gmail.com'},).execute()
        return (spreadsheetId)
    def deleteList(self,spreadsheetId,sheet_id):
        """
        Deletes list from table.

        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :param sheet_id: id of sheet
        :type sheet_id: string
        """
        self.service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId,body = {"requests": [{"deleteSheet": {"sheet_id": sheet_id}}]}).execute()
    def copyList(self,spreadsheetId,spreadsheetId2):
        """
        Copies first list from table with id = 'spreadsheetId' into table with id = 'spreadsheetId2'.

        :param spreadsheetId: id of table which first list we copy
        :type spreadsheetId: string
        :param spreadsheetId2: id of table into which we copy the first list of another table
        :type spreadsheetId2: string
        """
        self.service.spreadsheets().sheets().copyTo(spreadsheetId = spreadsheetId,sheetId=0,body={'destinationSpreadsheetId':spreadsheetId2}).execute()
    def sheet_id(self,spreadsheetId):
        """
        Output id of first list in table.

        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :returns: id of first list in table
        :rtype: string
        """
        return self.service.spreadsheets().get(spreadsheetId=spreadsheetId).execute().get('sheets')[0]['properties']['sheetId']
    def updateData(self,spreadsheetId,range,value):
        """
        Changes information in table with id = 'spreadsheetId' in range = 'range'.

        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :param range: range in table where we want to change information
        :type range: string
        :param value: new value of information in range in table
        :type value: string
        """
        self.service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {"valueInputOption": "USER_ENTERED","data": [{"range": range,"majorDimension": "ROWS","values":value}]}).execute()
    def createColumnOrRow(self,spreadsheetId,typeOfCr,index):
        """
        Creates column in table with id = 'spreadsheetId' with dimension = 'typeOfCr' before column number = 'index' + 1.

        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :param typeOfCr: dimension
        :type range: string
        :param index: number of column, before which we want to add new column
        :type value: string
        """
        self.service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {'requests': [{'insertDimension':{'range':{'sheetId':'0','dimension':typeOfCr,'startIndex':index,'endIndex':index+1}}}]}).execute()
    def widthOfColumn(self,spreadsheetId,index,size):
        """
        Changes width of column with index = 'index' in table with id = 'spreadsheetId'.
        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :param index: number of column
        :type index: string
        :param size: new size
        :type size: string
        """
        self.service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {'requests': [{'updateDimensionProperties':{'range':{'sheetId':'0','dimension':'COLUMNS','startIndex':index-1,'endIndex':index},'properties':{'pixelSize':8*size},'fields':'pixelSize'}}]}).execute()
    def getData(self,spreadsheetId,range):
        """
        Output information from range = 'range' from table with id = 'spreadsheetId'.
        :param spreadsheetId: id of table
        :type spreadsheetId: string
        :param range: range in tablefrom which we get information
        :type range: string
        :returns: information from range from table
        :rtype: string
        """
        results = self.service.spreadsheets().values().get(spreadsheetId = spreadsheetId,range=range).execute()
        values=results.get('values',[])
        if not values:
            return "No data found."
        else:
            return results

