from flask import request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from app.models.User import *
from app.models.Result import *
from PIL import Image
from tensorflow.keras.utils import normalize
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import numpy as np
import bcrypt
import os
import cv2

path_image = 'static/uploads/'

def returnAPI(code=200, message='', data=[]):
    status = 'success'
    if code != 200:
        status = 'failed'
    returnArray = {
        'code': code,
        'status': status,
        'message': message,
        'data': data
    }
    return jsonify(returnArray)

##*************** AUTH ***************##
def register():
    post = request.form
    password      = bcrypt.hashpw(post['password'].encode('utf8'), bcrypt.gensalt())
    checkUsername = User.get_by_username(post['username'])
    if checkUsername == None:
        user = User()
        user.nama     = post['nama']
        user.username = post['username']
        user.password = password
        user.roles    = 'user'
        user.save()
        return returnAPI(200, 'Register berhasil, silahkan login untuk klasifikasi.!')
    else:
        return returnAPI(201, 'Username sudah terdaftar.!')

def login():
    post = request.form
    user = User.get_by_username(post['username'])
    if user == None:
        return returnAPI(202, 'Username yang anda masukan salah.!')
    if bcrypt.checkpw(post['password'].encode('utf8'), user['password'].encode('utf8')):
        return returnAPI(200, 'Login berhasil.!', user)
    else:
        return returnAPI(202, 'Password yang anda masukan salah.!')

##*************** PREDICT ***************##
def save_file(image):
    name = secure_filename(image.filename)
    path = os.path.join(path_image, name)

    try:
        os.remove(path)
    except OSError:
        pass
        
    image.save(path)
    return name

def predict():
    # Load the Model
    model_inception = tf.keras.models.load_model('static/model/best_model_inceptionv3.keras')
    model_mobileNet = tf.keras.models.load_model('static/model/best_model_MobileNetV2.keras')

    classes = ['Belimbing Wuluh', 'Jambu Biji', 'Jeruk Nipis', 'Kemangi', 'Lidah Buaya', 'Nangka', 'Pandan', 'Pepaya', 'Seledri', 'Sirih']
    size    = 224

    image = request.files['image']
    name  = save_file(image)

    image_path = os.path.join(path_image, name)

    # 1. Muat gambar dengan ukuran target yang sama
    img = load_img(image_path, target_size=(size, size))

    # 2. Ubah gambar menjadi array NumPy
    img_array = img_to_array(img)

    # 3. Ubah skala nilai piksel menjadi [0, 1] (sama seperti pelatihan)
    img_array = img_array / 255.0

    # 4. Perluas dimensi agar sesuai dengan bentuk input model (batch size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)

    # 5. Memprediksi probabilitas kelas
    pred_inception = model_inception.predict(img_array)
    pred_mobileNet = model_mobileNet.predict(img_array)

    # 6. Dapatkan kelas yang diprediksi dan probabilitasnya
    y_pred_inception = np.argmax(pred_inception, axis=1)
    y_pred_mobileNet = np.argmax(pred_mobileNet, axis=1)

    result_inception = classes[y_pred_inception[0]]
    result_mobileNet = classes[y_pred_mobileNet[0]]

    prob_inception = round(np.max(pred_inception)*100, 2)
    prob_mobileNet = round(np.max(pred_mobileNet)*100, 2)

    data = {'image_path': image_path,
            'predict_inception': result_inception,
            'predict_mobileNet': result_mobileNet,
            'prob_inception': prob_inception,
            'prob_mobileNet': prob_mobileNet
            }
    print(data)

    save_result = Result()
    save_result.user_id           = request.form['user_id']
    save_result.image             = name
    save_result.predict_inception = result_inception
    save_result.prob_inception    = prob_inception
    save_result.predict_mobileNet = result_mobileNet
    save_result.prob_mobileNet    = prob_mobileNet
    save_result.save()

    return returnAPI(200, 'Success', data)

def uploaded_file(filename):
    return send_from_directory('uploads', filename)

##*************** HISTORY ***************##

def history():
    args = request.args
    data = Result.where('user_id', args['user_id']).get().serialize()

    for d in range(len(data)):
        data[d]['image_path'] = f"static/uploads/{data[d]['image']}"
    return returnAPI(200, 'Success', data)
