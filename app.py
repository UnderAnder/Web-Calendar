from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
import sys

app = Flask(__name__)
api = Api(app)


@api.resource('/event/today')
class TodayEvents(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


@api.resource('/event')
class PostEvent(Resource):
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

    def post(self):
        args = self.parser.parse_args()
        resp = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        return resp


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
