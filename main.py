from bson.json_util import dumps
from pymongo import MongoClient
import random
import string


class Aboutme:
    def __init__(self):
        self.c = None
        self.connectdb()

    def connectdb(self):
        # This function is used to connect to database and it returns a collection object from mongodb
        uri = "mongodb+srv://Samarth:Samarth@cluster0.3kqbc.mongodb.net/"
        client = MongoClient(uri)
        client.list_database_names()
        db = client['Aboutme']
        self.c = db['Userdata']
        print("DB connection successful")
        return

    def authenticate(self, fname, fkey):
        # this function suthenticates user with the passcode
        cursor = self.c.find_one({"name": fname}, {"skey": 1})
        # Change 2.0 handled edge case of wrong username
        if cursor and str(fkey) == str(cursor["skey"]):
            print("Authentication Successful")
            return 1
        else:
            print(" Wrong key or wrong username")
            return 0

    def custom_hash(self):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return res

    def display_all(self):
        # this function displays all the entries in the datasse
        cursor = self.c.find({}, {"_id": 0, "skey": 0})
        for x in cursor:
            print(dumps(x))
        return

    def query_by_name(self, fname):
        # this functiom is used to query the information by name
        cursor = self.c.find({"name": {"$regex": fname}}, {"_id": 0, "skey": 0})
        for x in cursor:
            print(dumps(x))
        return

    def query_by_proffesion(self, fprof):
        # this function is used to query the information by profession
        cursor = self.c.find({"profession": {"$regex": fprof}}, {"_id": 0, "skey": 0})
        for x in cursor:
            print(dumps(x))

    def query_by_contact(self, fcontact):
        # this function is used to query the information by contact
        cursor = self.c.find({"contact": fcontact}, {"_id": 0, "skey": 0})
        for x in cursor:
            print(dumps(x))

    def query_by_secretkey(self, fsk):
        # this function is used to query the data by passcode
        cursor = self.c.find({"skey": fsk}, {"_id": 0, "skey": 0})
        for x in cursor:
            print(dumps(x))

    def add_data(self, fname, fage, fprof, fcontact, fskills):
        # change 2.0 handled showing duplicates while inserting
        # this function is used add new enteries into the db
        fsecretkey = self.custom_hash()
        print(f"Secret key is {fsecretkey}")
        doc = {
            "name": fname,
            "age": fage,
            "profession": fprof,
            "contact": fcontact,
            "skills": fskills,
            "skey": fsecretkey
        }
        self.c.insert_one(doc)
        print("Inserted About Information successfully")
        print("Displaying added information from the database")
        cursor = self.c.find({"name": fname, "skey": fsecretkey}, {"_id": 0})
        for x in cursor:
            print(dumps(x))

    def delete_data(self, fname, fkey):
        # this function is used to delete about me information
        if self.authenticate(fname, fkey):
            cursor = self.c.find_one({"name": fname})
            if cursor:
                self.c.delete_one({"name": fname})
                print("Sucessfully deleted")
            else:
                print("not Found")

    def edit_data(self, foldname, fnewname, fage, fprof, fcontact, fskills):
        # this function is used to update the information about me
        self.c.update_one({"name": foldname}, {"$set": {"name": fnewname, "age": fage, "profession": fprof, "contact": fcontact, "skills": fskills}})
        print("Here is Your updated information:")
        d = self.c.find_one({"name": fnewname}, {"_id": 0, "skey": 0})
        print(d)


if __name__ == '__main__':
    print("--------Hello User--------")
    e = 1
    while e:
        print("1.ADD about me")
        print("2.UPDATE about me")
        print("3.DELETE about me")
        print("4.DISPLAY all")
        print("5.QUERY BY name,profession,contact")
        print("6.QUERY by secret key")
        print("Enter number with respect to option :")
        n = int(input())
        if n > 6 or n < 0:
            print("----Invalid---")
        else:
            obj = Aboutme()
            print("--------Welcome--------")
            if n == 1:
                print("-----------ADD ABOUT ME-----------")
                print(" Enter your name  : ")
                name = str(input())
                print("Enter your age :")
                age = str(input())
                print("Enter profession :")
                prof = str(input())
                print("Enter Contact : ")
                contact = str(input())
                print("Enter Skills :")
                skills = str(input())
                obj.add_data(name, age, prof, contact, skills)
            elif n == 2:
                print("-----Edit window-----")
                print("Enter your name : ")
                oldname = str(input())
                print("Enter your Secret key")
                secretkey = str(input())
                if obj.authenticate(oldname, secretkey):
                    print("You can go ahead and edit the information")
                    print(" Enter new your name  : ")
                    newname = str(input())
                    print("Enter new your age :")
                    age = str(input())
                    print("Enter new profession :")
                    prof = str(input())
                    print("Enter new Contact : ")
                    contact = str(input())
                    print("Enter new Skills :")
                    skill = str(input())
                    obj.edit_data(oldname, newname, age, prof, contact, skill)
            elif n == 3:
                print("----Delete Window----")
                print("Enter Your name : ")
                name = str(input())
                print("Enter your key :")
                key = str(input())
                obj.delete_data(name, key)
            elif n == 4:
                obj.display_all()
            elif n == 5:
                print("1.Query by name ")
                print("2.Query by profession")
                print("3.Query by contact")
                nn = int(input())
                if nn > 0 and nn < 4:
                    if nn == 1:
                        print("Enter name :")
                        name = str(input())
                        obj.query_by_name(name)
                    elif nn == 2:
                        print("Enter Profession :")
                        prof = str(input())
                        obj.query_by_proffesion(prof)
                    elif nn == 3:
                        print("Enter Contact:")
                        contact = str(input())
                        obj.query_by_contact(contact)
            elif n == 6:
                print("Enter secret key : ")
                sk = str(input())
                obj.query_by_secretkey(sk)
        print(" 0. EXit, 1. Contitue")
        e = int(input())
