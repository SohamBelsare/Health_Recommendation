from flask import Flask, render_template, request, redirect, url_for,session,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from diabetes import main
import lungCancer
from heart import  train_logistic_regression_model,predict_heart_disease_probability
import os
import pandas as pd
from mymodels import main1,main2

def calculate_map(systolic, diastolic):
    map_value = (2 * diastolic + systolic) / 3
    return map_value

def check_cholesterol_level(saturatedTransFats, dietaryCholesterol, omega3FattyAcids, solubleFiber, alcoholConsumption, smoking):

    # Calculate the total score
    total_score = saturatedTransFats+ dietaryCholesterol+ omega3FattyAcids+ solubleFiber+ alcoholConsumption+ smoking

    # Determine cholesterol level based on the total score
    if total_score >= 8:
        return 2
    elif 4 <= total_score <= 7:
        return 1
    else:
        return 0
    

def has_fever(bodytemp):
    """
    Check if the given body temperature indicates a fever.

    Args:
    - body_temperature (float): The body temperature in degrees Fahrenheit.

    Returns:
    - bool: True if the temperature indicates a fever, False otherwise.
    """
    # Define the fever threshold
    fever_threshold_fahrenheit = 98.6

    # Check if the body temperature is above the threshold
    return bodytemp > fever_threshold_fahrenheit    


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Users_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'User.db')
Checkup_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Checkup.db')
CheckupDetails_uri='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Checkupdetails.db')

app.config['SQLALCHEMY_DATABASE_URI'] = Users_uri
app.config['SQLALCHEMY_BINDS'] = {
    'checkup': Checkup_uri,
    'Checkupdetails':CheckupDetails_uri
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
    doctor=db.Column(db.Integer, nullable=True)

class Checkup(db.Model):
    __bind_key__ = 'checkup'
    id=db.Column(db.Integer, primary_key=True)
    user_adhaar = db.Column(db.Integer,unique=False)
    #Checkup_type=db.Column(db.String(10),nullable=False,unique=False)
    Checkup_Result=db.Column(db.String(10),nullable=False,unique=False)
    Date=db.Column(db.String(10), default=datetime.datetime.utcnow().strftime("%m/%d/%Y"))

class Checkupdetails(db.Model):
    __bind_key__='Checkupdetails'
    id=db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(30),nullable=False,unique=False)
    gender=  db.Column(db.Integer,nullable=False,unique=False)
    age= db.Column(db.Integer,nullable=False,unique=False)
    sleepDuration=  db.Column(db.Float,nullable=False,unique=False)
    qualityOfSleep= db.Column(db.Integer,nullable=False,unique=False)
    physicalActivityLevel=  db.Column(db.Float,nullable=False,unique=False)
    stressLevel= db.Column(db.Integer,nullable=False,unique=False)
    bmi= db.Column(db.Float,nullable=False,unique=False)
    bloodPressure= db.Column(db.Float,nullable=False,unique=False)
    heartRate=  db.Column(db.Integer,nullable=False,unique=False)
    dailySteps= db.Column(db.Integer,nullable=False,unique=False)
    fever= db.Column(db.Integer,nullable=False,unique=False)
    cough= db.Column(db.Integer,nullable=False,unique=False)
    fatigue= db.Column(db.Integer,nullable=False,unique=False)
    breathingDifficulty= db.Column(db.Integer,nullable=False,unique=False)
    cholesterol= db.Column(db.Integer,nullable=False,unique=False)
    
# class Checkup(db.Model):
#     __bind_key__ = 'checkup'
#     id=db.Column(db.Integer, primary_key=True)
#     Date=db.Column(db.String(10), default=datetime.datetime.utcnow().strftime("%m/%d/%Y"))
#     user_adhaar = db.Column(db.Integer,unique=False)
   
#     name: db.Column(db.String(30),nullable=False,unique=False)
#     gender:  db.Column(db.String(10),nullable=False,unique=False)
#     age: db.Column(db.Integer,nullable=False,unique=False)
#     sleepDuration:  db.Column(db.Float,nullable=False,unique=False)
#     qualityOfSleep: db.Column(db.Integer,nullable=False,unique=False)
#     physicalActivityLevel:  db.Column(db.Integer,nullable=False,unique=False)
#     stressLevel: db.Column(db.Integer,nullable=False,unique=False)
#     bmi: db.Column(db.Float,nullable=False,unique=False)
#     bloodPressure: db.Column(db.Integer,nullable=False,unique=False)
#     heartRate:  db.Column(db.Integer,nullable=False,unique=False)
#     dailySteps: db.Column(db.Integer,nullable=False,unique=False)
#     fever: db.Column(db.Integer,nullable=False,unique=False)
#     cough: db.Column(db.Integer,nullable=False,unique=False)
#     fatigue: db.Column(db.Integer,nullable=False,unique=False)
#     breathingDifficulty: db.Column(db.Integer,nullable=False,unique=False)
#     cholesterol: db.Column(db.Integer,nullable=False,unique=False)

#     Checkup_Result=db.Column(db.String(10),nullable=False,unique=False)

        

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
            if user.doctor==0:
            # If the user exists, redirect to the user details page
                session['logged_in'] = True
                session['adhaar'] = user.Adhaar
                return render_template('Dashboard2.html', name=user.Name,Age=user.Age,username=user.Username,password=user.Password,adhaar=user.Adhaar)

            else:
                session['logged_in'] = True
                session['adhaar'] = user.Adhaar
                return render_template('doctor.html', name=user.Name,Age=user.Age,username=user.Username,password=user.Password,adhaar=user.Adhaar)


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
        doctor=int(request.form['doctor'])

        # Create a new user with the given data
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
            new_user = User(Name=name, Age=age, Gender=gender, Phoneno=phoneno, Address=address, Username=username, Password=password, Adhaar=adhaar,doctor=doctor)
            db.session.add(new_user)
            db.session.commit()
            listuser.append(username)
            listAdhar.append(adhaar)
            session['logged_in'] = True
            session['adhaar'] = new_user.Adhaar
            # Redirect to the user details page after successful signup
            if(doctor==0):
                return render_template('Dashboard2.html', name=new_user.Name,Age=new_user.Age,username=new_user.Username,password=new_user.Password,adhaar=new_user.Adhaar)
            else:
                return render_template('doctor.html', name=new_user.Name,Age=new_user.Age,username=new_user.Username,password=new_user.Password,adhaar=new_user.Adhaar)
                

    # If the request method is GET, render the signup page
    return render_template('signup.html')



@app.route('/doctoruser',methods=['GET','POST'])
def doc():
    id=request.form["loginId"]
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))  # Redirect to login page if not logged in
    else:
        user = User.query.filter_by(Adhaar=id).first()

        # Fetch checkup history for the user
        checkups = Checkup.query.filter_by(user_adhaar=id).all()
        for checkup in checkups:
            print(f"Checkup ID: {checkup.id},  Result: {checkup.Checkup_Result}, Date: {checkup.Date}")
        return render_template('doctorhistory.html', user=user, checkups=checkups)
    

@app.route('/review/<int:checkup_id>', methods=['GET','POST'])
def review(checkup_id):
    # Access the checkup_id parameter here
    print("Checkup ID:", checkup_id)
    # ... rest of your code ...
    details=Checkupdetails.query.filter_by(id=checkup_id).all()
    return render_template('review.html',data=details[0])




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
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()

        # Store the result in the session to pass it to the next page

        return render_template('result.html',percent=int(session['prob']*100),result=session['Output'])
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
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()


        return render_template('result.html',percent=int(session['prob']*100),result=session['Output'])

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
        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_Result=session['Output'])
        db.session.add(new_tuple)
        db.session.commit()
        return render_template('result.html',percent=int(session['prob']*100),result=session['Output'])

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
            print(f"Checkup ID: {checkup.id},  Result: {checkup.Checkup_Result}, Date: {checkup.Date}")

        return render_template('history.html', user=user, checkups=checkups)

@app.route('/checkup-form',methods=['GET', 'POST'])
def checkupform():
    if not session.get('logged_in'):
        return redirect(url_for('helloworld'))
    if request.method == 'POST':

        name=str(request.form['name'])
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        sleepduration=float(request.form['sleepDuration'])
        qualityOfSleep=int(request.form['qualityOfSleep'])
        physicalActivity=float(request.form['physicalActivity'])*10
        stresslevel=int(request.form['stressLevel'])
        bmi=float(request.form['bmi'])

        bloodpressure=str(request.form['bloodPressure'])
        bp=bloodpressure.split('/')
        bloodpressure=round(calculate_map(int(bp[0]),int(bp[1])),2)

        heartrate=int(request.form['heartRate'])
        daily_steps=int(request.form['dailySteps'])
        
        bodytemp=float(request.form['bodytemp'])
        Fever=has_fever(bodytemp)

        cough=int(request.form['cough'])
        fatigue=int(request.form['fatigue'])
        Breathing_difficulty=int(request.form['difficultyBreathing'])

        saturatedTransFats=int(request.form['saturatedTransFats'])
        dietaryCholesterol=int(request.form['dietaryCholesterol'])
        omega3FattyAcids=int(request.form['omega3FattyAcids'])
        solubleFiber=int(request.form['solubleFiber'])
        alcoholConsumption=int(request.form['alcoholConsumption'])
        smoking=int(request.form['smoking'])
        cholesterolLevel = check_cholesterol_level(saturatedTransFats, dietaryCholesterol, omega3FattyAcids, solubleFiber, alcoholConsumption, smoking)
        
        details_tuple=Checkupdetails(name=name,gender=gender,age=age,sleepDuration=sleepduration,qualityOfSleep=qualityOfSleep,physicalActivityLevel=physicalActivity,stressLevel=stresslevel,bmi=bmi,bloodPressure=bloodpressure,heartRate=heartrate,dailySteps=daily_steps,fever=Fever,cough=cough,fatigue=fatigue,breathingDifficulty=Breathing_difficulty,cholesterol=cholesterolLevel)
        db.session.add(details_tuple)
        db.session.commit()


        session['name']=name
        session['gender']=gender
        session['age']=age
        session['sleepduration']=sleepduration
        session['qualityOfSleep']=qualityOfSleep
        session['physicalActivity']=physicalActivity
        session['stresslevel']=stresslevel
        session['bmi']=bmi
        session['bloodpressure']=bloodpressure
        session['heartrate']=heartrate
        session['daily_steps']=daily_steps
        session['Fever']=Fever
        session['cough']=cough
        session['fatigue']=fatigue
        session['Breathing_difficulty']=Breathing_difficulty
        session['cholesterolLevel']=cholesterolLevel


        
        if bmi<18.5 :
            bmi=0
        elif bmi>=18.5 and bmi<25:
            bmi=1
        elif bmi>=25:
            bmi=2



        output1=main2(gender, age, sleepduration,qualityOfSleep, physicalActivity,stresslevel,bmi, bloodpressure, heartrate, daily_steps)
        output2=main1(Fever,cough,fatigue,Breathing_difficulty,age,gender,bloodpressure,cholesterolLevel)
        print (str(output2)+str(output1))
        if output1==1 or output2==1:
            session['Output']=1
            result='Must visit'
        else:
            session['Output']=0
            result='Visit Not required'



        new_tuple=Checkup(user_adhaar=session['adhaar'],Checkup_Result=result)
        db.session.add(new_tuple)
        db.session.commit()
        
        return render_template('try.html')

    return render_template('newform.html')



@app.route('/get_health_data')
def get_health_data():
    health_data = {
        "name": session.get('name'),
        "gender":  session.get('gender'),
        "age": session.get('age'),
        "sleepDuration":  session.get('sleepduration'),
        "qualityOfSleep": session.get('qualityOfSleep'),
        "physicalActivityLevel":  session.get('physicalActivity'),
        "stressLevel": session.get('stresslevel'),
        "bmi": session.get('bmi'),
        "bloodPressure": session.get('bloodpressure'),
        "heartRate":  session.get('heartrate'),
        "dailySteps": session.get('daily_steps'),
        "fever": session.get('Fever'),
        "cough": session.get('cough'),
        "fatigue": session.get('fatigue'),
        "breathingDifficulty": session.get('Breathing_difficulty'),
        "cholesterol": session.get('cholesterolLevel'),
        "result":session['Output']
    }
    return jsonify(health_data)


@app.route('/logout')
def logout():
    # Clear session variables to log out the user
    session.pop('logged_in', None)
    session.pop('prob', None)
    session.pop('Output',None)
    session.pop('adhaar', None)

    return redirect(url_for('helloworld'))

if __name__=='__main__':
    app.run(debug=False)





