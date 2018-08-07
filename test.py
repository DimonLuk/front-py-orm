from front_py_orm import config, Model
from Types import Types

config["storage_directory"] = "/home/dimonlu/storage_test"


class Person(Model):
    name = Types.text()
    fullname = Types.text()


p = Person()
person = p.get_by(name="test")
print(person.fullname)
