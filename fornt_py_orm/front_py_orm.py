import copy
import datetime
import hashlib
import os
import sqlite3

config = {
    "db_file_name": "data3.db",
    "storage_directory": "/home/dimonlu/PycharmProjects/front-py-orm/storage",
    "username": "",
    "password": ""
}


class DBConnection:

    def __init__(self):
        self.db_name = config["db_file_name"]
        self.username = config["username"]
        self.password = config["password"]

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(config["storage_directory"])
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
        os.chdir(self.cwd)


def get_value(self, name):
    with DBConnection() as cursor:
        result = cursor.execute("""SELECT * FROM {0} where {1}='{2}'"""
                        .format(self.__table_name__, "__uid__", self.__uid__)).fetchall()[0]
        names = cursor.execute("PRAGMA table_info({0})".format(self.__table_name__)).fetchall()
        for i in range(len(names)):
            if names[i][1] == name:
                return result[i]


def set_value(self, name, value):
    if name.startswith("__") and name != "__uid__":
        self.__dict__[name] = value
    elif name != "__uid__":
        with DBConnection() as cursor:
            if type(value) != float and type(value) != int:
                cursor.execute("""UPDATE {0} SET {1}='{2}' WHERE __uid__='{3}'"""
                               .format(self.__table_name__, name, str(value), self.__uid__))
            else:
                cursor.execute("""UPDATE {0} SET {1}={2} WHERE __uid__='{3}'"""
                               .format(self.__table_name__, name, str(value), self.__uid__))


def get(table_name):
    def inner(self, **keys):
        execute_str = """SELECT * FROM %s WHERE """
        components = [table_name]
        for i in keys:
            try:
                float(keys[i])
                execute_str += "%s=%s AND"
                components.append(i)
                components.append(float(keys[i]))
            except ValueError:
                execute_str += "%s='%s' AND "
                components.append(i)
                components.append(keys[i])
        execute_str = execute_str[:-4]
        execute_str = execute_str % tuple(components)
        with DBConnection() as cursor:
            cursor.execute(execute_str.format(*components))
            res = cursor.fetchall()
            result = list()
            obj_name = table_name.split("__")[0]
            for k in res:
                obj = {"__table_name__": table_name, "__getattr__": get_value, "__uid__": k[0], "__setattr__": set_value}
                result.append(type(obj_name, tuple(), obj)())
            if len(result) == 1:
                return result[0]
            else:
                return result
    return inner


class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        dct["__qualname__"] = "{0}__model".format(dct["__qualname__"])
        dct_ = copy.deepcopy(dct)
        name = name+"__model"
        flag = False
        try:
            with open(os.path.join(config["storage_directory"], name+"__info.data"), "r") as file:
                fields = file.read()
        except FileNotFoundError:
            fields = ""
            flag = True
        if fields != "":
            fields_arr = fields.split(",")
        else:
            fields_arr = []
        add_column_flag = False
        items_to_add = []
        create_str = """CREATE TABLE IF NOT EXISTS {0} ( __uid__ VARCHAR(320) NOT NULL,""".format(dct["__qualname__"])
        for item in dct:
            if not item.startswith("__"):
                create_str += "{0} {1},".format(item, dct[item])
                if flag:
                    fields_arr.append(item)
                if fields_arr != [] and item not in fields_arr:
                    add_column_flag = True
                    fields_arr.append(item)
                    items_to_add.append(item)
        dct_["get_by"] = get(name)
        try:
            create_str = create_str[:-1] + ")"
            with DBConnection() as cursor:
                cursor.execute(create_str)
                if add_column_flag:
                    for i in items_to_add:
                        add_column_str = """ALTER TABLE {0} ADD COLUMN {1} '{2}'""".format(name, i, dct_[i])
                        cursor.execute(add_column_str)
                with open(os.path.join(config["storage_directory"], name+"__info.data"), "w") as file:
                    file.write(",".join(fields_arr))
        except sqlite3.OperationalError:
            pass
        finally:
            return super(ModelMeta, cls).__new__(cls, name, bases, dct_)


class Model(metaclass=ModelMeta):
    def add(self, obj):
        def inner(obj_):
            with DBConnection() as cursor:
                to_execute = "INSERT INTO {0} (".format(type(self).__name__)
                hash_ = str(hashlib.sha256((str(datetime.datetime.now())+str(obj_)).encode("utf-8")).hexdigest())
                obj_["__uid__"] = hash_
                for key in obj_:
                    to_execute += key + ","
                to_execute = to_execute[:-1] + ") VALUES ("
                for key in obj_:
                    if type(obj_[key]) != float and type(obj_[key]) != int:
                        to_execute += "'" + str(obj_[key]) + "'" + ","
                    else:
                        to_execute += str(obj_[key])+","
                to_execute = to_execute[:-1] + ")"
                cursor.execute(to_execute)
        if type(obj) == list:
            for i in obj:
                inner(i)
        else:
            inner(obj)
