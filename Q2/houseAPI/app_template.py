from flask import (
    Flask,
    abort,
    request,
    render_template,
)
import json
import os
import sys
from search import *
from parseInput import *
from getBbox import get_bbox
from mongoCli import mongoDB, vlg_bound
import ast


port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/corp_demo", methods=["GET"])
def corp_demo():
    return render_template("corp_demo.html")


@app.route("/api/CODE3_list", methods=["GET", "POST"])
def get_CODE3():
    if request.method=="POST":
        request_data = request.get_json()
        data_type = "map"
    else:
        request_data = request.args
        data_type = "list"

    try:
        parsed = parse_input(request_data)
    except Exception as e:
        abort(400, {"message": "parsing fail: " + str(e)})
    else:
        x, y, num, unit, filters = parsed
      
    try:
        #CODE3 = q_es(float(x), float(y), num, data_type, filters)
        CODE3 = find_CODE3(float(x), float(y), num, filters, data_type)
        bbox = get_bbox(CODE3)
        json_string = json.dumps(
            {"CODE3_list": CODE3, "x": x, "y": y, "bbox": bbox}, ensure_ascii=False
        )
        #print(json_string, flush=True)
    except Exception as e:
        print(str(e),flush=True)
        abort(400, {"message": str(e)})

    return json_string


@app.route("/api/CODE3_list_batch", methods=["GET"])
def get_CODE3_batch():
    request_data = request.get_json()
    #print(f"request_data: {request_data}")

    coord_ls = request_data["coordinates"]
    filters = parse_filters(request_data['filters'])
    distance, unit = parse_distance(request_data["distance"])
    data_type = 'list' if "data_type" not in list(request_data.keys()) else request_data["data_type"]
    code3_ls = []
    data_ls = []
    
    for coord in coord_ls:
        x, y = parse_coords(coord[0], coord[1])
        code3 = find_CODE3(
            float(x), float(y), 
            float(distance), 
            filters,
            data_type)
        for c in code3:
            if c["attributes"]["CODE3"] not in code3_ls:
                code3_ls.append(c["attributes"]["CODE3"])
                data_ls.append(c)
    
    return json.dumps({"CODE3_list":data_ls}, ensure_ascii=False)


@app.route("/api/csv", methods=["GET"])
def return_csv():
    # to do: 2. return a csv file

    return None


@app.route("/api/county_ls", methods=["POST"])
def get_county_ls():
    return json.dumps({"COUN_NA_ls" : min_stat.distinct("attributes.COUN_NA")})


@app.route("/get_vlg_bound", methods=["GET","POST"])
def get_vlg_bound():
    fetch_data = request.get_json()
    q = {}
    if fetch_data:
        county_filter = fetch_data["filter"]
        
        q = { "attributes.COUNTYNAME":{"$in" : [c for c in county_filter]}}
    
    vlg_bound_ls= [v for v in vlg_bound.find(q, {"_id":False})]
    
    
    return json.dumps({"vlg_bound_ls":vlg_bound_ls})


@app.route("/get_corp", methods=["GET","POST"])
def get_corp():
    fetch_data = request.get_json()
    
    filter_field = fetch_data["filter"]
    #es_bmc_corp = esIndex('bmc_corp')
    #corp_ls = es_bmc_corp.get_corp(filter_field  = filter_field)
    md_bmv_corp = mongoDB('bmc_corp')
    q={key: { "$regex" : f"{val}"} for key, val in filter_field.items()}

    corp_ls = md_bmv_corp.search(q)

    corp_ls = {"hits":{"hits":[{"_source":r} for r in corp_ls]}}

    corp_ls_geojson = [{ 
        "type" : "Feature",
        "geometry" : { 
        "coordinates" : i['_source']['LOCATION'], 
        "type":"Point",
        }
    } for i in corp_ls['hits']['hits']]

    try:
        corp_ls_response = {
            "type": "FeatureCollection",
            "crs": {"init": "epsg:4326"},
            "name": "corp_ls",
            "features": corp_ls_geojson
        }
    except Exception as e:
        corp_ls_response = {}
        print(e)
    return json.dumps(corp_ls_response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)