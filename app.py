from flask import Flask, escape, request, jsonify, abort
from werkzeug.utils import secure_filename
import os, json, urllib
import test as t

app = Flask(__name__)
entities =[]
test_ = {}

#POST TEST
@app.route('/api/tests',methods=['POST'])
def create_test():
    test_data = request.get_json()
    global test_
    test_ = {
            "subject" : test_data["subject"],
            "answer_keys" : test_data['answer_keys']
    }
    t.create_table()
    for i in test_.keys():
        entities.append(test_[i])
    t.insert_into_tests(entities)
    ret_data = t.get_data()
    ret_val = { 
            "test_id" : ret_data[0][0],
            "subject"   : ret_data[0][1],
            "answer_keys": eval(ret_data[0][2]),
            "submissions" : ret_data[0][3]
                }
    return ret_val,201


#POST Scantron Submission
@app.route('/api/tests/<test_id>/scantrons',methods=['POST'])
def upload_scantron(test_id):
    scr,res,entries = 0,dict(),[]

    t_id = request.view_args['test_id']
    f = request.files['data']

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLD = '/Users/admin/Desktop/'
    UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename("scantron.json")))
    f.seek(0)
    
    in_data = json.loads(f.read())    
    entries =[in_data['name'], in_data['subject'], in_data['answers']]

    s_id = t.insert_into_scantrons(t_id, entries)   
    data = t.get_answer_key(t_id)
    data = eval(data[0][0])
    
    for i  in data.keys():
        res[i] =    {
                    "actual": data[i],
                    "expected": in_data['answers'][i]
                    }
        if data[i] == in_data['answers'][i]:
            scr+=1

    ret ={
        "scantron_id": s_id[0],
        "scantron_url": "http://localhost:5000/files/scantron-1.json",
        "name": in_data['name'],
        "subject": in_data['subject'],
        "score": scr,
        "result" : res
        }

    return ret,201


  
@app.route('/api/tests/<test_id>', methods=['GET'])
def get_submissions(test_id):
    t_id = request.view_args['test_id']
    data = t.get_sub_data(t_id)
    res =dict()
    scr= 0
    count = 0
    subb = {}
    ans = eval(data[0][2])
    subb = eval(data[0][7])
    print(type(ans))
    print(type(subb))

    for i  in ans.keys():
        print("Print i", i, ans[i], subb[i])
        res[i] =    {
                    "actual": ans[i],
                    "expected": subb[i]
                    }
        if ans[i] == subb[i]:
            scr+=1
        count += 1

    rev ={
         "test_id" : test_id,
         "Subject" : data[0][1],
         "answer_keys" : eval(data[0][2]),
         "Submissions" : [
             {
                "scantron_id": data[0][4],
                "scantron_url": "http://localhost:5000/files/scantron-1.json",
                "name": data[0][5],
                "subject": data[0][6],
                "score": scr,
                "result" : res
             }
         ]
     }

    return rev,201




