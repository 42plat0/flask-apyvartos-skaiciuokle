import sqlite3

class Database():
    def __init__(self, name, db_filename):
        self.coin_table = name
        self.db_filenam = db_filename

        db = sqlite3.connect(self.db_filenam)

        # Check if table doesn't already exist
        table = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='{self.coin_table}'")
        
        if not table:
            db.execute(f"CREATE TABLE {self.coin_table}(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date TEXT NOT NULL, coins_counted INTEGER NOT NULL, is_correct BOOLEAN)")
        
        db.close()
    
    def write(self, command, values):
        db = sqlite3.connect(self.db_filenam)
        db.execute(command, values)
        db.commit()
        db.close()
