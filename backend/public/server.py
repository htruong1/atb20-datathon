from flask import Flask
from flask_restplus import Resource, Api
from backend.utils.requestutil import atbRequests
from backend.utils.firebaseutil import FirebaseClient

app = Flask(__name__)
api = Api(app)
fb_client = FirebaseClient()
atb_requests = atbRequests()

@api.route('/api/hello')
class HelloWorld(Resource):
    def get(self):
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/atms")
        return response

@api.route('/api/bank/accounts')
class GetCustomers(Resource):
    def get(self):
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts" )
        return response


if __name__ == '__main__':
    app.run(debug=True)
