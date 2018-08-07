import exceptions as e


class Types:
    @staticmethod
    def int(byte_size=0, nullable=False):
        res = ""
        if byte_size == 0:
            res = "INT"
        elif byte_size == 8:
            res = "INT"+str(byte_size)
        elif byte_size == 2:
            res = "INT"+str(byte_size)
        else:
            raise e.InvalidDataTypeException("Invalid data type")
        if nullable:
            return res
        else:
            return res + " NOT NULL"

    @staticmethod
    def integer(nullable=False):
        if nullable:
            return "INTEGER"
        else:
            return "INTEGER NOT NULL"

    @staticmethod
    def tiny_int(nullable=False):
        if nullable:
            return "TINYINT"
        else:
            return "TINYINT NOT NULL"

    @staticmethod
    def small_int(nullable=False):
        if nullable:
            return "SMALLINT"
        else:
            return "SMALLINT NOT NULL"

    @staticmethod
    def medium_int(nullable=False):
        if nullable:
            return "MEDIUMINT"
        else:
            return "MEDIUMINT NOT NULL"

    @staticmethod
    def big_int(nullable=False):
        if nullable:
            return "BIGINT"
        else:
            return "BIGINT NOT NULL"

    @staticmethod
    def unsigned_big_int(nullable=False):
        if nullable:
            return "UNSIGNED BIG INT"
        else:
            return "UNSIGNED BIG INT NOT NULL"

    @staticmethod
    def character(size, nullable=False):
        if size <= 0 or size > 20:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 20")
        else:
            if nullable:
                return "CHARACTER({0})".format(str(size))
            else:
                return "CHARACTER({0}) NOT NULL".format(str(size))

    @staticmethod
    def var_char(size, nullable=False):
        if size <= 0 or size > 255:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 255")
        else:
            if nullable:
                return "VARCHAR({0})".format(str(size))
            else:
                return "VARCHAR({0}) NOT NULL".format(str(size))

    @staticmethod
    def varying_character(size, nullable=False):
        if size <= 0 or size > 255:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 255")
        else:
            if nullable:
                return "VARYING CHAR({0})".format(str(size))
            else:
                "VARYING CHAR({0}) NOT NULL".format(str(size))

    @staticmethod
    def nchar(size, nullable=False):
        if size <= 0 or size > 55:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 55")
        else:
            if nullable:
                return "NCHAR({0})".format(str(size))
            else:
                return "NCHAR({0}) NOT NULL".format(str(size))

    @staticmethod
    def native_character(size, nullable=False):
        if size <= 0 or size > 70:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 70")
        else:
            if nullable:
                return "NATIVE CHARACTER({0})".format(str(size))
            else:
                return "NATIVE CHARACTER({0}) NOT NULL".format(str(size))

    @staticmethod
    def n_var_char(size, nullable=False):
        if size <= 0 or size > 100:
            raise e.InvalidDataTypeException("Invalid size, has to be between 1 and 100")
        else:
            if nullable:
                return "NVARCHAR({0})".format(str(size))
            else:
                return "NVARCHAR({0}) NOT NULL".format(str(size))

    @staticmethod
    def text(nullable=False):
        if nullable:
            return "TEXT"
        else:
            return "TEXT NOT NULL"

    @staticmethod
    def clob(nullable=False):
        if nullable:
            return "CLOB"
        else:
            return "CLOB NOT NULL"

    @staticmethod
    def blob(nullable=False):
        if nullable:
            return "BLOB"
        else:
            return "BLOB NOT NULL"

    @staticmethod
    def real(nullable=False):
        if nullable:
            return "REAL"
        else:
            return "REAL NOT NULL"

    @staticmethod
    def double(nullable=False):
        if nullable:
            return "DOUBLE"
        else:
            return "DOUBLE NOT NULL"

    @staticmethod
    def double_precision(nullable=False):
        if nullable:
            return "DOUBLE PRECISION"
        else:
            return "DOUBLE PRECISION NOT NULL"

    @staticmethod
    def float(nullable=False):
        if nullable:
            return "FLOAT"
        else:
            return "FLOAT NOT NULL"

    @staticmethod
    def numeric(nullable=False):
        if nullable:
            return "NUMERIC"
        else:
            return "NUMERIC NOT NULL"

    @staticmethod
    def decimal(int_size, float_size, nullable=False):
        if nullable:
            return "DECIMAL({0}, {1})".format(int_size, float_size)
        else:
            return "DECIMAL({0}, {1}) NOT NULL".format(int_size, float_size)

    @staticmethod
    def boolean(nullable=False):
        if nullable:
            return "BOOLEAN"
        else:
            return "BOOLEAN NOT NULL"

    @staticmethod
    def date(nullable=False):
        if nullable:
            return "DATE"
        else:
            return "DATE NOT NULL"

    @staticmethod
    def date_time(nullable=False):
        if nullable:
            return "DATETIME"
        else:
            return "DATETIME NOT NULL"
