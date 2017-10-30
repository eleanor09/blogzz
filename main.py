from flask import Flask, request, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:ladyjay09@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'learnthis'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title,body,owner):
        self.title= title
        self.body= body
        self.owner= owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password= db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password= password

@app.before_request
def require_login():
    allowed_routes = ['login','blog','index','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



@app.route('/', methods=['POST','GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
    

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method =='POST':
        username= request.form['username']
        password= request.form['password']
        verify= request.form['verify']
        username_error = ''
        password_error=''

#if password or username < 3 characters
        existing_user= User.query.filter_by(username=username).count()

        if len(username) < 3 or len(password) < 3:
            username_error= 'Invalid Entry'
            password_error= 'Invalid Entry'
            return render_template('signup.html', username_error=username_error,password_error=password_error)
        if not username or not password or not verify:
            username_error= 'Fill in All Fields'
            return render_template ('signup.html', username_error=username_error,password_error=password_error)
        if verify!= password:
            password_error='Invalid Password'
            return render_template ('signup.html', username_error=username_error,password_error=password_error)
        if existing_user < 0:
            username_error='Invalid Entry'
            return render_template('signup.html',username_error=username_error,password=password_error)
        else:
            new_user= User(username,password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/new_entry')      

        
    return render_template('signup.html')


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=='POST':
        username= request.form['username']
        password= request.form['password']
        username_error=''
        password_error=''

        user = User.query.filter_by(username=username).first()
        
        if username and password == password:
            session['username']= username            
            return redirect('/new_entry')
        else:
            username_error= "Incorrect Data"

        if username == username and password is not password:
            
            return redirect('/login')
        if username is not username:            
            return redirect('/login')        

    return render_template('login.html')   


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')



@app.route('/blog', methods=['GET', 'POST'])
def list_blog():
      
                       
    if request.args.get('id'):
        blog_id= request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('post.html', blog=blog)

    elif request.args.get('user'):
        user_id= request.args.get('user')
        user = User.request.get(user_id)
        blogs = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blogs=blogs)
        
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, title="Build A Blog")  



@app.route('/new_entry', methods=['GET','POST'])
def newentry():
    if request.method =='GET':
        return render_template('new_entry.html', title='Add Blog')

    if request.method =='POST':
        owner = User.query.filter_by(username=session['username']).first()
        blog_title= request.form['title']
        blog_body= request.form['body']
        title_error=''
        body_error=''     
        
        if len(blog_body) ==0:
            body_error ="Invalid Entry"
        if len(blog_title) == 0:
            title_error ="No title entered"
        

        if not title_error and not body_error:
            updated_blog= Blog(blog_title,blog_body,owner) 
                    
            db.session.add(updated_blog)
            db.session.commit()
            query_string = "/blog?id=" + str(updated_blog.id)

            return redirect(query_string)
        else:
            return render_template('new_entry.html', title_error=title_error, body_error=body_error)  
    

if __name__ == '__main__':
    app.run()