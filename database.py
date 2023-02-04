from mysql import connector
import math
import numpy
class Database(object):

    def __init__(self):
        try:
            self.__db = connector.connect(host="localhost", user="root", password="Minion082002.424", database="vulnerabilities")
            self.__cursor = self.__db.cursor()
            print("Connected database OK")

        except ValueError:
            print(ValueError)

    def tables(self):
        query = "SHOW TABLES"
        self.__cursor.execute(query)
        tables = list()
        for i in self.__cursor:
            tables.append(i[0])
            
        return tables

    def __create_s(self, count):
        s = list()
        for i in range(count):
            s.append("%s")

        return "(" + ", ".join(s) + ")"

    def __format_adjustment(self, dataframe):
        columns = "(" + ", ".join(dataframe.head(0)) + ")"
        values = list()

        for i in dataframe.values:
            i = i.tolist()

            try:
                if(not math.isnan(i[3])):
                    for j in range(len(i)):
                        if isinstance(i[j], int):
                            continue
                        else:
                            i[j] = "{0:.6f}".format(i[j])
                    values.append(list(i))

                else:
                    i[3] = "{0:.6f}".format(1.23456789)
                    for j in range(len(i)):
                        if isinstance(i[j], int):
                            continue
                        else:
                            i[j] = "{0:.6f}".format(float(i[j]))
                    values.append(list(i))

            except TypeError:

                try:
                    if (not math.isnan(i[2])):
                        values.append(list(i))

                    else:
                        i[2] = "{0:.6f}".format(1.23456789)
                        values.append(list(i))

                except TypeError:
                        values.append(list(i))

        return [columns, self.__create_s(len(dataframe.columns)), values]

    def insert_data(self, dataframe, table_name):
        data = self.__format_adjustment(dataframe)
        print("Work with ", table_name)
        query = f"INSERT INTO {table_name} {data[0]} VALUES {data[1]}"
        self.__cursor.executemany(query, data[2])
        self.__db.commit()
        print("insert OK", table_name)


