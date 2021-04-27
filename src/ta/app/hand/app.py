from flask import Flask
from flask_restful import Api

from ImageController import SendImage


app = Flask(__name__)
api = Api(app)

api.add_resource(SendImage, '/hand')


if __name__ == '__main__':
    app.run()

