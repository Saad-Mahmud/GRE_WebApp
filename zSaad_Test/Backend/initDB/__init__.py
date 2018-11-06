import os

class initDB_Config():

    initDB_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    initDB_dir = os.path.join(initDB_dir, 'Backend')
    initDB_dir = os.path.join(initDB_dir, 'initDB')
    Language_name = ['English','Bangali','Arabic','Chinese','French','German','Hindi','Italian','Japanese','Spanish']
    encoding = "ISO-8859-1"
    TYPEr = ['Translation', 'Meaning', 'Usage', 'Error', 'New Words', 'Bug']
    statusr = ['US', 'TD']
    report = 'This is a generic suggestion for testing.This is a generic suggestion for testing.' + 'This is a generic suggestion for testing.This is a generic suggestion for testing.'

