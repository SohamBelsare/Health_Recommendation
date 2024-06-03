import pandas as pd

from sklearn.neighbors import KNeighborsClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score, classification_report


from sklearn.naive_bayes import GaussianNB  
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report




def main1(Fever,
    Cough,
    Fatigue,
    Difficulty_Breathing,
    Age,
    Gender,
    Blood_Pressure,
    Cholesterol_Level):
    data=pd.read_csv('Disease_symptom_and_patient_profile_dataset.csv')
    
    
    X=data[['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing', 'Age','Gender', 'Blood Pressure', 'Cholesterol Level']]
    Y=data['Outcome']
    
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=4)
                                                                                                  
    #create model                                                   
    #from sklearn.naive_bayes import GaussianNB 
    classifier = GaussianNB()  
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    #accuracy = accuracy_score(y_test, y_pred)
    #print("Accuracy:", accuracy)
    df=pd.DataFrame({
    'Fever':[Fever],
    'Cough':[Cough],
    'Fatigue':[Fatigue],
    'Difficulty Breathing':[Difficulty_Breathing],
    'Age':[Age],
    'Gender':[Gender],
    'Blood Pressure':[Blood_Pressure],
    'Cholesterol Level':[Cholesterol_Level]
    })
    ypred=classifier.predict(df)
    return ypred




def main2(gender, age, sleepduration,qualityOfSleep, physicalActivity,stresslevel,bmi, bloodpressure, heartrate, daily_steps):
    
    data=pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
    
    X=data[['Gender', 'Age', 'Sleep Duration','Quality of Sleep', 'Physical Activity Level', 'Stress Level','BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps',]]
    Y=data['Disorder']
    
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    
    classifier= KNeighborsClassifier(n_neighbors=3, metric='minkowski', p=2 )  
    classifier.fit(X_train, y_train)
    
    
    #y_pred = classifier.predict(X_test) 
    #accuracy = accuracy_score(y_test, y_pred)
    #print(f'Accuracy: {accuracy:.2f}')

    df= pd.DataFrame({
        'Gender':[gender],
        'Age':[age],
        'Sleep Duration':[sleepduration],
        'Quality of Sleep':[qualityOfSleep],
        'Physical Activity Level':[physicalActivity],
        'Stress Level':[stresslevel],
        'BMI Category':[bmi],
        'Blood Pressure':[bloodpressure],
        'Heart Rate':[heartrate],
        'Daily Steps':[daily_steps]
    })
    
    y_pred = classifier.predict(df) 
    
    #accuracy = accuracy_score(y_test, y_pred)
    #print(f'Accuracy: {accuracy:.2f}')
    return y_pred