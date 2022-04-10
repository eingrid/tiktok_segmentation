import os
from werkzeug.utils import secure_filename

from flask import redirect, render_template, url_for
from flask import Flask, flash, request 

import numpy as np
import cv2

import tensorflow as tf
from tensorflow.python.ops.numpy_ops import np_config
from keras.preprocessing import image
from keras.models import load_model

np_config.enable_numpy_behavior()



UPLOAD_FOLDER = 'static/uploads'


def add_mask(img,mask):
    
  img = (img).astype(np.uint8)
  mask = mask.astype(np.uint8)

  #create yellow mask
  mask_yellow = np.concatenate([mask*255,mask*255,mask*0],axis=2)

  #create mask of a person
  mask_person = cv2.bitwise_and(img,img,mask=mask)

  #create mask of backgroung
  mask_background = cv2.bitwise_and(img,img,mask=cv2.threshold(cv2.bitwise_not(mask), 0, 255, cv2.THRESH_OTSU)[1])
  
  #add yellow color to a human mask
  dst = cv2.addWeighted(mask_person, 0.6, mask_yellow, 0.4, 0.0)
 
  #add human mask and background mask to ger resulted image
  return cv2.add(dst,mask_background)

app = Flask(__name__)

def load_model_from_file():
    myModel = load_model("/mnt/Dev/Study_Mentorship/TASK3/main_model2")
    return myModel  

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'GET' :
        return render_template('index.html')
    else: 
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
       
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('uploaded_file',filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Load image, show masked image and original image. 
    """

    myModel = app.config['MODEL']

    image_src = UPLOAD_FOLDER+'/'+filename
    seg_src = '/' + UPLOAD_FOLDER+'/seg'+filename


    img = image.load_img(image_src,color_mode='rgb')
    img = tf.image.resize(image.img_to_array(img),(960,640)).numpy()
    img_copy =  img

    img = img/255.0
    img_reshaped = img.reshape((-1,960,640,3))
    
    result = add_mask(img_copy,myModel(img_reshaped)[0][:,:,1].numpy().reshape((960,640,-1)) > 0.5)

    tf.keras.utils.save_img(UPLOAD_FOLDER+'/seg'+filename,result)
    tf.keras.utils.save_img(image_src,img_copy)
   
    image_src = '/' + image_src
    answer = f'''
        <div class='row'>
            <div class='column'>
                <img width='566' height='955'  src={image_src} class='img-thumbnail'/>
            </div>
            <div class='column'>
                <img width='566' height='955'  src={seg_src} class='img-thumbnail'/>
            </div>
        </div>'''
    results.append(answer)
    return render_template('index.html',len=len(results),results = results) 

def main():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    myModel = load_model_from_file()    

    app.config['MODEL'] = myModel
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run()

results = []

main()