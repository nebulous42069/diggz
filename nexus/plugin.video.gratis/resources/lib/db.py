import sqlite3
from .plugin2 import m


class DB:
    def __init__(self, media_type):
        self.db = m.cache_file
        self.media_type = media_type
        try:
            self.con = sqlite3.connect(self.db)
            self.cursor = self.con.cursor()
            query = f"CREATE TABLE IF NOT EXISTS {self.media_type}(id integer PRIMARY KEY, item text)"
            self.cursor.execute(query)
            self.con.commit()
        except sqlite3.Error as e:
            m.log(f"Failed to write data to the sqlite table: {e}")
        finally:
            if self.con:
                self.con.close()

    def set(self, _id: str, response: str):
        try:
            self.con = sqlite3.connect(self.db)
            self.cursor = self.con.cursor()
            query = f"INSERT OR REPLACE INTO {self.media_type}(id, item) VALUES(?, ?);"
            self.cursor.execute(query, (_id, response))
            self.con.commit()
        except sqlite3.Error as e:
            m.log(f"Failed to write data to the sqlite table: {e}")
        finally:
            if self.con:
                self.con.close()

    def get(self, _id: int):
        response = None
        try:
            self.con = sqlite3.connect(self.db)
            self.cursor = self.con.cursor()
            query = f"SELECT item FROM {self.media_type} WHERE id = ?"
            self.cursor.execute(query, (_id,))
            response = self.cursor.fetchone()
        except sqlite3.Error as e:
            m.log(f"Failed to read data from the sqlite table: {e}")
        finally:
            if self.con:
                self.con.close()
        return response
    
    def clear_cache(self):
        from xbmcgui import Dialog
        dialog = Dialog()
        clear = dialog.yesno("Clear Cache", "Do You Wish to Clear Addon Cache?")
        if clear:
            try:
                self.con = sqlite3.connect(self.db)
                self.cursor = self.con.cursor()
                self.cursor.execute('DELETE FROM tmdb_meta;',)
                self.con.commit()
            except sqlite3.Error as e:
                m.log(f"Failed to delete data from the sqlite table: {e}")
                dialog.ok("Clear Cache", "There was a problem clearing cache.\nCheck the log for details.")
                return
            finally:
                if self.con:
                    self.con.close()
            try:
                self.con = sqlite3.connect(self.db)
                self.cursor = self.con.cursor()
                self.cursor.execute('VACUUM;',)
                self.con.commit()
            except sqlite3.Error as e:
                m.log(f"Failed to vacuum data from the sqlite table: {e}")
            finally:
                if self.con:
                    self.con.close()
        dialog.notification(m.addon_name, 'Cache Cleared', m.addon_icon, 3000, sound=False)
        return