from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ladyjay09@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title,body):
        self.title= title
        self.body= body

# add route if needed
@app.route('/')
def index():
    return render_template('/blog.html', blog=blog)

@app.route('/blog', methods=['GET', 'POST'])
def blog():

    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)

        return render_template('post.html', blog=blog)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs, title="Build A Blog")  



@app.route('/new_entry', methods=['GET','POST'])
def newentry():

    if request.method =='POST':
        blog_title= request.form['title']
        blog_body= request.form['body']
        title_error=''
        body_error=''

        if len(blog_body) ==0:
            body_error ="Invalid Entry"
        if len(blog_title) == 0:
            title_error ="No title entered"
        

        if not title_error and not body_error:
            updated_blog= Blog(blog_title,blog_body)         
            db.session.add(updated_blog)
            db.session.commit()
            query_string = "/blog?id=" + str(updated_blog.id)

            return redirect(query_string)
        else:
            return render_template('new_entry.html', title_error=title_error, body_error=body_error)  
    else:
        return render_template('new_entry.html')

if __name__ == '__main__':
    app.run()