import sqlite3, datetime, os

class Network_Database:
    def __init__(self):
        self.database = sqlite3.connect("Network_Database.db") # database name
        self.c = self.database.cursor() # allow for changes
        self.database.text_factory = str # establish data type of table

        self.date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M") # get current date and time

        self.createTable()

    def createTable(self): # create table if not created
        self.c.execute("CREATE TABLE IF NOT EXISTS Network_table(Network_name TEXT, Network_location TEXT, Date TEXT)")

    def insertData(self, network_name, file_name): # insert network into table
        self.c.execute("INSERT INTO Network_table VALUES (?, ?, ?)", (network_name, file_name, " " + self.date))
        self.database.commit()

    def retrieveNetwork(self, network_name): # return network name
        self.c.execute("SELECT Network_location FROM Network_table WHERE Network_name = ?", [network_name])
        return [[str(item) for item in results] for results in self.c.fetchall()] # format tuple into once list

    def displayAll(self): # return all network names and dates
        self.c.execute("SELECT Network_name, Date FROM Network_table ORDER BY Date DESC")
        return [[str(item) for item in results] for results in self.c.fetchall()] # format tuple into once list

    def deleteNetwork(self, network_name): # delete network from table and OS
        try:
            os.remove("C:/Users/ICT/Documents/Program/Network Sim/"+network_name+".pkl") # remove network file from OS
            self.c.execute("DELETE FROM Network_table WHERE Network_name = ?", [network_name])
            self.database.commit()
            return True
        except WindowsError: # if network does not exist
            return False



