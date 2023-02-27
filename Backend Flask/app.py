from flask import Flask, flash, redirect, render_template, request, jsonify, send_file
import os, cgi, openai, time, json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from script import *
from backend import zip_to_result
import zipfile

app = Flask(__name__)
cors = CORS(app)

uploaded_file = ''

openai.api_key = 'your api key here'

@app.route("/")
def data():
    return render_template("form.html")

@app.route('/shortenurl')
def shortenurl():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= request.args['shortcode'],
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return render_template("shortenurl.html", response = response.choices[0].text)


@app.route("/upload", methods=['GET'])
def upload_file():
    return render_template("upload.html")   


def generateResponse(classes_interfaces):
  res={}
  for i in classes_interfaces:
    res[i]={}
    for j in classes_interfaces[i]:
      cmd=""
      if i=='controllers':
         cmd="convert this java code to flask python :"
      elif i=="entities":
         cmd="convert this to python class :"
      elif i=="repositories":
         cmd= "convert this to python using sqlAlchemy :"
      elif i=="services":
         cmd= "convert this to python code :"
      response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{cmd} {classes_interfaces[i][j]}",
        temperature=0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
      )
      res[i][j]=response.choices[0].text          
  return res


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
    file = request.files['file']
    if file.filename == '':
        return redirect('http://localhost:3000/')
    uploaded_file =  file.filename
    file.save(secure_filename(file.filename))
    class_interfaces = zip_to_result(uploaded_file)
    payLoad=generateResponse(class_interfaces)

    with open("output.json","w") as f:
        json.dump(payLoad,f)
    generatePythonFiles()  
    zf = zipfile.ZipFile("Output.zip", "w")
    for diir,subdir,fil in os.walk("Dirs"):
        zf.write(diir)
        for fname in fil:
            zf.write(os.path.join(diir,fname))
    # zf.close()
    return redirect('/download')       

@app.route('/download')
def downloadFile ():
    path = "Output.zip"
    return send_file(path, as_attachment=True)
		
if __name__ == '__main__':
   app.run(debug = True)        

 
  
        
