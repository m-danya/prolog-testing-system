import argparse
import traceback

import werkzeug
from flask import Flask
from flask_restful import Api, Resource, reqparse
from uuid import uuid4
import jinja2

from prolog_parsing import execute_on_tests
from settings import *


submit_parser = reqparse.RequestParser()
submit_parser.add_argument(
    "submission", type=werkzeug.datastructures.FileStorage, location="files"
)

execute_parser = reqparse.RequestParser()
execute_parser.add_argument("type", type=str)
execute_parser.add_argument("task", type=str)
execute_parser.add_argument("submission_id", type=str)

loader = jinja2.FileSystemLoader(searchpath="./")
environment = jinja2.Environment(loader=loader)


class Execute(Resource):
    def post(self):
        try:
            args = execute_parser.parse_args()
            if args.type is None:
                args.type = "gprolog"
            if args.submission_id is None:
                return {
                    "message": "You need to specify submission_id.",
                    "status": 400,
                }, 400
            if (
                SUBMISSIONS_DIRECTORY / (args.submission_id + ".pl")
                not in SUBMISSIONS_DIRECTORY.iterdir()
            ):
                return {
                    "message": f"Submission with id {args.submission_id} was not found.",
                    "status": 404,
                }, 404
            if args.task is None:
                return {"message": "You need to specify task", "status": 400}, 400
            if args.type not in ["gprolog", "ХЛП"]:
                return {
                    "message": f"Argument type={args.type} is not valid",
                    "status": 400,
                }, 400
            cmd_template = environment.get_template("test_prolog_program.j2")

            execution_result = execute_on_tests(
                args.submission_id, args.task, cmd_template
            )

            return {
                "message": "Successfully executed",
                "result": execution_result,
                "status": 200,
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {"message": "Server error: %s" % e, "status": 500}, 500


class Submit(Resource):
    def post(self):
        try:
            args = submit_parser.parse_args()
            if args.submission is None:
                return {
                    "message": "File of Prolog program is required",
                    "status": 400,
                }, 400

            submission_id = str(uuid4())
            args.submission.save(SUBMISSIONS_DIRECTORY / (submission_id + ".pl"))
            return {
                "submission_id": submission_id,
                "message": "Successfully submitted",
                "status": 200,
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {"message": "Server error: %s" % e, "status": 500}, 500


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="prolog-testing-system")
    parser.add_argument(
        "--host",
        metavar="<host_address>",
        type=str,
        default="127.0.0.1",
        help="Server hostname",
    )
    parser.add_argument(
        "--port", "-p", metavar="<port>", default=3001, type=int, help="Server port"
    )
    try:
        args, args_list = parser.parse_known_args(argv)
    except argparse.ArgumentError:
        raise Exception("Failed to parse arguments. Exiting.")
    return args.host, args.port


app = Flask(__name__)
api = Api()
api.add_resource(Submit, "/submit")
api.add_resource(Execute, "/execute")
api.init_app(app)


def main(argv=None):
    host, port = parse_args(argv)
    app.run(port=port, host=host, debug=True, use_reloader=False)


if __name__ == "__main__":
    SUBMISSIONS_DIRECTORY.mkdir(exist_ok=True, parents=True)
    main()
