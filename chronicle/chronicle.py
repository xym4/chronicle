from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_mail import Mail, Message
from datetime import datetime
import random, logging, requests, pyshorteners, os

app = Flask(__name__)
api = Api(app)

password = os.environ['EMAIL_PASSWORD']

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='chronicletest3000@gmail.com',
    MAIL_PASSWORD=password,
))

mail = Mail(app)

DB_API_URL = 'http://db-api-108704205.us-east-1.elb.amazonaws.com/alter'
CHRONICLE_API_URL = 'http://chronicle-elb-2118927082.us-east-1.elb.amazonaws.com/static/img/logo.gif'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class ContentDelivery(Resource):

    def post(self):
        req_data = request.get_json()

        name, contact,  comm_type, message, campaign_id, created_ts = req_data['name'], req_data['contact'], req_data['comm_type'], req_data['message'], req_data['campaign_id'], datetime.now()
        message_id = '_'.join([contact, comm_type, campaign_id, str(random.getrandbits(128))])

        if comm_type.upper() == 'PHONE':
            contact = contact + '@mms.att.net'

        try:
            # compose and send email
            msg = Message("Hello", sender="chronicletest3000@gmail.com", recipients=[contact])

            if comm_type.upper() == 'EMAIL':
                img_src = CHRONICLE_API_URL + '?' + message_id
                msg.html = message + '<img src="' + img_src + '">'
            elif comm_type.upper() == 'PHONE':
                s = pyshorteners.Shortener()
                info_link = s.tinyurl.short(CHRONICLE_API_URL + '?' + message_id)
                full_message = info_link + message
                msg = Message(message, sender="chronicletest3000@gmail.com", recipients=[contact])

            mail.send(msg)

            # log message to db
            message_data = {
                'name': name,
                'contact': contact,
                'comm_type': comm_type,
                'message': message,
                'campaign_id': campaign_id,
                'message_id': message_id
            }

            requests.post(DB_API_URL, json=message_data)
            return Response('{"message": "Successfully sent email and updated communications DB"}', status=200, mimetype='application/json')

        except Exception as e:
            return Response('{"error_message": "Could not send email and/or update communications DB", "exception": "' + str(e) + '"}', status=400, mimetype='application/json')

api.add_resource(HelloWorld, '/')
api.add_resource(ContentDelivery, '/delivery')

if __name__ == '__main__':
    logging.basicConfig(filename='chronicle.log', level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=80)
