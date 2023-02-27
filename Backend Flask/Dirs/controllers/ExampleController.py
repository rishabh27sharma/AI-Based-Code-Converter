
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/getAllExample', methods=['GET'])
def getAllExample():
    return jsonify(exampleService.getAllExample())

@app.route('/saveExample', methods=['POST'])
def saveExample():
    exampleEntity = request.get_json()
    return jsonify(exampleService.saveExample(exampleEntity))