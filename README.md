# prolog-testing-system

**Work in progress.**

*Available [here](prolog-contest.ru).*

Easy installation with docker compose:
```bash
docker-compose up --build -d
```

Run the backend:
```bash
sudo apt install gprolog python3-venv
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python api.py
```

Run the frontend:
```bash
# 0. install nodejs (version >= 16)
# 1. run this:
cd react-frontend
npm install
npm start
```

## API description

Currently, the pipeline is like this:
1) Submitting the `.pl` file to the system
2) Executing this program on a set of tests

#### Submitting a program

`http://127.0.0.1:3001/submit` with form field `'submission'`

Response:
```json
{
    "submission_id": "90c5b537-43f4-47e2-a1da-638a457c2b7f",
    "message": "Successfully submitted",
    "status": 200
}
```

#### Executing a program on a set of tests

`POST http://127.0.0.1:3001/execute` with args
`{"type": "gprolog", "task": "task_2", "submission_id": 
"90c5b537-43f4-47e2-a1da-638a457c2b7f"}`

Response:

```json
{
    "message": "Successfully executed",
    "result": [
        {
            "test_number": 1,
            "result": "WA: output mismatch",
            "output_lines": [
                "Length = 1",
                "yes"
            ],
            "correct_lines": [
                "Length = 0",
                "yes"
            ]
        },
        {
            "test_number": 2,
            "result": "OK",
            "output_lines": [
                "Length = 3",
                "yes"
            ],
            "correct_lines": [
                "Length = 3",
                "yes"
            ]
        },
        {
            "test_number": 3,
            "result": "OK",
            "output_lines": [
                "Length = 2",
                "yes"
            ],
            "correct_lines": [
                "Length = 2",
                "yes"
            ]
        },
        {
            "test_number": 4,
            "result": "OK",
            "output_lines": [
                "Length = 4",
                "yes"
            ],
            "correct_lines": [
                "Length = 4",
                "yes"
            ]
        }
    ],
    "status": 200
}

```

## Development scripts

For now, one can use `api/submit_and_execute.sh` script to submit and execute
a solution like this:
```bash
./submit_and_execute.sh task_5_1 examples/task_5_1.pl
```

Also, `api/submit.sh` and `api/execute.sh` scripts are available: 

```bash
$ ./submit.sh path/to/my_program.pl
{
    "submission_id": "2d666df2-20b5-42da-9303-279481677f57",
    "message": "Successfully submitted",
    "status": 200
}
$ ./execute.sh task_1 2d666df2-20b5-42da-9303-279481677f57
{
    "message": "Successfully executed",
    "result": [
        {
            "test_number": 1,
            "result": "OK",
            "output_lines": [
                "yes"
            ],
            "correct_lines": [
                "yes"
            ]
        },
        {
            "test_number": 2,
            "result": "OK",
            "output_lines": [
                "no"
            ],
            "correct_lines": [
                "no"
            ]
        },
        {
            "test_number": 3,
            "result": "OK",
            "output_lines": [
                "yes"
            ],
            "correct_lines": [
                "yes"
            ]
        },
        {
            "test_number": 4,
            "result": "OK",
            "output_lines": [
                "yes"
            ],
            "correct_lines": [
                "yes"
            ]
        }
    ],
    "status": 200
}

```
