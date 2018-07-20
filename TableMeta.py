from Types import Types
import sqlite3
import copy


def get(table_name):
    def inner(self, keys):
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
        print(execute_str)
        print(components)
        execute_str = execute_str % tuple(components)
        print(execute_str)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute(execute_str.format(*components))
        res = cursor.fetchall()
        connection.close()
        return res
    return inner


class Model(type):
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
        create_str = """CREATE TABLE IF NOT EXISTS {0} (""".format(dct["__qualname__"])
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
        return super(Model, cls).__new__(cls, name, bases, dct_)


class Person(metaclass=Model):
    name = Types.text()
    fullname = Types.text()
    age = Types.int()


t = Person()
print(t.get_by({"name": "Dima"}))
