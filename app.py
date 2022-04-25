from flask import Flask,jsonify,request,make_response
from flask_restful import Resource, Api
import flask_sqlalchemy as sqlalchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sqlalchemy.SQLAlchemy(app)

class Employee(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(50))
  lastname = db.Column(db.String(50))
  gender = db.Column(db.String(50))
  salary = db.Column(db.Float)

  def __repr__(self):
    return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"

class GetEmployee(Resource):
  def get(self):
    employees = Employee.query.all()
    emp_list=[]
    for emp in employees:
      emp_data={'Id': emp.id, 'Firstname': emp.firstname,'Lastname': emp.lastname,'Gender':emp.gender,'Salary': emp.salary}
      emp_list.append(emp_data)
    return {'Employees': emp_list},200

class AddEmployee(Resource):
  def post(self):
    if request.is_json:
      emp = Employee(firstname=request.json['Firstname'],lastname=request.json['Lastname'],gender=request.json['Gender'],salary=request.json['Salary'])
      db.session.add(emp)
      db.session.commit()
      return make_response(jsonify({'Id':emp.id,'Firstname':emp.firstname,'Lastname':emp.lastname,'Gender':emp.gender,'Salary':emp.salary}),201)
    else:
      return make_response(jsonify({'Error':'Bad request'}),400)


class UpdateEmployee(Resource):
  def put(self,id):
    if request.is_json:
      emp = Employee.query.get(id)
      if emp is None:
        return make_response(jsonify({'Error':'Employee not found'}),404)
      else:
        emp.firstname = request.json['Firstname']
        emp.lastname = request.json['Lastname']
        emp.Gender = request.json['Gender']
        emp.Salary = request.json['Salary']
        db.session.commit()
        return "Updated",200

class DeleteEmployee(Resource):
  def delete(self,id):
    emp = Employee.query.get(id)
    if emp is None:
      return make_response(jsonify({'Error':'Employee not found'}),404)
    else:
      db.session.delete(emp)
      db.session.commit()
      return f'{id} is Deleted',200
    
api.add_resource(GetEmployee,'/employees')
api.add_resource(AddEmployee,'/employees/add')
api.add_resource(UpdateEmployee,'/employees/update/<int:id>')
api.add_resource(DeleteEmployee,'/employees/delete/<int:id>')


if __name__ == '__main__':
  app.run(debug=True)



