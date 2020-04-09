from flask import Flask, request
from flask_restful import Resource, Api
from flask_mail import Mail, Message

app = Flask(__name__)
api = Api(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'chronicletest3000@gmail.com',
    MAIL_PASSWORD = 'chronicle1234!',
))


mail = Mail(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Emails(Resource):

    def post(self):
        req_data = request.get_json()
        msg = Message("Hello", sender="chronicletest3000@gmail.com", recipients=["xym.yao@gmail.com"])
        msg.body = "testing"
        msg.html = '<img src="http://localhost:5001/static/img/square.gif?monopolymaster@gmail.com&1">'
        mail.send(msg)

api.add_resource(HelloWorld, '/')
api.add_resource(Emails, '/email')

if __name__ == '__main__':
    app.run(debug=True)