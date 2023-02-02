from flask import Flask, request
from flask_restful import Resource, Api
import datetime


app = Flask(__name__)
api = Api(app)


class tracker(Resource):

    def get(self):
        return {'msg': 'Hello World'}

    def post(self):
        payload = request.get_json()
        mail_id = payload['mail_id']
        TrackerTime().add_time_to_file(mail_id)
        return {'msg': 'recived mail_id: {}'.format(mail_id)}


class TrackerTime:
    def add_time_to_file(self, mail_id):
        with open('time.txt', 'a') as f:
            f.write(str(mail_id) + '\n')
            f.write(str(datetime.datetime.now()) + '\n')
            f.write('------------------------' + '\n')


api.add_resource(tracker, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
