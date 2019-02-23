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

    def getProcedures(self):
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

    def getProcedure(self, id):
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
