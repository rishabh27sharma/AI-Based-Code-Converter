import json
import os
import sys
assert('output.json' in os.listdir());
responseData=None
if 'Dirs' not in os.listdir():
	os.mkdir('Dirs')

def generatePythonFiles():
    with open("output.json",'r') as f:
        responseData=json.load(f)
    for i in responseData.keys():
        path=os.path.dirname(__file__)
        if i not in os.listdir('Dirs'):
            os.mkdir(os.path.join('Dirs',i))
        for k in responseData.get(i):
            with open(path+f"/Dirs/{i}/{k}.py","w") as f:
                f.write(responseData.get(i).get(k))    
