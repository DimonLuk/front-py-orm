import copy
import sqlite3

from Types import Types


def get_value(self, name):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    result = cursor.execute("""SELECT * FROM {0} where {1}='{2}'"""
                    .format(self.__table_name__, "__uid__", self.__uid__)).fetchall()[0]
    names = cursor.execute("PRAGMA table_info({0})".format(self.__table_name__)).fetchall()
    for i in range(len(names)):
        if names[i][1] == name:
            return result[i]


def set_value(self, name, value):
    if name.startswith("__"):
        self.__dict__[name] = value
    else:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            int(value)
            cursor.execute("""UPDATE {0} SET {1}={2} WHERE __uid__='{3}'"""
                        .format(self.__table_name__, name, value, self.__uid__))
        except ValueError:
            try:
                float(value)
                cursor.execute("""UPDATE {0} SET {1}={2} WHERE __uid__='{3}'"""
                            .format(self.__table_name__, name, value, self.__uid__))
            except ValueError:
                cursor.execute("""UPDATE {0} SET {1}='{2}' WHERE __uid__='{3}'"""
                               .format(self.__table_name__, name, str(value), self.__uid__))
        connection.commit()
        connection.close()


def get(table_name):
    def inner(self, **keys):
        execute_str = """SELECT * FROM %s WHERE """
        components = []
        components.append(table_name)
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
        # print(execute_str)
        # print(components)
        execute_str = execute_str % tuple(components)
        # print(execute_str)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute(execute_str.format(*components))
        res = cursor.fetchall()
        names = cursor.execute("PRAGMA table_info({0})".format(table_name)).fetchall()
        connection.close()
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
            with open(name+"__info.data", "r") as file:
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
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            cursor.execute(create_str)
            if add_column_flag:
                for i in items_to_add:
                    add_column_str = """ALTER TABLE {0} ADD COLUMN {1} '{2}'""".format(name, i, dct_[i])
                    cursor.execute(add_column_str)
            with open(name+"__info.data", "w") as file:
                file.write(",".join(fields_arr))
            connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            pass
        finally:
            return super(ModelMeta, cls).__new__(cls, name, bases, dct_)


class Model(metaclass=ModelMeta):
    pass


class Person(Model):
    name = Types.text()
    fullname = Types.text()
    age = Types.int()


t = Person()
dima = t.get_by(name="Dima")
print(dima.age)
# dima.age = 10
# print(dima.age)

