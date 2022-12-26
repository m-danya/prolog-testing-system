import argparse
import os
import traceback

import werkzeug
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse
from uuid import uuid4
import jinja2

from translator import translate
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

tasks_info_parser = reqparse.RequestParser()

loader = jinja2.FileSystemLoader(searchpath="./")
environment = jinja2.Environment(loader=loader)


class Execute(Resource):
    @cross_origin()
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
            if args.type not in ["gprolog", "HLP"]:
                return {
                    "message": f"Argument type={args.type} is not valid",
                    "status": 400,
                }, 400
            cmd_template = environment.get_template("test_prolog_program.j2")

            translate(args.submission_id, args.type)
            execution_result = execute_on_tests(
                args.submission_id, args.task, cmd_template
            )

            os.remove(SUBMISSIONS_DIRECTORY / (args.submission_id + ".pl"))
            return {
                "message": "Successfully executed",
                "result": execution_result,
                "status": 200,
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {"message": "Server error: %s" % e, "status": 500}, 500


class Submit(Resource):
    @cross_origin()
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


class TasksInfo(Resource):
    @cross_origin()
    def get(self):
        try:
            args = tasks_info_parser.parse_args()
            task_names = []
            task_descriptions = []
            # the tasks list is sorted by their names
            for task_dir in sorted(TESTS_DIRECTORY.glob("*")):
                task_names.append(task_dir.name)
                description_file = task_dir / "description.md"
                if description_file.exists():
                    with open(description_file) as f:
                        task_descriptions.append(f.read())
                else:
                    task_descriptions.append(
                        f"## {task_dir.name}\n\nNo description provided"
                    )
            return {
                "task_names": task_names,
                "task_descriptions": task_descriptions,
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
api.add_resource(TasksInfo, "/tasks_info")
api.init_app(app)
cors = CORS(app)


def main(argv=None):
    host, port = parse_args(argv)
    app.run(port=port, host=host, debug=True, use_reloader=False)


if __name__ == "__main__":
    SUBMISSIONS_DIRECTORY.mkdir(exist_ok=True, parents=True)
    main()
