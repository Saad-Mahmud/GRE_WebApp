import os
import threading


class DBConf():
    # Here will be the instance stored.
    initDB_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    initDB_dir = os.path.join(initDB_dir, 'Backend')
    initDB_dir = os.path.join(initDB_dir, 'initDB')
    initDB_dir = os.path.join(initDB_dir, 'csvs')
    Language_name = ['English', 'Bangali', 'Arabic', 'Chinese', 'French', 'German', 'Hindi', 'Italian', 'Japanese',
                     'Spanish']
    encoding = "ISO-8859-1"
    TYPEr = ['Translation', 'Meaning', 'Usage', 'Error', 'New Words', 'Bug']
    statusr = ['US', 'TD']
    report = 'This is a generic suggestion for testing.This is a generic suggestion for testing.' + 'This is a generic suggestion for testing.This is a generic suggestion for testing.'

    __instance = None
    lock = threading.Lock()

    def __init__(self):
        self.data = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        DBConf.lock.acquire()
        if DBConf.__instance == None:
            DBConf.__instance = DBConf()
        DBConf.lock.release()
        return DBConf.__instance

    def setData(self, data):
        self.data = data