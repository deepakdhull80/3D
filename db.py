import pymongo
import time
from user import User
from werkzeug.security import generate_password_hash
import os
client = pymongo.MongoClient("mongodb+srv://root:root@cluster0-r7wdc.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("3d")

user_collection=db.get_collection('users')
user_blog=db.get_collection('blog')
user_info=db.get_collection('info')

#---------------------user collection---------------------------------------------#


def getuser(user_name):
    user=user_collection.find_one({"_id":user_name})
    return User(user['_id'],user['email'],user['password'])
# print(getuser("deepak").email)

def count(username):
    data=user_blog.find_one({"_id":username})
    if data:
        return len(data['blog'])
    return 0
# print(count("deepak"))

#-------------------------- Blog collection-----------------------------------------------#

def get_blog(username):
    blog=user_blog.find_one({"_id":username})
    return blog['blog']

# print(get_blog("deepak"))

def add_blog(username,title,text,img="/static/img/portfolio/app1.jpg"):
    if user_blog.find_one({"_id":username}):
        u=count(username)+1
        blog_tmp=get_blog(username)
        text.replace("\n","<br>")
        blog_tmp["blog"+str(u)]={"title":title,"text":text,"date":time.localtime(),"img_path":img}
        user_blog.update_one({"_id":username},{"$set":{"blog":blog_tmp}})
        print("added")
    else:
        user_blog.insert_one({"_id":username,"blog":{"blog1":{"title":title,"text":text,"date":time.localtime(),"img_path":img}}})
# add_blog("root","evening","3 day of text")



def delete_blog(username,blog_name):
    blogs=get_blog(username)
    del blogs[blog_name]
    user_blog.update_one({"_id":username},{"$set":{"blog":blogs}})




def edit_blog(username,blog_name,title,text,img="/static/img/portfolio/app1.jpg"):
    blog_to_edit=get_blog(username)
    blog_to_edit[blog_name]={"title":title,"text":text,"date":time.localtime(),"img_path":img}
    user_blog.update_one({"_id":username},{"$set":{"blog":blog_to_edit}})


# delete_blog('manoj','blog1')


def get_limit_blog(username):
    blog=get_blog(username)
    b={}
    j=0
    for i in blog:
        j+=1
        b[i]=blog[i]
        if j==4:
            break
    return b

# print(get_limit_blog('deepak'))
#-----------------  user information -------------------------------------#

def get_info(username):
    info=user_info.find_one({"_id":username})
    return info['information']

def add_info(username,image_path,dob,linkdin,fb):

    if user_info.find_one({"_id":username}):
        user_info.update_one({"_id":username},{"information":{"image_path":image_path,"dob":dob,"linkdin":linkdin,"fb":fb}})
    else:
        user_info.insert_one({"_id":username,"information":{"image_path":image_path,"dob":dob,"linkdin":linkdin,"fb":fb}})





def adduser(email,user_name,password):
    if not user_collection.find_one({"_id":user_name}):
        hash_password=generate_password_hash(password)
        user_collection.insert_one({"_id":user_name,"email":email,"password":hash_password})
        add_blog(user_name,"Hello "+user_name,"Here I'm welcome to you 3D devotional love.",img='/static/img/portfolio/app1.jpg')
        add_info(user_name,"","","","")
        os.mkdir("/static/blog/"+user_name)
    else:
        print('hello')
# adduser("tmp@3D.com","tmp1","deepak")

