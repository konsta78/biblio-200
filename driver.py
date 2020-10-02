from typing import Protocol
import json


class IBodyDriver(Protocol):
    def save(self, db):
        pass


class JsonDriver(IBodyDriver):
    def __init__(self, filename):
        self.filename = filename

    def save(self, db):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for item in db.read_all_from_db():
                json.dump(item, f, ensure_ascii=False, indent=4)
            f.flush()


class TextDriver(IBodyDriver):
    def __init__(self, filename):
        self.filename = filename

    def save(self, db):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for item in db.read_all_from_db():
                f.write(str(item) + '\n')
            f.close()


class SaveToFile:
    def __init__(self, db, driver: IBodyDriver = None):
        self.driver = driver
        self.db = db

    def save(self):
        self.driver.save(self.db)
