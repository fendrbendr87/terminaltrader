import model

class User(model.Model):

    def __init__(self):
        self.dbname = "mydb.db"
        self.tablename = "users"
        self.columns = {
            "username" : "VARCHAR",
            "password" : "VARCHAR"
        }
        self.connect()
    
    def login(self, username, password):
        command = f"SELECT pk FROM {self.tablename} WHERE username = ? AND password = ?;"
        self.cursor.execute(command, (username, password))
        row = self.cursor.fetchone()
        if row is not None:
            self.load_from_id(row[0])
