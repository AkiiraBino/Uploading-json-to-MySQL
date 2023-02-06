from mysql import connector
import math
import numpy
class Database(object):

    #Constructor, connect database and create cursor
    def __init__(self, h, u, p, d): #h - host, u - user, p - passwd, d - database
        try:
            self.__db = connector.connect(host=h, user=u, password=p, database=d)
            self.__cursor = self.__db.cursor()
            print("Connected database OK")

        except ValueError: 
            print(ValueError)

    #Print tables in database
    def tables(self): 
        query = "SHOW TABLES"
        self.__cursor.execute(query)
        tables = list()
        for i in self.__cursor:
            tables.append(i[0])
            
        return tables
    #create %s for syntax MySQL
    def __create_s(self, count):
        s = list()
        for i in range(count):
            s.append("%s")

        return "(" + ", ".join(s) + ")"

    #Formattin data for syntax mySQL
    def __format_adjustment(self, dataframe):
        columns = "(" + ", ".join(dataframe.head(0)) + ")" #columns title
        values = list() #array with line data

        for i in dataframe.values:
            i = i.tolist() #numpy to standart python list

            try:
                if(not math.isnan(i[3])): #there are nan in my database and they need to be changed
                    for j in range(len(i)):
                        if isinstance(i[j], int): #check type
                            continue #int not change
                        else:
                            i[j] = "{0:.6f}".format(i[j]) #float format to 1.000001
                    values.append(list(i)) #add to array

                else:
                    i[3] = "{0:.6f}".format(1.23456789) #if nan write 1.23456789
                    for j in range(len(i)):
                        if isinstance(i[j], int):
                            continue
                        else:
                            i[j] = "{0:.6f}".format(float(i[j]))
                    values.append(list(i))

            except TypeError: #if datatype its string
                try:
                    if (not math.isnan(i[2])):
                        values.append(list(i)) #there are nan in my database and they need to be changed

                    else:
                        i[2] = "{0:.6f}".format(1.23456789) #if nan write 1.23456789
                        values.append(list(i))

                except TypeError:
                        values.append(list(i))

        return [columns, self.__create_s(len(dataframe.columns)), values] #return title columns, array with %s, data
        
    #insert data in database
    def insert_data(self, dataframe, table_name): #dataframe - pandas DataFrame with data, table_name - name table in MySQL
        data = self.__format_adjustment(dataframe) #format data
        print("Work with ", table_name)
        query = f"INSERT INTO {table_name} {data[0]} VALUES {data[1]}" #insert data
        self.__cursor.executemany(query, data[2]) #exec query
        self.__db.commit() #coomit change, comment if you are not sure if the data is entered correctly 
        print("insert OK", table_name)


