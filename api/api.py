import argparse
import os
import traceback

import werkzeug
import yaml
from flask import Flask
from flask_restful import Api, Resource, reqparse
from yaml import Loader
from uuid import uuid4
import jinja2


SUBMISSIONS_DIRECTORY = 'submissions'
TESTS_DIRECTORY = 'tests'

submit_parser = reqparse.RequestParser()
submit_parser.add_argument('submission', type=werkzeug.datastructures.FileStorage,
                           location='files')

execute_parser = reqparse.RequestParser()
execute_parser.add_argument('type', type=str)
execute_parser.add_argument('task', type=str)
execute_parser.add_argument('submission_id', type=str)

loader = jinja2.FileSystemLoader(searchpath="./")
environment = jinja2.Environment(loader=loader)


def parse_output(output):
    output = output.split('\n')
    for i in range(len(output)):
        if '|' == output[i][0]:
            output = output[i:]
            break
    result = list(filter(lambda a: a != '' and a[0] != '|', output))
    only_yes_no = list(filter(lambda a: 'yes' in a or 'no' in a, result))
    return result, only_yes_no


def check_output(output, task, only_yes_no):
    result = []
    failed = False
    with open(os.path.join(TESTS_DIRECTORY, task, 'correct.yaml')) as f:
        correct = yaml.load(f, Loader=Loader)

    for elem in output:
        if 'exception' in elem:
            result.append(elem)
            failed = True

    if failed:
        return result
    idx = len(output) // len(only_yes_no)
    if len(correct) != len(only_yes_no):
        raise Exception('Bad test length')
    for i in range(0, len(output), idx):
        tmp_result = []
        errors = []
        for j in range(idx):
            if '=' in output[i + j]:
                prolog_parse = output[i + j].split(' = ')
                if str(correct[i // idx].get(prolog_parse[0])) == str(prolog_parse[1]):
                    tmp_result.append(True)
                else:
                    errors.append(str(correct[i // idx].get(prolog_parse[0])) + ' != ' + str(prolog_parse[1]))
                    tmp_result.append(False)
            else:
                if str(correct[i // idx].get('correct')) in str(output[i + j]):
                    tmp_result.append(True)
                else:
                    tmp_result.append(False)
                    errors.append('bad value: ' + output[i + j])
        new_val = all(map(lambda x: x is True, tmp_result))
        if new_val is False:
            new_val = errors
        result.append(new_val)
    return result


class Execute(Resource):
    def post(self):
        try:
            args = execute_parser.parse_args()
            if args.type is None:
                args.type = 'gprolog'
            if args.submission_id is None:
                return {'message': 'File of Prolog program is required', 'status': 400}, 400
            if args.submission_id + '.pl' not in os.listdir(SUBMISSIONS_DIRECTORY):
                return {'message': 'File of Prolog program not found', 'status': 404}, 404
            if args.task is None:
                return {'message': 'Task name is required', 'status': 400}, 400
            if args.type not in ['gprolog', 'ХЛП']:
                return {'message': 'Bad program type', 'status': 400}, 400
            template = environment.get_template('testing-system.j2')
            script = template.render(submission_file=SUBMISSIONS_DIRECTORY +'/' + args.submission_id + '.pl', test_file=TESTS_DIRECTORY + '/' + args.task + '/run.pl')
            stream = os.popen(script)
            output = stream.read()
            output, only_yes_no = parse_output(output)
            result = check_output(output, args.task, only_yes_no)
            return {'message': 'Successfully executed', 'result': result, 'status': 200}, 200
        except Exception as e:
            traceback.print_exc()
            return {'message': 'Server error: %s' % e, 'status': 500}, 500


class Submit(Resource):
    def post(self):
        try:
            args = submit_parser.parse_args()
            print(args)
            if args.submission is None:
                return {'message': 'File of Prolog program is required', 'status': 400}, 400

            submission_id = str(uuid4())
            args.submission.save(os.path.join(SUBMISSIONS_DIRECTORY, submission_id + '.pl'))
            return {'submission_id': submission_id, 'message': 'Successfully submitted', 'status': 200}, 200
        except Exception as e:
            traceback.print_exc()
            return {'message': 'Server error: %s' % e, 'status': 500}, 500


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="prolog-testing-system")
    parser.add_argument('--host',
                        metavar='<host_address>',
                        type=str,
                        default='127.0.0.1',
                        help='Server hostname')
    parser.add_argument('--port', '-p',
                        metavar='<port>',
                        default=3001,
                        type=int,
                        help='Server port')
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


if __name__ == '__main__':
    if not os.path.exists(SUBMISSIONS_DIRECTORY):
        os.makedirs(SUBMISSIONS_DIRECTORY)
    main()
