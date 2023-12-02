from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('people', user='poowoo', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Person(BaseModel):
  name = CharField()
  age = IntegerField()

db.connect()
db.drop_tables([Person])
db.create_tables([Person])

Person(name='Raul', age=1000).save()
Person(name='Chris', age=1000).save()
Person(name='Mega Hawk', age=9999).save()

app = Flask(__name__)

@app.route('/person/', methods=['GET', 'POST'])
@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Person.get(Person.id == id)))
    else:
        people_list = []
        for person in Person.select():
            people_list.append(model_to_dict(person))
        return jsonify(people_list)

  if request.method =='PUT':
    body = request.get_json()
    Person.update(body).where(Person.id == id).execute()
    return "Person " + str(id) + " has been updated."

  if request.method == 'POST':
    new_person = dict_to_model(Person, request.get_json())
    new_person.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Person.delete().where(Person.id == id).execute()
    return "Person " + str(id) + " deleted."

app.run(debug=True, port=9000)
