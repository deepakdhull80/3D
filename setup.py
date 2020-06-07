from flask import Flask,render_template,request,redirect,url_for
import flask_login
from flask_login import LoginManager,login_user,login_required,current_user ,logout_user
from db import getuser,adduser,get_blog,add_blog,get_limit_blog,get_info,edit_blog,delete_blog
import os
# import user


app=Flask(__name__)
app.secret_key="gr3at_d@y_101"
login_manager=LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)
app.config['FILE_UPLOAD']="/static/blog/"

def cvt(st):
    pass


@login_manager.user_loader
def load_user(user_id):
    return getuser(user_id)

# place to work tomorrow-------------------------------

@app.route('/my-blog/<blog>/edit_blog',methods=["POST","GET"])
def edit_blogs(blog):
    if current_user.is_authenticated:
        data=get_blog(current_user.username)
        cur_blog=data[blog]
        return render_template('edit_blog.html',user=current_user,data=cur_blog,blog_name=blog)
    return redirect(url_for('login'))



@app.route('/add-blog/edit',methods=["POST","GET"])
def edit_cur_blog():
    if current_user.is_authenticated:
        if request.method=="POST":
            title=request.form['title']
            text=request.form['text']
            text=text.replace("\n","<br>")
            blog_name=request.form['blog_name']
            path=""
            if request.files['blog_img']:
                fil=request.files['blog_img']
                # print(fil.filename)
                # fil.filename="deepak."+fil.filename.split('.')[1]
                des="/".join([app.config['FILE_UPLOAD']+current_user.username,fil.filename])
                path=des
                fil.save(des)
                path=path.split('3D')[1]
            else:
                path="/static/img/portfolio/app1.jpg"
            # print(text)
            edit_blog(current_user.username,blog_name,title,text,img=path)
            return redirect(url_for('my_blog'))
        return redirect(url_for('my_blog'))
    return redirect(url_for('login'))


@app.route('/my-blog/<blog>/delete_blog',methods=["POST","GET"])
def delete(blog):
    if current_user.is_authenticated:
        delete_blog(current_user.username,blog)
        return redirect(url_for('my_blog'))
    return redirect(url_for('login'))

#----------------------------------------------------------------------

@app.route('/my-blog',methods=["POST","GET"])
def my_blog():
    if current_user.is_authenticated:
        data=get_blog(current_user.username)
        tmp={}
        for i in sorted(data,reverse=True):
            tmp[i]=data[i]
        # info=get_info(current_user.username)
        return render_template('view_blog.html',user=current_user,data=tmp)
    return redirect(url_for('login'))


@app.route('/my-blog/<blog>',methods=["POST","GET"])
def blog_page(blog):
    if current_user.is_authenticated:
        data=get_blog(current_user.username)
        return render_template('blog.html',data=data[blog],blog_name=blog,user=current_user)   
    return redirect(url_for('login'))




# @login_required
@app.route('/add-blog',methods=["POST","GET"])
def add_blogs():
    if current_user.is_authenticated:
        data=get_blog(current_user.username)
        return render_template('add_blog.html',user=current_user,data=data)
    return redirect(url_for('login'))




@login_required
@app.route('/add-blog/write',methods=["POST","GET"])
def write():
    mess=""
    if request.method=="POST":
        title=request.form['title']
        text=request.form['text']
        text=text.replace("\n","<br>")
        path=""
        if request.files['blog_img']:
            fil=request.files['blog_img']
            # print(fil.filename)
            # fil.filename="deepak."+fil.filename.split('.')[1]
            des="/".join([app.config['FILE_UPLOAD']+current_user.username,fil.filename])
            path=des
            fil.save(des)
            path=path.split('3D')[1]
        else:
            path="/static/img/portfolio/app1.jpg"
        # print(text)

        add_blog(current_user.username,title,text,img=path)
        mess="Blog Added Successfully."
        
    return redirect(url_for('home'))







@app.route('/')
def home():
    if current_user.is_authenticated:
        data=get_limit_blog(current_user.username)
        return render_template('dashboard.html',user=current_user,data=data,n=0)
    return render_template('home.html')








@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        data=get_limit_blog(current_user.username)
        return render_template('dashboard.html',user=current_user,data=data,n=0)
    message=''
    if request.method=="POST":    
        user_name=request.form['user_name']
        password=request.form['password']
        user=getuser(user_name)
        if user and user.check_password(password):
            login_user(user)
            data=get_limit_blog(current_user.username)
            return render_template('dashboard.html',user=current_user,data=data,n=0)
    return render_template('login.html',message=message)





@app.route('/signup',methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        data=get_limit_blog(current_user.username)
        return render_template('dashboard.html',user=current_user,data=data,n=0)
    message=''
    if request.method=="POST":
        user_name=request.form['user_name']
        password=request.form['password']
        email=request.form['email']
        repass=request.form['re_password'] 
        if repass==password and user_name and email:
            try:
                adduser(email,user_name,password)
                message="User created successfully"
                return render_template('signup.html',message=message)
            except:
                message="User already Exist"
                return render_template('signup.html',message=message)
        message="Data Insufficient"
    return render_template('signup.html',message=message)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



app.run()