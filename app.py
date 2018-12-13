import os

from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import csv
import json

app = Flask(__name__)
api = Api(app)


ifsc_lookup_map = {}
citywise_branch_lookup_map = {}

with open('bank_branches.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if line_count!=0:
            branch = {"ifsc": row[0], "bank_id": row[1], "branch" : row[2], "address": row[3], "city": row[4], "district": row[5], "state" : row[6], "bank_name": row[7]}
            ifsc_lookup_map[row[0]] = branch

            if row[7] in citywise_branch_lookup_map:
                city_map = citywise_branch_lookup_map[row[7]]
                if row[4] in city_map:
                    branches_list = []
                    branches_list = city_map[row[4]]
                    branches_list.append(branch)
                else:
                    branches_list = []
                    branches_list.append(branch)
                city_map[row[4]] = branches_list
                citywise_branch_lookup_map[row[7]]  =  city_map
            else:
                branches_list = []
                branches_list.append(branch)
                city_map = {}
                city_map[row[4]] = branches_list
                citywise_branch_lookup_map[row[7]] = city_map



class UserResource(Resource):
    def get(self, user_id):
        return "Hello"


class Ifsc(Resource):
    def get(self, name):
        if name in ifsc_lookup_map:
            return ifsc_lookup_map[name], 200
        else:
            return "Ifsc not found", 404

class CityWise(Resource):
    def get(self, bank, city):
        if bank in citywise_branch_lookup_map and city in citywise_branch_lookup_map[bank]:
            return citywise_branch_lookup_map[bank][city], 200
        else:
            return "Not found", 404

      
api.add_resource(Ifsc, "/banks/ifsc-code/<string:name>")
api.add_resource(CityWise, "/banks/<string:bank>/cities/<string:city>/")




api.add_resource(UserResource, '/users/<user_id>/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
