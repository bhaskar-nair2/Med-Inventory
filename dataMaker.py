import tkinter as tk
import sqlite3 as sql
from openpyxl import load_workbook as load


# database and tables
# database: medinv
# nameTable: nameList
# dataTable: medDetails
# Log Table: <pillname>_log
# test Tabel: testVals

class GUI:
    def __init__(self):
        pass


class Func:
    def __init__(self):
        self.db = './data/db/medinv'
        pass

    def makeNameList(self):
        q0 = 'create table if not exists namelist (name varchar(200) primary key ,loc varchar(100))'
        q1 = 'delete from namelist'
        q2 = 'insert into namelist(name,loc) values(?,?)'
        dupCounter = 0
        dataFile = load('./data/files/Search.xlsx')
        con = sql.connect(self.db, isolation_level=None)
        cur = con.cursor()
        cur.execute(q0)
        cur.execute(q1)
        for sheet in range(len(dataFile.sheetnames)):
            dataFile._active_sheet_index = sheet
            dataSheet = dataFile.active
            nameSet = dataSheet['D'][1:]
            locSet = dataSheet['C'][1:]
            for name, loc in zip(nameSet, locSet):
                if name.value is None:
                    break
                try:
                    cur.execute(q2, (name.value, loc.value))
                except sql.IntegrityError:
                    dupCounter += 1
                    print(dupCounter, name.value, loc.value)
                    pass

    def DropTb(self, tab):
        q0 = 'drop table ' + tab
        con = sql.connect(self.db, isolation_level=None)
        cur = con.cursor()
        cur.execute(q0)


class App:
    def __init__(self):
        pass


def main():
    # root = tk.Tk()
    x = Func()
    x.makeNameList()


if __name__ == '__main__':
    main()
