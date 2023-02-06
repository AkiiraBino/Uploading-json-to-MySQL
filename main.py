from searchJSON import SearchJSON
from database import Database
import mysql.connector


sj = SearchJSON("C:\\Stack\\BDU")
sj.search_path()
sj.search_json()
sj.create_dict()
dict_json = sj.dict_json

db = Database('localhost', 'root', 'Minion082002.424', 'vulnerabilities')

for key in dict_json.keys():
    db.insert_data(dict_json[key], key)