# prolog-testing-system

**Work in progress.**

Run server:
```bash
sudo apt install gprolog python3-venv
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python api.py
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
        true,
        true,
        true,
        true
    ],
    "status": 200
}
```
