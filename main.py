from flask import Flask, request
from flask_restful import Resource, Api
import datetime
import psycopg2
from psycopg2._psycopg import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

from track_orm import MailTrack

app = Flask(__name__)
api = Api(app)

# connect to db
url = 'postgresql://tracker_6oxo_user:vtt49y1VVO7JZQ44R1gWbJQl5LGWAedn@dpg-cfdvljo2i3mmlo4v2ar0-a.oregon-postgres.render.com/tracker_6oxo'
internal_url = 'postgres://tracker_6oxo_user:vtt49y1VVO7JZQ44R1gWbJQl5LGWAedn@dpg-cfdvljo2i3mmlo4v2ar0-a/tracker_6oxo'
test_url = 'postgresql://postgres: @localhost/tracker'
engine = create_engine(internal_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# create table mail_track with columns mail_id and time
metadata = MetaData()
mail_track = Table('mail_track', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('mail_id', String(250), nullable=False),
                   Column('time', DateTime, nullable=False)
                   )
metadata.create_all(engine)


class tracker(Resource):

    def get(self):
        return {'msg': 'Hello World'}

    def post(self):
        payload = request.get_json()
        mail_id = payload['mail_id']
        if TrackerTime().add_time_to_db(mail_id):
            return {'msg': 'recived mail_id: {}'.format(mail_id)}
        else:
            return {'msg': 'failed to add mail_id: {}'.format(mail_id)}


class TrackerTime:
    def add_time_to_db(self, mail_id):
        date_time = str(datetime.datetime.now())
        mail_track = MailTrack(mail_id=mail_id, time=date_time)
        session.add(mail_track)
        try:
            session.commit()
            return True
        except Exception as e:
            print(e)
            session.rollback()
            return False

    def get_mail_id_time(self, mail_id):
        mail_id_time = session.query(MailTrack.time).filter_by(mail_id=mail_id)\
            .order_by(MailTrack.time).limit(20).all()
        # [2023-04-27 10:29:42.483961, 2023-04-27 10:29:42.483961, 2023-04-27 10:29:42.483961]
        # calculate the time difference until the gap between two consicutive time is 2 seconds
        end_time = mail_id_time[-1].time
        print("end_time: ", end_time)
        # run reverse loop until the gap between two consicutive time is 2 seconds
        for i in range(len(mail_id_time)-1, 0, -1):
            time_diff = mail_id_time[i].time - mail_id_time[i-1].time
            if time_diff.seconds > 2:
                break
            start_time = mail_id_time[i-1].time
        total_time = end_time - start_time
        # convert total_time to seconds
        total_time = total_time.seconds
        return {'start_time': str(start_time), 'end_time': str(end_time), 'total_time': str(total_time) + ' seconds'}


class GetMailIdTime(Resource):
    def get(self):
        mail_id = request.args.get('mail_id')
        mail_id_time = TrackerTime().get_mail_id_time(mail_id)
        return {'mail_id': mail_id, 'time': mail_id_time}


api.add_resource(tracker, '/')
api.add_resource(GetMailIdTime, '/time')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
