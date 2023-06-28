from flask import Flask,request,render_template,jsonify
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
import pandas as pd

app = Flask(__name__,template_folder='./')


# load the model
model = tf.keras.models.load_model('Fake_IG_ML_Model.h5')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()


    external_url = data["externalUrl"]
    profile_picture = data["profilepic"]
    name_equals_username = data["fullname==username"]
    private = data["private"]

    nums_length_username = data["nums/length_username"]
    fullname_words = data["fullname_words"]
    nums_profile_name_length = data["nums/full_name_length"]
    

    description_length = data["description"]
    posts = data["posts"]
    follows = data["follow"]
    followers = data["followers"]
    
    print('profile_picture : ',profile_picture)
    print('nums/length username : ',nums_length_username)
    print('fullname words : ',fullname_words)
    print('nums/length fullname : ',nums_profile_name_length)
    print('name==username : ',name_equals_username)
    print('external url : ',external_url)
    print('description length : ',description_length)
   
    
    print('private : ',private)
    print('#posts : ',posts)
    print('#followers : ',followers)
    print('#following : ',follows)
   
    user_input = [profile_picture,nums_length_username,fullname_words,nums_profile_name_length , name_equals_username,description_length,external_url,private,posts,followers,follows]

    user_input = np.array(user_input).reshape(1,-1)
    user_input.shape

    print(user_input)

    scaler_x = StandardScaler()
    instagram_df_train_2 = pd.read_csv('insta_train.csv')
    X_train= instagram_df_train_2.drop(columns = ['fake'])
    scaler_x.fit(X_train)
    user_input = scaler_x.transform(user_input)

    print(user_input)
    # Make a prediction using the model
    prediction = model.predict(user_input)
    print(prediction)

    if  prediction[0][0] >  prediction[0][1]:
        result=1
        print(result)
    else:
        result=0
        print(result)
    # Return the prediction as a JSON response
    return jsonify({'prediction': result})
   
if __name__ == '__main__':
    app.run(debug=True,port=4000)