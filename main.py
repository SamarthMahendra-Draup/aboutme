# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bson.json_util import dumps
from pymongo import MongoClient
class aboutme:
    def __init__(self):
        pass
    def connectdb(self):
        '''
        This function is used to connect to database and it returns a collection object from mongodb
        :return:
        '''
        uri="mongodb+srv://Samarth:Samarth@cluster0.3kqbc.mongodb.net/"
        client=MongoClient(uri)
        client.list_database_names()
        db=client['Aboutme']
        c=db['Userdata']
        print("DB connection successful")
        return c
    def authenticate(self,c,name,key):
        '''
        this function suthenticates user with the passcode
        :param c:
        :param name:
        :param key:
        :return:
        '''
        cursor = c.find_one({"name": name}, {"skey": 1})
        if str(key) == str(cursor["skey"]):
            print("Authentication Successful")
            return 1
        else:
            print(" Wrong key")
            return 0

    '''def custom_hash(self,name,age):
        n=""
        for i in range(0,len(name),2):
            n+=name[i]
        z=n[::-1]
        print(z)
        s=str(z)+str(len(name))+str(age)
        return s'''
    def displayall(self):
        '''
        this function displays all the entries in the datasse
        :return:
        '''
        c = self.connectdb()
        cursor = c.find({},{"_id":0,"skey":0})
        for x in cursor:
            print(dumps(x))
        return
    def querybyname(self):
        '''
        this functiom is used to query the information by name
        :return:
        '''
        print("Enter name :")
        name=str(input())
        c=self.connectdb()
        cursor=c.find({"name":name},{"_id":0,"skey":0})
        for x in cursor:
            print(dumps(x))
        return

    def querybyproffesion(self):
        '''
        this function is used to query the information by profession
        :return:
        '''
        print("Enter Profession :")
        prof=str(input())
        c=self.connectdb()
        cursor=c.find({"profession":prof},{"_id":0,"skey":0})
        for x in cursor:
            print(dumps(x))
    def querybycontact(self):
        '''
        this function is used to query the information by contact
        :return:
        '''
        print("Enter Contact:")
        contact=str(input())
        c=self.connectdb()
        cursor=c.find({"contact":contact},{"_id":0,"skey":0})
        for x in cursor:
            print(dumps(x))
    def querybysecretkey(self):
        '''
        this function is used to query the data by passcode
        :return:
        '''
        print("Enter secret key : ")
        sk=str(input())
        c=self.connectdb()
        cursor=c.find({"skey":sk},{"_id":0,"skey":0})
        for x in cursor:
            print(dumps(x))

    def add_data(self):
        '''
        this function is used add new enteries into the db
        :return:
        '''
        print("-----------ADD ABOUT ME-----------")
        print(" Enter your name  : ")
        name=str(input())
        print("Enter your age :")
        age=str(input())
        print("Enter profession :")
        prof=str(input())
        print("Enter Contact : ")
        contact=str(input())
        print("Enter Skills :")
        skills=str(input())
        '''secretkey=self.custom_hash(name,age)'''
        print("Enter Secret key :")
        secretkey=str(input())
        print(" Please confirm by entering again : ")
        ss=str(input())
        if ss!=secretkey:
            print(" invalid passcode ")

        print(f"Secret key is {secretkey}")
        c=self.connectdb()
        doc={
            "name":name,
            "age":age,
            "profession":prof,
            "contact":contact,
            "skills":skills,
            "skey":secretkey
        }
        c.insert_one(doc)
        print("Inserted About Information successfully")
        print("Displaying added information from the database")
        cursor=c.find({"name":name},{"_id":0})
        for x in cursor:
            print(dumps(x))
    def delete_data(self):
        '''
        this function is used to delete about me information
        :return:
        '''
        print("----Delete Window----")
        print("Enter Your name : ")
        name=str(input())
        print("Enter your key :")
        key=str(input())
        c = self.connectdb()
        if self.authenticate(c,name,key):
            c.delete_one({"name":name})
            print("Sucessfully deleted")



    def edit_data(self):
        '''
        this function is used to update the information about me
        :return:
        '''
        print("-----Edit window-----")
        print("Enter your name : ")
        oldname=str(input())
        print("Enter your Secret key")
        secretkey=str(input())
        c=self.connectdb()
        if self.authenticate(c,oldname,secretkey):
            print("You can go ahead and edit the information")
            print("Enter name,age")
            newname=str(input())
            age=str(input())
            print(c.count_documents({"name":oldname}))
            c.update_one({"name":oldname},{"$set":{"name":newname,"age":age}})
            print("Here is Your updated information:")
            d=c.find_one({"name":newname},{"_id":0,"skey":0})
            print(d)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("--------Hello User--------")
    print("1.ADD about me")
    print("2.UPDATE about me")
    print("3.DELETE about me")
    print("4.DISPLAY all")
    print("5.QUERY BY name,profession,contact")
    print("6.QUERY by secret key")
    print("Enter number with respect to option :")
    n=int(input())
    if n>6 or n<0:
        print("----Invalid---")
    else:
        obj=aboutme()
        print("--------Welcome--------")
        if n==1:
            obj.add_data()
        elif n==2:
            obj.edit_data()
        elif n==3:
            obj.delete_data()
        elif n==4:
            obj.displayall()
        elif n==5:
            print("1.Query by name ")
            print("2.Query by profession")
            print("3.Query by contact")
            nn=int(input())
            if nn>0 and nn<4:
                if nn==1:
                    obj.querybyname()
                elif nn==2:
                    obj.querybyproffesion()
                elif nn==3:
                    obj.querybycontact()
        elif n==6:
            obj.querybysecretkey()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
