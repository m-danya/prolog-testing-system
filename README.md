# prolog-testing-system

Work in progress.

Run server:
```python
sudo apt install gprolog
python3 ./api/api.py
```
For upload file:
```http://127.0.0.1:3001/upload with form field 'file'```

Returning:
```json
{
    "file_id": "90c5b537-43f4-47e2-a1da-638a457c2b7f",
    "message": "Upload success",
    "status": 200
}
```
For execution:
```POST http://127.0.0.1:3001/submit with args {"type": "gprolog", "task": "task_2", "file_id": "90c5b537-43f4-47e2-a1da-638a457c2b7f"}```

Returning:
```json
{
    "message": "Submit success",
    "result": [
        true,
        true,
        true,
        true
    ],
    "status": 200
}
```
