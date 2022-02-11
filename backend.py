import sqlite3
from config import DB_NAME

class Database:
    def __init__(self):
        self.con = sqlite3.connect(DB_NAME, check_same_thread=True)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()


class Subject(Database):
    def select_subjects(self):
        query = "select subject_id, subject_name from subjects"
        return self.cur.execute(query).fetchall()


    def insert_subject(self, name):
        query = "insert into subjects (subject_name) values ('"+name+"')"
        self.cur.execute(query)
        self.con.commit()

    def delete_subject(self, id):
        query = "delete from subjects where subject_id='"+id+"'"
        self.cur.execute(query)
        self.con.commit()



class Employee(Database):
    def select_employees(self):
        query = "select * from employees"
        return self.cur.execute(query).fetchall()

    def select_position(self):
        query = "SELECT position FROM employees GROUP BY position"
        return self.cur.execute(query).fetchall()

    def insert_employee(self, name, surname, workplace, position, password):
        query = "insert into employees (name, surname, workplace, position, password) values " \
                "('"+ name +"', '"+ surname +"', '"+ workplace +"', '"+ position +"', '"+ password +"') "
        self.cur.execute(query)
        self.con.commit()

    def delete_employee(self, id):
        query = "delete from employees where employe_id='"+id+"'"
        self.cur.execute(query)
        self.con.commit()



class Statistics(Database):
    def select_statistics_subject(self, subject_id):
        query = "select (select Ism, Familiyasi, ish_joyi, lavozimi, parol from hodimlar where hodimId=hodimId), "

    def insert_statistics(self, e_id, s_id, count, answers, date):
        query = "insert into statistics (employe_id, subject_id, count, answers, date) values " \
                "('"+e_id+"', '"+s_id+"', '"+count+"', '"+answers+"', '"+date+"')"
        self.cur.execute(query)
        self.con.commit()

    def join_employee_subject(self, sub_id):
        query = "SELECT * from employees INNER JOIN statistics ON statistics.subject_id='"+sub_id+"' and statistics.employe_id=employees.employe_id"
        return self.cur.execute(query).fetchall()

    def join_employee_position(self, position):
        query = "SELECT * from employees INNER JOIN statistics ON employees.position='"+position+"' and statistics.employe_id=employees.employe_id inner join subjects on subjects.subject_id=statistics.subject_id"
        return self.cur.execute(query).fetchall()


class Test(Database):
    def select_tests(self, subject_id):
        query = "select * from tests where fan_id='"+subject_id+"'"
        return self.cur.execute(query).fetchall()


    def insert_test(self, q, a, b, c, d, fan_id):
        query = "insert into tests (question, a, b, c, d, fan_id) values ('"+q+"', '"+a+"', '"+b+"', '"+c+"', '"+d+"', '"+fan_id+"')"
        self.cur.execute(query)
        self.con.commit()


    def delete_test(self, id):
        query = "delete from tests where test_id='"+id+"'"
        self.cur.execute(query)
        self.con.commit()


class User(Database):
    def check_password(self, password):
        query = "SELECT employe_id FROM employees where password='"+password+"'"
        result = self.cur.execute(query).fetchall()
        if result:
            return [True, result[0]]
        else:
            return [False, 0]

    # def check_subject(self, text):
