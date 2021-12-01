import os
from flask import Flask,url_for,request,flash,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'restaurant.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'JGEWGR34JGJ345J'

class Restaurant(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(50),nullable = False)
    description = db.Column(db.Text)


    def __init__(self,title,description):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"{self.title}"

@app.route('/')
def index():
    items = Restaurant.query.all()
    return render_template('index.html', items = items)
@app.route('/delete/<int:id>')
def Delete(id):
   
    try:
        getItem = Restaurant.query.get(id)
        db.session.delete(getItem)
        db.session.commit()
        flash('Item Deleted!')
        return redirect('/')
    except:
        return render_template('index.html')
        
@app.route('/submit',methods=["GET","POST"])
def submit():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        newItems = Restaurant(title = title,description=description)
        
        db.session.add(newItems)
        db.session.commit()
        flash('Item Added!')
        return redirect('/')

    else:
        return render_template('index.html')
        
        
        
    


if __name__ == '__main__':
    app.run(debug = True)