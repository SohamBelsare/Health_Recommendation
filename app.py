from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
import datetime
from diabetes import main
import lungCancer
from heart import  train_logistic_regression_model,predict_heart_disease_probability
import os
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Users_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'User.db')
Checkup_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Checkup.db')

app.config['SQLALCHEMY_DATABASE_URI'] = Users_uri
app.config['SQLALCHEMY_BINDS'] = {
    'checkup': Checkup_uri
}

db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    Adhaar = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Gender=db.Column(db.String(7),nullable=False)
    Phoneno = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.Text)
    Username = db.Column(db.String(30), nullable=False,unique=True)
    Password = db.Column(db.String(30), nullable=False)

class Checkup(db.Model):
    __bind_key__ = 'checkup'
    id=db.Column(db.Integer, primary_key=True)
    user_adhaar = db.Column(db.Integer,unique=False)
    Checkup_type=db.Column(db.String(10),nullable=False,unique=False)
    Checkup_Result=db.Column(db.String(10),nullable=False,unique=False)
    Date=db.Column(db.String(10), default=datetime.datetime.utcnow().strftime("%m/%d/%Y"))

# Create the database tables within the Flask app context

with app.app_context():
    db.create_all()


listuser=[]
listAdhar=[]


@app.route('/')
def helloworld():
    
    
    return render_template('login.html')





@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(Username=username).first()

        if username==user.Username and password == user.Password:
            # If the user exists, redirect to the user details page
            session['logged_in'] = True
            session['adhaar'] = user.Adhaar
            return render_template('Dashboard.html', name=user.Name,Age=user.Age,username=user.Username,password=user.Password,adhaar=user.Adhaar)
        else:
            # If the user doesn't exist, redirect to the login page
            return 'wrong username and password'

    # If the request method is GET, render the login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve user data from the form
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phoneno = request.form['phone']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        adhaar = request.form['aadhaar']
        existing_user=0
        if (username in listuser  or  adhaar in listAdhar):
            existing_user=1


        # Check if a user with the same username or Aadhaar number already exists
        #existing_user = User.query.filter((User.Username == username) | (User.Adhaar == adhaar)).first()

        if existing_user:
            # If the username or Aadhaar number already exists, redirect to the signup page with an error message
            return render_template('signup.html', error="Username or Aadhaar number already exists. Please choose different ones.")
        else:
            # Create a new user and add it to the database
            new_user = User(Name=name, Age=age, Gender=gender, Phoneno=phoneno, Address=address, Username=username, Password=password, Adhaar=adhaar)
            db.session.add(new_user)
            db.session.commit()
            listuser.append(username)
            listAdhar.append(adhaar)
            session['logged_in'] = True
            session['adhaar'] = new_user.Adhaar
            # Redirect to the user details page after successful signup
            return render_template('Dashboard.html', name=new_user.Name, age=new_user.Age, username=new_user.Username, password=new_user.Password)

    # If the request method is GET, render the signup page
    return render_template('signup.html')

@app.route('/heart',methods=['GET', 'POST'])
def heart():
    # Check if the user is logged in (session variable set)
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))
    if request.method == 'POST':
        trained_model = train_logistic_regression_model('heart.csv')
        age = int(request.form['age'])
        sex= str(request.form['gender'])
        ChestPainType=str(request.form['ChestpainType'])
        RestingBP=float(request.form['RestingBP'])
        Cholesterol=float(request.form['cholesterol'])
        FastingBS=int(request.form['FastingBS'])
        RestingECG=str(request.form['RestingECG'])
        MaxHR=float(request.form['heart-rate'])
        Exang=str(request.form['ExerciseEngina'])
        Oldpeak=float(request.form['Oldpeak'])

        new_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex],
            'ChestPainType': [ChestPainType],
            'RestingBP': [RestingBP],
            'Cholesterol': [Cholesterol],
            'FastingBS': [FastingBS],
            'RestingECG': [RestingECG],
            'MaxHR': [MaxHR],
            'ExerciseAngina': [Exang],
            'Oldpeak': [Oldpeak]
        })
        session['Checkup_type']='Heart'
        session['prob'],session['Output']=predict_heart_disease_probability(trained_model, new_data)
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_type=session['Checkup_type'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()

        # Store the result in the session to pass it to the next page

        return str(session['prob'])+session['Output']

    return render_template('heart.html')
  # Redirect to login page if not logged in
    
@app.route('/diabetes',methods=['GET', 'POST'])
def diabetes():
    # Check if the user is logged in (session variable set)
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))
    if request.method == 'POST':
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        hypertension=int(request.form['Hypertension'])
        bmi=float(request.form['bmi'])
        heartDisease=int(request.form['Heart_Disease'])
        HbA1c_level=float(request.form['hba1c'])
        blood_glucose_level=float(request.form['bgl'])

        session['prob'],session['Output'] = main(gender,age,hypertension,heartDisease,bmi,HbA1c_level,blood_glucose_level)
        session['Checkup_type']='Diabetes'
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_type=session['Checkup_type'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()


        return str(session['prob'])+session['Output']

    return render_template('sugar.html')
    
@app.route('/lung_cancer',methods=['GET', 'POST'])
def lung_cancer():
    # Check if the user is logged in (session variable set)
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))
    if request.method == 'POST':
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        smoking=int(request.form['smoking'])
        yellow_fingers=int(request.form['yellowfinger'])
        anxiety=int(request.form['anxiety'])
        peer_pressure=int(request.form['Peer_pressure'])
        chronic_disease=int(request.form['Chronic Disease'])
        fatigue=int(request.form['Fatigue'])
        allergy=int(request.form['Allergy'])
        weezing=int(request.form['Wheezing'])
        alcohol_consumption=int(request.form['Alcohol'])
        coughing=int(request.form['Coughing'])
        shortness_of_breath=int(request.form['Shortness of Breath'])
        swallowing_difficulty=int(request.form['Swallowing Difficulty'])
        chest_pain=int(request.form['Chest pain'])

        # Store the result in the session to pass it to the next page
        session['prob'],session['Output'] =lungCancer.main(gender,age,smoking,yellow_fingers,anxiety,peer_pressure,chronic_disease,fatigue,allergy,weezing,alcohol_consumption,coughing,shortness_of_breath,swallowing_difficulty,chest_pain ) 
        session['Checkup_type']='Lung Cancer'
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_type=session['Checkup_type'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()
        return str(session['prob'])+session['Output']

    return render_template('cancer.html')

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))  # Redirect to login page if not logged in
    else:
        adhaar = session.get('adhaar')
        user = User.query.filter_by(Adhaar=adhaar).first()

        # Fetch checkup history for the user
        checkups = Checkup.query.filter_by(user_adhaar=adhaar).all()
        for checkup in checkups:
            print(f"Checkup ID: {checkup.id}, Type: {checkup.Checkup_type}, Result: {checkup.Checkup_Result}, Date: {checkup.Date}")

        return render_template('history.html', user=user, checkups=checkups)



@app.route('/logout')
def logout():
    # Clear session variables to log out the user
    session.pop('logged_in', None)
    session.pop('prob', None)
    session.pop('Output',None)
    session.pop('adhaar', None)

    return redirect(url_for('helloworld'))


if __name__=='__main__':
    app.run(debug=True)


