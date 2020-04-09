from flask import Flask, request, Response
from flask_restful import Resource, Api
from datetime import datetime
import pg8000, os

app = Flask(__name__)
api = Api(app)

host = 'chronicle.civ3etippyfn.us-east-1.rds.amazonaws.com'
database = 'communications'

password = os.environ['DB_PASSWORD']

conn = pg8000.connect(user="postgres", password=password, host=host, port=5432, database=database)
cursor = conn.cursor()
INSERT_QUERY = 'INSERT INTO communications (name, contact, comm_type, message, campaign_id, message_id, is_read, created_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
UPDATE_QUERY = 'UPDATE communications set is_read=%s, updated_ts=%s where message_id=%s'

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'database'}

class Actions(Resource):
    def post(self):
        req_data = request.get_json()
        print(str(req_data))
        try:
            name, contact, comm_type, message, campaign_id, message_id, is_read, created_ts = req_data['name'], req_data['contact'], req_data['comm_type'], req_data['message'], req_data['campaign_id'], req_data['message_id'], 'N', datetime.now()
            cursor.execute(INSERT_QUERY, (name, contact, comm_type, message, campaign_id, message_id, is_read, created_ts))
            conn.commit()
            return Response('{"message": "successfully created new entry"}', status=201, mimetype='application/json')
        except KeyError as e:
            error_message = "KeyError on " + str(e)
        return Response('{"error_message": "' + error_message + '"}', status=400, mimetype='application/json')

    def put(self):
        req_data = request.get_json()
        try:
            message_id, is_read, updated_ts = req_data['message_id'], 'Y', datetime.now()
            cursor.execute(UPDATE_QUERY, (is_read, updated_ts, message_id))
            conn.commit()
            return Response('{"message": "successfully updated entry"}', status=200, mimetype='application/json')
        except KeyError as e:
            error_message = "KeyError on " + str(e)
            return Response('{"error_message": "' + error_message + '"}', status=400, mimetype='application/json')


api.add_resource(Actions, '/alter')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
