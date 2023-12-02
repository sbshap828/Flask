from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('building', user='poowoo', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Building(BaseModel):
  name = CharField()
  bldgnum=CharField()
  address=CharField()
  coop=BooleanField()
  managerid=IntegerField()


db.connect()
db.drop_tables([Building])
db.create_tables([Building])

Building(name='Colorado',bldgnum='123',address='123 mains',coop=True, managerid=1000).save()
Building(name='Phoenix',bldgnum='234', address='133 mains',coop=False,managerid=1000).save()
Building(name='Bentley',bldgnum='345', address='355 mains',coop=True,managerid=9999).save()

app = Flask(__name__)

@app.route('/building/', methods=['GET', 'POST'])
@app.route('/building/<id>', methods=['GET', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Building.get(Building.id == id)))
    else:
        building_list = []
        for building in Building.select():
            building_list.append(model_to_dict(building))
        return jsonify(building_list)


  if request.method == 'POST':
    new_building = dict_to_model(Building, request.get_json())
    new_building.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Building.delete().where(Building.id == id).execute()
    return "Building " + str(id) + " deleted."

app.run(debug=True, port=9001)
