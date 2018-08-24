import sqlite3

class Model():

    def __init__(self):
        self.dbname = "mydb.db"
        self.tablename = "modelclass"
        self.columns = {
            "value" : "VARCHAR"
        }
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()
        print(self.table_exists())
        if not self.table_exists():
            self.table_create()
        self.data = {}

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def table_exists(self):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.tablename,))
        res = self.cursor.fetchall()
        if len(res) > 0:
            return True
        return False
    
    def table_create(self):
        command = f"DROP TABLE IF EXISTS {self.tablename};"
        self.cursor.execute(command)

        command = f"""CREATE TABLE {self.tablename} (
            pk INTEGER PRIMARY KEY AUTOINCREMENT
            """
        for key in self.columns:
            command = command + f", {key} {self.columns[key]} "
        
        command = command + ");"

        self.cursor.execute(command)
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def stage_save(self):
        if 'pk' not in self.data:
            keys = [key for key in self.data if key in self.columns and key != 'pk']
            command = f"INSERT INTO {self.tablename} ("
            command = command + ", ".join(keys)
            command = command + ") VALUES ("
            command = command + ",".join([" ? " for key in keys])
            command = command + ");"
            values = tuple([self.data[key] for key in keys])
            print(command, values)
            self.cursor.execute(command, values)
            self.cursor.execute('SELECT last_insert_rowid()')
            self.data['pk'] = self.cursor.fetchone()
        else:
            keys = [key for key in self.columns if key != "pk"]
            values = [self.data.get(key, "NULL") for key in keys]
            command = f"UPDATE {self.tablename} SET "
            command = command + ",".join([f"{key} = ? " for key in keys])
            command = command + "WHERE pk = ?;"
            values = tuple(values + [self.data['pk']])
            self.cursor.execute(command, values)
        
    def save(self):
        self.stage_save()
        self.connection.commit()

    def load_from_id(self, id):
        keys = [key for key in self.columns if key != 'pk']
        command = "SELECT "
        command = command + ", ".join(keys)
        command = command + f" FROM {self.tablename} WHERE pk = ?;"
        self.cursor.execute(command, (id,))
        row = self.cursor.fetchone()
        if row is None:
            self['pk'] = None
            for key in keys:
                self.data[key] = None
        else:
            for i in range(len(keys)):
                self.data['pk'] = id
                self.data[keys[i]] = row[i]
