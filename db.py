import mysql.connector

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
        print("get the patient with id if exists")

