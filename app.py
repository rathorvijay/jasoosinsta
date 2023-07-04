from flask import Flask,request,render_template,jsonify
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
import pandas as pd
import mysql.connector

app = Flask(__name__)

# load the model
model = tf.keras.models.load_model('Fake_IG_ML_Model.h5')

# Establishing the connection
cnx = mysql.connector.connect(
    host='localhost',
    port=3307,
    user='root',
    password='',
    database='instagram-feedback'
)

# Checking if the connection is successful
if not cnx.is_connected():
    print("Failed to connect to the database.")
else:
    print("database connection successful.")


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/policy.html')
def policy():
    return render_template('policy.html')

@app.route('/feedbackform.html')
def feedbackform():
    return render_template('feedbackform.html')

@app.route('/profilebadge.html')
def profilebadge():
    return render_template('profilebadge.html')

@app.route('/message',methods=['POST'])
def message():
    return render_template('message.php')


@app.route('/feedback', methods=['GET', 'POST'])
def form_handler():
    print("inside feedback")
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        massage = request.form['massage']

        print(name, email, subject, massage)

        # Inserting data into the feedback table
        insert_query = "INSERT INTO feedback (name, email, subject, massage) VALUES (%s, %s, %s, %s)"
        values = (name, email, subject, massage)

        try:
            cursor = cnx.cursor()
            cursor.execute(insert_query, values)
            cnx.commit()
            print("Feedback submitted successfully")
            response = jsonify({'message': 'Feedback submitted successfully'})
            response.status_code = 200
            cursor.close()

            # Return the response with a JavaScript alert
            return """
            <script>
                alert('Feedback submitted successfully');
                window.location.href = '/index.html';
            </script>
            """
        except mysql.connector.Error as error:
            print("Something went wrong during insertion:", error)
            response = jsonify({'message': 'Something went wrong during insertion'})
            response.status_code = 500
            return """
            <script>
                alert('something went wrong');
                window.location.href = '/feedbackform.html';
            </script>
            """

    return render_template('feedbackform.html')    

@app.route('/predict', methods=['POST'])
def predict():
    print("inside of predict funtion")
    data = request.get_json()
    # Extract data from the JSON request
    features = [
        data["profilepic"], 
        data["nums/length_username"], 
        data["fullname_words"], 
        data["nums/full_name_length"], 
        data["fullname==username"], 
        data["description"], 
        data["externalUrl"], 
        data["private"], 
        data["posts"], 
        data["followers"], 
        data["follow"]
    ]

    # Reshape the input data
    user_input = np.array(features).reshape(1, -1)

    # Standardize the input data
    scaler_x = StandardScaler()
    instagram_df_train_2 = pd.read_csv('insta_train.csv')
    X_train = instagram_df_train_2.drop(columns=['fake'])
    scaler_x.fit(X_train)
    user_input = scaler_x.transform(user_input)

    # Make a prediction using the model
    prediction = model.predict(user_input)

     # Inserting data into the userinfo table
    insert_query = "INSERT INTO userinfo (Username, Fullname, Description, ExternalUrl, Profilepic, Private, Posts, Followers, Follow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data["username"], data["fullname"], data["description"], data["externalUrl"], data["profilepic"], data["private"], data["posts"], data["followers"], data["follow"])

    try:
        cursor = cnx.cursor()
        cursor.execute(insert_query, values)
        cnx.commit()
        print("User data inserted successfully")
        cursor.close()
    except mysql.connector.Error as error:
             print("Something went wrong during insertion:", error)

    # Determine the predicted result
    result = 1 if prediction[0][0] > prediction[0][1] else 0

    return jsonify({'prediction': result})

   
if __name__ == '__main__':
  app.run(debug=True)