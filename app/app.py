#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import io
import PIL
from PIL import Image
import simplejson
import traceback
import base64
import uuid
import imutils


from flask import Flask, request, render_template, redirect, url_for, send_file, send_from_directory, g, abort, flash, make_response
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename

from lib.upload_file import uploadfile
from lib.histogramManager import histogramManager
from lib.luminanceManager import luminanceManager
from lib.mergeManager import mergeManager
from lib.isometricsManager import isometricsManager
from lib.noisefilterManager import noisefilterManager
from lib.panoramaManager import panoramaManager

#


import random
import StringIO

import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

##

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['WORKING_FOLDER'] = 'static/data_tmp/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #50MB

ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg', 'bmp'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print traceback.format_exc()
        return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                files.save(uploaded_file_path)

                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename)
                
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)
                
                im=Image.open(uploaded_file_path)
                wi,he = im.size # (width,height) tuple
                

                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size, not_allowed_msg="", width=wi,height=he)
            
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        """
        # get all file in ./data directory
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())
        """    
        
        file_display = getFileDisplay()

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('filemanager'))

def getFileDisplay():
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], f)
            size = os.path.getsize(filePath)
            im=Image.open(filePath)
            wi,he = im.size # (width,height) tuple
            file_saved = uploadfile(name=f, size=size,not_allowed_msg="", width=wi,height=he)
            file_display.append(file_saved.get_file())
        
        return file_display

@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/filemanager', methods=['GET', 'POST'])
def filemanager():
    return render_template('filemanager.html')
    

@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    return render_template('histogram.html')

@app.route("/histogram/<string:filename>/<string:typeClr>/<int:channel>", methods=['GET'])
def get_histogram(filename, typeClr, channel):
    t = 0 if typeClr=='grey' else 1
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename),t) # grey scale
    hm = histogramManager()
    canvas = hm.buildCDF(img, channel, filename + " color:" + typeClr + " channel:" + str(channel))
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/luminance', methods=['GET', 'POST'])
def luminance():
    return render_template('luminance.html')

@app.route("/negative/<string:filename>", methods=['GET'])
def get_negative(filename):
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename),1) # grey scale
    lm = luminanceManager()
    imgN = lm.negative(img)
    retval, buffer = cv2.imencode('.jpg', imgN)
    response = make_response(buffer.tobytes())
    
    response.mimetype = 'image/jpg'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response
    
@app.route("/luminance/<string:filename>", methods=['GET'])
def get_luminance(filename):
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename),1) # grey scale
    lm = luminanceManager()
    add = request.args.get('add')
    lumin = lm.addLuminance(img, int(add))
 
    retval, buffer = cv2.imencode('.jpg', lumin)
    response = make_response(buffer.tobytes())
    
    response.mimetype = 'image/jpg'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response    


@app.route('/merge', methods=['GET', 'POST'])
def merge():
    file_display = getFileDisplay()
    return render_template('merge.html', result =file_display)

@app.route('/merge2img', methods=['POST'])
def merge2img():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    app.logger.info(selectedImg)
    if(selectedImgLen <2):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    filenameSecond = selectedImg[1]
    imgSecond = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameSecond),1) # grey scale
    
    rows01, cols01, channels= imgFirst.shape
    rows02, cols02, channels = imgSecond.shape
    if(rows01 != rows02):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images with same height..."})

    if(cols01 != cols02):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images with same width..."})

    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    a= 0.5
    imgResult = cv2.addWeighted(imgFirst,a,imgSecond,1-a,0)
    cv2.imwrite(outputFilePath,imgResult)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})

@app.route('/threshold', methods=['POST'])
def threshold():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    threshold_val = request.form.get("threshold_val")
    app.logger.info("threshold_val:" + threshold_val)
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),0) # grey scale
    #rows01, cols01, channels= imgFirst.shape
    
    hm = histogramManager()
    fig = hm.getThresholdCanvas(imgFirst, int(threshold_val))
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    fig.savefig(outputFilePath)
    #cv2.imwrite(outputFilePath,output)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})


@app.route('/boundingbox', methods=['GET', 'POST'])
def boundingbox():
    file_display = getFileDisplay()
    return render_template('boundingbox.html', result =file_display)
    

@app.route('/isometrics', methods=['GET', 'POST'])
def isometrics():
    file_display = getFileDisplay()
    return render_template('isometrics.html', result =file_display)    
    
@app.route('/translate', methods=['POST'])
def translate():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    transx = request.form.get("transx")
    app.logger.info("transx:" + transx)
    transy = request.form.get("transy")
    app.logger.info("transy:" + transy)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    im = isometricsManager()
    fig = im.translation(imgFirst, int(transx), int(transy))
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})  
    
@app.route('/rotate', methods=['POST'])
def rotate():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    rotateVal = request.form.get("rotate")
    app.logger.info("rotate:" + rotateVal)
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    im = isometricsManager()
    fig = im.rotation(imgFirst, int(rotateVal))
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})    

@app.route('/noisefilter', methods=['GET', 'POST'])
def noisefilter():
    file_display = getFileDisplay()
    return render_template('noisefilter.html', result =file_display)


@app.route('/meanfilter', methods=['POST'])
def meanfilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.mean(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})   

@app.route('/medianfilter', methods=['POST'])
def medianfilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.median(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})        
    
@app.route('/gaussianFilter', methods=['POST'])
def gaussianFilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.gaussianFilter(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})        
   
@app.route('/otsuFilter', methods=['POST'])
def otsuFilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.otsuFilter(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"}) 
    
@app.route('/adaptiveGaussianFilter', methods=['POST'])
def adaptiveGaussianFilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),0) # grey scale
    #rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.adaptiveMeanFilter(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})  
    
@app.route('/bilateralFilter', methods=['POST'])
def bilateralFilter():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    
    #rotateVal = request.form.get("rotate")
    #app.logger.info("rotate:" + rotateVal)
    
    app.logger.info("selectedImg:"+str(selectedImg))
    if(selectedImgLen <1):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 1 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    rows01, cols01, channels= imgFirst.shape
    
    nm = noisefilterManager()
    fig = nm.bilateralFilter(imgFirst)
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

    #fig.savefig(outputFilePath)
    cv2.imwrite(outputFilePath,fig)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})        
    
@app.route('/mosaik', methods=['GET', 'POST'])
def mosaik():
    file_display = getFileDisplay()
    return render_template('mosaik.html', result =file_display)

@app.route('/stitch', methods=['POST'])
def stich():
    selectedImg = request.form.getlist("delete")
    selectedImgLen = len(selectedImg)
    app.logger.info(selectedImg)
    if(selectedImgLen <2):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images..."})
        
    app.logger.info(selectedImg)
    filenameFirst = selectedImg[0]
    imgFirst = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameFirst),1) # grey scale
    filenameSecond = selectedImg[1]
    imgSecond = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filenameSecond),1) # grey scale
    
    """
    rows01, cols01, channels= imgFirst.shape
    rows02, cols02, channels = imgSecond.shape
    if(rows01 != rows02):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images with same height..."})

    if(cols01 != cols02):
        return simplejson.dumps({"imgPath": "", "result":0, "msg":"Error, select at least 2 images with same width..."})
    """
    
    outputFileName = str(uuid.uuid4())+"_"+filenameFirst
    outputFilePath = os.path.join(app.config['WORKING_FOLDER'], str(uuid.uuid4())+"_"+outputFileName)

 
    imageA = imutils.resize(imgFirst, width=400)
    imageB = imutils.resize(imgSecond, width=400)
    
    # stitch the images together to create a panorama
    pm = panoramaManager()
    (result, vis) = pm.stitch([imageA, imageB], showMatches=True)
    cv2.imwrite(outputFilePath,result)
    
    return simplejson.dumps({"imgPath": outputFilePath, "result":1, "msg":"OK"})  
    

#START
if __name__ == '__main__':
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port, debug=True)
    app.logger.info("Starting flask app on %s:%s", host, port)
    #app.run(debug=True)
