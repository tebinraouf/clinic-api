from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/api/v1.0/patients", methods=["GET"])
def getPatients():
    '''
        Get all the patients

        Returns:
            a list of patient objects
    '''
    return jsonify({'patients': [make_public_patient(patient) for patient in patients]})
 
@app.route("/api/v1.0/patients/<int:patientID>", methods=["GET"])
def getPatient(patientID):
    '''
        Get a patient by ID

        Parameter:
            - patientID: the ID of the patient

        Returns:
            a patient object
    '''
    patient = [patient for patient in patients if patient['id'] == patientID]
    if len(patient) == 0:
        abort(404)
    return jsonify({'patient': make_public_patient(patient[0])})

@app.route("/api/v1.0/patients", methods=["POST"])
def createPatient():
    '''
        Create a new patient through a POST method. Takes a JSON object


        Returns:
            The newly created patient.
    '''
    if not request.json or not 'firstName' in request.json:
        abort(400)
    print(request.json)
    patient = {
        'id': patients[-1]['id'] + 1,
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
        'age': request.json['age']
    }
    patients.append(patient)
    return jsonify({'patient': patient}), 201

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