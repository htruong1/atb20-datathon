from flask import Flask, request
from flask_restplus import Resource, Api
from backend.utils.requestutil import atbRequests
from backend.utils.firebaseutil import FirebaseClient
from flask_restplus import reqparse

parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app, title='ATB Hackathon API', description='Web interface version of API')
fb_client = FirebaseClient()
atb_requests = atbRequests()

@api.route('/api/user')
class User(Resource):

    @api.doc("Retrieve all data based on user_id", params={'id': 'A user ID'})
    def get(self):
        user_id = request.args.get("id")
        print('Retrieving data for user: {}'.format(user_id))
        return {'future':'data_endpoint'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
