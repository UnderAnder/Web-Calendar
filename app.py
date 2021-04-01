import sys
from dataclasses import dataclass
from datetime import date

from flask import Flask
from flask import jsonify
from flask.json import JSONEncoder
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db?check_same_thread=False'
app.json_encoder = CustomJSONEncoder
api = Api(app)
db = SQLAlchemy(app)

@api.resource('/event/today')
class TodayEvents(Resource):
    def get(self):
        return jsonify(DBWorker.today_events())


@api.resource('/event')
class Events(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'date',
        type=inputs.date,
        help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
        required=True
    )
    parser.add_argument(
        'event',
        type=str,
        help='The event name is required!',
        required=True
    )

    def get(self):
        return jsonify(DBWorker.all_events())

    def post(self):
        args = self.parser.parse_args()
        event = args['event']
        date = args['date']
        DBWorker.add_event(event, date)
        resp = {
            "message": "The event has been added!",
            "event": event,
            "date": str(date.date())
        }
        return resp


@dataclass
class Events(db.Model):
    id: int
    event: str
    date: str

    __tablename__ = 'table_name'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)

db.create_all()
db.session.commit()

class DBWorker:
    @staticmethod
    def all_events():
        return Events.query.all()

    @staticmethod
    def today_events():
        return Events.query.filter(func.DATE(Events.date) == date.today()).all()

    @staticmethod
    def add_event(event, date):
        row = Events(event=event, date=date)
        db.session.add(row)
        db.session.commit()

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
