import mysql.connector
from flask import abort

class DBConnector:
    def __init__(self):
        '''Initialize a connection with the MySQL database'''
        self._connection = mysql.connector.connect(
            user='root', 
            password='root1234', 
            host='127.0.0.1', 
            database='mydb')
        self.cursor = self._connection.cursor(buffered=True)

####                        #####
####        GET ALL         #####
####                        #####
    def getPatients(self):
        '''Get all the patients from the database
        
        Returns:
            [Patient] -- a list of Patient Objects.
            patient = {
                "id": id, 
                "firstName": firstName,
                "lastName": lastName,
                "mobile": mobile,
                "gender": gender,
                "email": email,
                "note": note,
                "storageID": storageID,
                "date": date,
                "age": age
            }

        '''
        query = ("SELECT * FROM Patient")
        self.cursor.execute(query)
        patients = []
        for (id, firstName, lastName, mobile, gender, email, note, storageID, date, age) in self.cursor:
            patient = {
                "id": id, 
                "firstName": firstName,
                "lastName": lastName,
                "mobile": mobile,
                "gender": gender,
                "email": email,
                "note": note,
                "storageID": storageID,
                "date": date,
                "age": age
            }
            patients.append(patient)
        self.cursor.close()
        self._connection.close()
        return patients
    
    def getProcedures(self):
        '''Get all the procedures.
        
        Returns:
            an array of procedure objects
            procedure = {
                "id": id,
                "name": name,
                "price": price,
                "note": note,
                "patientID": patientID,
                "date": date,
                "storageID": storageID
            }
            [procedure]
        '''

        query = ("SELECT * FROM mydb.Procedure")
        self.cursor.execute(query)
        procedures = []
        for (id, note, price, patientID, date, storageID, name) in self.cursor:
            procedure = {
                "id": id,
                "name": name,
                "price": price,
                "note": note,
                "patientID": patientID,
                "date": date,
                "storageID": storageID
            }
            procedures.append(procedure)
        self.cursor.close()
        self._connection.close()
        return procedures

    def getProcedureTypes(self):
        '''Get all procedure types
        
        Returns:
            an array -- an array of all procedure types
        '''
        query = "SELECT * FROM mydb.ProcedureList"
        self.cursor.execute(query)
        proceduresList = []
        for (id, name) in self.cursor:
            aProcedure = {
                "id": id,
                "name": name
            }
            proceduresList.append(aProcedure)
        self.cursor.close()
        self._connection.close()
        return proceduresList
####                        #####
####        GET BY ID       #####
####                        #####
    def getPatient(self, id):
        '''Get a patient with ID
           
        Arguments:
            id {int} -- The id of the patient
        
        Returns:
            a patient object if exists
            patient = {
                "id": id, 
                "firstName": firstName,
                "lastName": lastName,
                "mobile": mobile,
                "gender": gender,
                "email": email,
                "note": note,
                "storageID": storageID,
                "date": date,
                "age": age
            }
        '''

        query = "SELECT * FROM Patient where id=" + str(id)
        self.cursor.execute(query)
        patient = {}
        for (id, firstName, lastName, mobile, gender, email, note, storageID, date, age) in self.cursor:
            patient = {
                "id": id, 
                "firstName": firstName,
                "lastName": lastName,
                "mobile": mobile,
                "gender": gender,
                "email": email,
                "note": note,
                "storageID": storageID,
                "date": date,
                "age": age
            }
        self.cursor.close()
        self._connection.close()
        return patient

    def getProcedure(self, id):
        '''Get a patient's procedure by its own id.
        
        Arguments:
            id {int} -- procedure type id
        
        Returns:
            a patient procedure object -- if the id exists, it returns an object which includes id, name, price, note, patientID, date, and storage ID
            procedure = {
                "id": id,
                "name": name,
                "price": price,
                "note": note,
                "patientID": patientID,
                "date": date,
                "storageID": storageID
            }
        '''
        query = "SELECT * FROM mydb.Procedure WHERE id=" + str(id)
        self.cursor.execute(query)
        procedure = {} 
        for (id, note, price, patientID, date, storageID, name) in self.cursor:
            procedure = {
                "id": id,
                "name": name,
                "price": price,
                "note": note,
                "patientID": patientID,
                "date": date,
                "storageID": storageID
            }
        self.cursor.close()
        self._connection.close()
        return procedure

    def getProcedureByPatient(self, id):
        '''Get all the procedures associated with a patient id
        
        Arguments:
            id {int} -- patient id
        
        Returns:
            an array of procedures -- an array of all procedures of a patient
        '''
        query = "SELECT * FROM mydb.Procedure WHERE patientID=" + str(id)
        self.cursor.execute(query)
        procedures = [] 
        for (id, note, price, patientID, date, storageID, name) in self.cursor:
            procedure = {
                "id": id,
                "name": name,
                "price": price,
                "note": note,
                "patientID": patientID,
                "date": date,
                "storageID": storageID
            }
            procedures.append(procedure)
        self.cursor.close()
        self._connection.close()
        return procedures

    def getProcedureType(self, id):
        '''Get a procedure type by its id
        
        Arguments:
            id {int} -- the id of the procedure type
        
        Returns:
            a type object -- includes id and name of the object
            aType = {
                "id" : id,
                "name": name
            }
        '''
        query = "SELECT * FROM mydb.ProcedureList WHERE id=" + str(id)
        self.cursor.execute(query)
        aType = {}
        for (id, name) in self.cursor:
            aType = {
                "id" : id,
                "name": name
            }
        self.cursor.close()
        self._connection.close()
        return aType