import os
import glob
import pandas as pd


#Class for auto search and read JSON
class SearchJSON(object):

#Initializing the necessary data structures and entering the path
    def __init__(self, bp):
        self.__basepath = bp #Path to folder with json
        self.__pathdir = list() #Path to folder with folder with json
        self.__pathjson = list() #Path to json
        self.__dictjson = dict() #Dictionary where keys is json file name and value is pandas dataframe from the file

#Search path if json not in one folder, else skip step and use setter
    def search_path(self):
        try:
            for i in os.listdir(self.__basepath):
                path = os.path.join(self.__basepath, i)
                if os.path.isdir(path):
                    self.__pathdir.append(path)

        except TypeError:
            print("Incorrect path \n", TypeError)

        except ValueError:
            print("Path is string\n", ValueError)

        except IndexError:
            print(IndexError)

        except FileNotFoundError:
            print("Incorrect path")

#Search all path to json
    def search_json(self):
        try:
            for i in self.__pathdir:
                if glob.glob(i + '\\*.json') is not []:
                    self.__pathjson.append(glob.glob(i + '\\*.json'))

        except IndexError:
            print(IndexError)

#Inner function, create name for dictionary with json
    def __create_name(self, col):
        try:

            return os.path.basename(col).split('.')[0]

        except ValueError:
            print("No basename")

        except TypeError:
            print("Error type")

#Create dict with content from json
    def create_dict(self):
        try:
            for line in self.__pathjson:
                for column in line:
                    self.__dictjson[self.__create_name(column)] = pd.read_json(column)

        except ValueError:
            print("Пустой файл")


    @property
    def path_json(self):
        try:

            return self.__pathjson

        except TypeError:
            print(TypeError)


    @property
    def path_dir(self):
        try:
            return self.__pathdir

        except TypeError:
            print(TypeError)
#If json in one folder, call this setter and path directory becomes equal to base path
    @path_dir.setter
    def path_dir(self):
        self.__pathdir = self.__basepath

    @property
    def base_path(self):
        try:

            return self.__basepath

        except TypeError:
            print(TypeError)


    @property
    def dict_json(self):

        return self.__dictjson


    @base_path.setter
    def base_path(self, bp):
        self.__basepath = bp