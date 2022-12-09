from flask import Flask, render_template, request
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('liner_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
# age, bmi,children,['gender']_male, region_northeast, region_northeast, region_southeast, region_southwest, smoker_yes 

@app.route("/pridict", methods=['POST'])
def pridict():
    region_northeast=0	
    region_northwest=0	
    region_southeast=0	
    region_southwest=0
    if request.method == "POST":
        age = request.form['age']
        bmi = request.form['bmi']
        children = request.form['children']
        gender = request.form['gender']
        region = request.form['region']
        smoker = request.form['smoker']

        if region == "region_northeast":
            region_northeast=1
            region_northwest=0	
            region_southeast=0	
            region_southwest=0
        elif region == "region_northwest":
            region_northeast=0
            region_northwest=1	
            region_southeast=0	
            region_southwest=0
        elif region == "region_southeast":
            region_northeast=0
            region_northwest=0	
            region_southeast=1	
            region_southwest=0
        else:
            region_northeast=0
            region_northwest=0	
            region_southeast=0	
            region_southwest=1
        
        standerd_scal = StandardScaler()

        # prediction = model.predict(standerd_scal.fit_transform([[19, 27.900, 0, 0,	0, 0, 0, 1, 1]]))

        prediction = model.predict(standerd_scal.fit_transform([[age, bmi, children, gender, region_northeast, region_northwest, region_southeast, region_southwest, smoker]]))

        output = round(prediction[0], 2)

        return render_template('index.html', prediction="Your premium is {}".format(prediction))
    else:
        return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')

@app.route('/customer')
def customer():
    return render_template('customer_dashboard.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')



if __name__ == '__main__':
    app.run(debug=True)