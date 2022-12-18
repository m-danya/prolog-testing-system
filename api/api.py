import argparse
import os

import werkzeug
import yaml
from flask import Flask
from flask_restful import Api, Resource, reqparse
from yaml import Loader
from uuid import uuid4
import jinja2

request_parser = reqparse.RequestParser()
request_parser.add_argument('type', type=str)
request_parser.add_argument('task', type=str)
request_parser.add_argument('file_id', type=str)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')

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
    with open(os.path.join('tests', task, 'correct.yaml')) as f:
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


class Submit(Resource):
    def post(self):
        try:
            args = request_parser.parse_args()
            if args.type is None:
                args.type = 'gprolog'
            if args.file_id is None:
                return {'message': 'File of Prolog program is required', 'status': 400}, 400
            if args.file_id + '.pl' not in os.listdir('files'):
                return {'message': 'File of Prolog program not found', 'status': 404}, 404
            if args.task is None:
                return {'message': 'Task name is required', 'status': 400}, 400
            if args.type not in ['gprolog', 'ХЛП']:
                return {'message': 'Bad program type', 'status': 400}, 400
            template = environment.get_template('testing-system.j2')
            script = template.render(file='files/' + args.file_id + '.pl', test='tests/' + args.task + '/run.pl')
            stream = os.popen(script)
            output = stream.read()
            output, only_yes_no = parse_output(output)
            result = check_output(output, args.task, only_yes_no)
            return {'message': 'Submit success', 'result': result, 'status': 200}, 200
        except Exception as e:
            return {'message': 'Server error: %s' % e, 'status': 500}, 500


class Upload(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            if args.file is None:
                return {'message': 'File of Prolog program is required', 'status': 400}, 400
            file_id = str(uuid4())
            args.file.save(os.path.join('files', file_id + '.pl'))
            return {'file_id': file_id, 'message': 'Upload success', 'status': 200}, 200
        except Exception as e:
            return {'message': 'Server error: %s' % e, 'status': 500}, 500


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="prolog-testing-system")
    parser.add_argument('--host',
                        metavar='<host_address>',
                        type=str,
                        default='127.0.0.1',
                        help='Host of server')
    parser.add_argument('--port', '-p',
                        metavar='<port>',
                        default=3001,
                        type=int,
                        help='Port of server')
    try:
        args, args_list = parser.parse_known_args(argv)
    except argparse.ArgumentError:
        raise Exception("Failed to parse arguments. Exiting.")
    return args.host, args.port


app = Flask(__name__)
api = Api()
api.add_resource(Submit, "/submit")
api.add_resource(Upload, "/upload")
api.init_app(app)


def main(argv=None):
    host, port = parse_args(argv)
    app.run(port=port, host=host, debug=True, use_reloader=False)


if __name__ == '__main__':
    if not os.path.exists('files'):
        os.makedirs('files')
    main()
