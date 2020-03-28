from flask import (
    Flask,
    abort,
    request,
    render_template,
    jsonify
)
import json
import os
import sys
from mongo import mongoDB
import ast

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# 所有 【 非屋主自行刊登 】 的租屋物件
@app.route('/identification', methods=['GET'])
def get_identification():
  house = mongoDB('house')
  output = []
  # {"username" : {$regex : ".*son.*"}}
  for s in house.search({ "name": {$not:{/屋主.*/ }}} ):
    output.append({'hid':s['hid'],'region':s['region'],'name':s['name']})
  return json.dumps({'result' : output},ensure_ascii=False)


#  【 臺北 】【 屋主為女性 】【 姓氏 為吳 】 所刊登的所有租屋 物件
@app.route('/condition', methods=['GET'])
def get_condition():
  house = mongoDB('house')
  output = []
  # {"username" : {$regex : ".*son.*"}}
  for s in house.search({"region":"花蓮縣","name":/^吳小姐.*/}):
    output.append({'hid':s['hid'],'region':s['region'],'name':s['name']})
  return json.dumps({'result' : output},ensure_ascii=False)


# # 以 【 聯絡電話 】 查詢租屋物件
@app.route('/dialPhone/', methods=['GET'])
def get_dialPhone(dialPhone):
  house = mongoDB('house')
  output = []
  for s in house.search({'dialPhone' : dialPhone}):
    output.append({'hid':s['hid'],'address':s['address'],'dialPhone' : s['dialPhone']})
  return json.dumps({'result' : output},ensure_ascii=False)


# # 【 男生可承租 】 且 【 位於新北 】 的租屋物件
@app.route('/region_male', methods=['GET'])
def get_region_male():
  house = mongoDB('house')
  output = []
  # {"username" : {$regex : ".*son.*"}}
  for s in house.search({"region":"花蓮縣","gender":/.*男.*/}):
    output.append({'hid':s['hid'],'region':s['region'],'gender':s['gender']})
#   return json.dumps({'result' : output},ensure_ascii=False)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)