from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from db import DBConnector

app = Flask(__name__)


@app.route("/dbtest", methods=['GET'])
def dbtest():
    db = DBConnector()
     
    return jsonify({'patient': db.getPatient(7)})
    

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'clinic-secret-key'
jwt = JWTManager(app)


@app.route('/login', methods=['GET'])
def login():
    access_token = create_access_token(identity='tebin')
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

patients = [
    {
        'id': 1,
        'firstName': 'John',
        'lastName': 'Smith', 
        'age': 25
    },
    {
        'id': 2,
        'firstName': 'Jane',
        'lastName': 'Mike', 
        'age': 27
    }
]
####                        #####
####        ERROR           #####
####                        #####
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



####                        #####
####        GET ALL         #####
####                        #####
@app.route("/api/v1.0/patients", methods=["GET"])
def getPatients():
    '''
        Get all the patients

        Returns:
            a list of patient objects
    '''
    db = DBConnector()
    result = db.getPatients()
    db.close()
    return jsonify({'patients': [make_public_patient(patient) for patient in result]})

@app.route("/api/v1.0/procedures", methods=["GET"])
def getProcedures():
    db = DBConnector()
    result = db.getProcedures()
    db.close()
    return jsonify({'procedures': result})

@app.route("/api/v1.0/procedureTypes", methods=["GET"])
def getProcedureTypes():
    db = DBConnector()
    result = db.getProcedureTypes()
    db.close()
    return jsonify({'types': result})

####                        #####
####        GET BY ID       #####
####                        #####
@app.route("/api/v1.0/patients/<int:patientID>", methods=["GET"])
def getPatient(patientID):
    '''
        Get a patient by ID

        Parameter:
            - patientID: the ID of the patient

        Returns:
            a patient object
    '''
    db = DBConnector()
    result = db.getPatient(patientID)
    if len(result) == 0:
        abort(404)
    db.close()
    return jsonify({'patient': make_public_patient(result)})

@app.route("/api/v1.0/procedures/<int:procedureID>", methods=["GET"])
def getProcedure(procedureID):
    db = DBConnector()
    result = db.getProcedure(procedureID)
    if len(result) == 0:
        abort(404)
    db.close()
    return jsonify({'procedure': result})

@app.route("/api/v1.0/procedures/patients/<int:patientID>", methods=["GET"])
def getProcedureByPatient(patientID):
    db = DBConnector()
    result = db.getProcedureByPatient(patientID)
    if len(result) == 0:
        abort(404) 
    db.close()
    return jsonify({'procedures': result})

@app.route("/api/v1.0/procedureTypes/<int:typeID>", methods=["GET"])
def getProcedureType(typeID):
    db = DBConnector()
    result = db.getProcedureType(typeID)
    if len(result) == 0:
        abort(404)
    db.close()
    return jsonify({'type': result})






####                        #####
####        CREATE          #####
####                        #####
@app.route("/api/v1.0/patients", methods=["POST"])
def createPatient():
    '''
        Create a new patient through a POST method. Takes a JSON object


        Returns:
            The newly created patient.
    '''
    json = request.json
    if not json or not 'firstName' in json:
        abort(400)    
    lastName = '' if not json.get('lastName') else json.get('lastName')
    mobile = '' if not json.get('mobile') else json.get('mobile')
    gender = '' if not json.get('gender') else json.get('gender')
    email = '' if not json.get('email') else json.get('email')
    note = '' if not json.get('note') else json.get('note')
    storageID = '' if not json.get('storageID') else json.get('storageID')
    date = '' if not json.get('date') else json.get('date')
    age = 0 if not json.get('age') else json.get('age')

    patient = {
        'firstName': request.json['firstName'],
        'lastName': lastName,
        'mobile' : mobile,
        'gender' : gender,
        'email' : email,
        'note' : note,
        'storageID' : storageID,
        'date' : date,
        'age' : age
    }
    db = DBConnector()
    result = db.createPatient(patient)
    db.close()
    return jsonify({'patient': result}), 201





####                        #####
####        UPDATE          #####
####                        #####
@app.route("/api/v1.0/patients/<int:patientID>", methods=["PUT"])
def updatePatient(patientID):
    '''
        Update a patient with ID. Takes a JSON object in a PUT method

        Parameter:
            - patientID: the ID of the patient. 
        Returns:
            The updated patient.
    '''
    patientObjc = [patient for patient in patients if patient['id'] == patientID]
    if len(patientObjc) == 0:
        abort(404)
    if not request.json:
        abort(400)
    patient = patientObjc[0]
    patient['firstName'] = request.json.get('firstName', patient['firstName'])
    patient['lastName'] = request.json.get('lastName', patient['lastName'])
    patient['age'] = request.json.get('age', patient['age'])
    return jsonify({'patient': patient})




####                        #####
####        DELETE          #####
####                        #####
@app.route("/api/v1.0/patients/<int:patientID>", methods=["DELETE"])
def deletePatient(patientID):
    '''
        Delete a patient with ID

        Parameter:
            - patientID: the ID of the patient to be deleted.
        Returns:
            - The deleted patient
    '''
    patientObjc = [patient for patient in patients if patient['id'] == patientID]
    if len(patientObjc) == 0:
        abort(404)
    patients.remove(patientObjc[0])
    return jsonify({'result': True})


def make_public_patient(patient):
    '''
        A utility function to make visible URI for each patient object

        Parameter:
            - patient: a patient object
        
        Returns:
            - a new patient object with its uri
    '''
    new_patient = {}
    for field in patient:
        if field == 'id':
            new_patient['uri'] = url_for('getPatient', patientID=patient['id'], _external=True)
        else:
            new_patient[field] = patient[field]
    return new_patient

if __name__ == "__main__":
    app.run()