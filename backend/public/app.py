from flask import Flask
from flask_restplus import Resource, Api
import requests
import os
app = Flask(__name__)
api = Api(app)

@api.route('/api/hello')
class HelloWorld(Resource):
    def get(self):
        token = os.getenv('ATB_TOKEN')
        test = { 'Authorization' : 'DirectLogin token=' }
        data = requests.get("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/atms", headers=test)
        return {'lil_shit': data.content}
        # return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
