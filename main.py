from re import search
import flask
from flask import Flask, app, json, jsonify, request
from flask.templating import render_template
import pymongo
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = pymongo.MongoClient('mongodb+srv://zulqarnain:zulqiawan@cluster0.afsfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.iot
col = db.switches

app = Flask(__name__)

#HTML file
@app.route('/')
def index():
    return render_template('index.html')

#HTML file
@app.route('/api/test')
def index():
    return "<h1> It works </h1>"

#Get switches info from database
@app.route('/api/getswitches', methods = ['GET'])
def getswitches():
    
    switches = col.find({}, {'_id':0})
    switches_list = []
    for switch in switches:
        switches_list.append(switch)
    sw_js = JSONEncoder().encode(switches_list)
    return sw_js

#Update switches detail in database
@app.route('/api/updateswitch/<int:switch_id>', methods = ['POST' ,'GET'])
def updateswitch(switch_id):

    search = {'switch_id':switch_id}

    for switch in col.find({'switch_id': switch_id}):
        if switch['status'] == False:
            new_status = {'$set': {'status': True}}
            col.update(search, new_status)

        elif switch['status'] == True:
            new_status = {'$set': {'status': False}}
            col.update(search, new_status)

    for sw_id in col.find({'switch_id': switch_id}):
        return JSONEncoder().encode(sw_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)