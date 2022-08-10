from pymongo import MongoClient # khai báo thư viện pymongo
from pprint import pprint # sử dụng thư viện pprint
client=MongoClient() #tạo đối tượng client
db=client.test #kết nối đến database
student=db.student 
def add():
    student_record={ # tạo record sinh viên
                    'Name':'Ayushi Sharma',
                    'Enrolment':'0875CS191003',
                    'Age':'22'}
    result=student.insert_one(student_record) # insert record vào database
    pprint(student.find_one({'Age':'22'})) # show ra một sinh viên có tuổi 22
def update():
    db.student.update_one({'Age':'22'},
                            {'$set': {'Name':'Name update', # cập nhật name =Name update
                            'Enrolment':'0875CS191003',
                            'Age':'23'}}) #Choosing the record to update
    pprint(student.find_one({'Age':'23'}))
def delete():
    db.student.delete_one({'Age':'23'})# xóa một object có age = 23
    pprint(student.find_one({'Age':'23'}))
if __name__ == '__main__':
    add()
