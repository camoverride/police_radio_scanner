from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS



restful_server = Flask(__name__)
CORS(restful_server)
api = Api(restful_server)


# Define a Resource to serve the contents of data.json
class DataResource(Resource):
    def get(self):
        # Read the contents of data.json
        with open("data.json", "r") as file:
            data = file.read()
        return jsonify(eval(data))

# Add the resource to the API
api.add_resource(DataResource, "/data")


if __name__ == "__main__":
    # Start the restful API, listening on all interfaces
    restful_server.run(host="0.0.0.0", debug=True)
