import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirebaseClient():

    def __init__(self):
        cred = credentials.Certificate("/Users/ima/dev/random-files/firebase_key.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'atb-hackathon-2020',
        })
        self.db = firestore.client()


    '''
    :param data: a json of data which will be saved to firebase
    :param col_name: the collection name
    :param doc_name: document name aka the "key" of the data
    '''
    def set(self, data, col_name, doc_name):
        try:
            db_pointer = self.db.collection(col_name).document(doc_name)
            db_pointer.set(data)
            return True
        except Exception as e:
            print(e)
            return False

    '''
    :param col_name: name of which column you want to spit all the data out
    '''
    def get_all(self, col_name):
        db_pointer = self.db.collection(col_name)
        return_data = db_pointer.stream()
        return_json = {}
        for row in return_data:
            return_json[row.id] = row.to_dict()
        return return_json

    '''
    :param col_name: name of which column you want to target
    :param doc_name: "key" value within the column
    '''
    def get(self, col_name, doc_name):
        return_data = self.db.collection(col_name).document(doc_name).get()
        return_json = {return_data.id: return_data.to_dict()}
        return return_json