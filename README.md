# prolog-testing-system

## Тестирующая система для программ на Prolog и ХЛП

Система доступна по адресу ➡️ [https://prolog-contest.ru](https://prolog-contest.ru) ⬅️

**Как пользоваться**: выбрать задачу, написать код в окошке справа, выбрать язык (Prolog / ХЛП), отправить задачу на проверку, получить вердикт тестирующей системы с подробным выводом на всех тестах.

Тестирующая система предназначена для самоподготовки студентов 3 потока 4 курса ВМК МГУ к экзамену по курсу "[Математическая логика и логическое программирование](https://mk.cs.msu.ru/index.php/%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BB%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0_%D0%B8_%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_(3-%D0%B9_%D0%BF%D0%BE%D1%82%D0%BE%D0%BA))".
Поскольку в курсе присутствует логическое программирование и существуют интерпретаторы языка Prolog, возникла идея создания
системы автоматизированной проверки программ студентов на задачах из семинаров для полноценной поддержки "программистской"
части курса. Для этого была проделана следующая работа:

1. Исследованы особенности работы интерпретатора `gprolog` языка Prolog

Здесь требовалось требовалось осуществить вывод всех решений для запроса-теста (тестирующего предикат пользователя) с учётом произвольности количества
переменных в запросе. Проблема была в том, что интерпретаторы Пролога выводят решения по одному, предлагая нажать ';'
для вычисления и вывода очередного решения. Для решения этой проблемы был использован предикат `setof(+Template, +Goal, -Set)`,
причём в качестве аргумента `Template` подаются все используемые в запросе переменные (их пришлось парсить из текста теста
в `variables_list`, см. ниже). Результат ожидается в переменной `Result`.

```bash
cat {{ test_file }} | sed --expression='s/^\(.*\)\.$/setof\({{ variables_list }},\1, Result\)\./g'
```

Таким образом, запрос `descendant(X, dima).` превращается в `setof({{ variables_list }},descendant(X, dima), Result).` = 
`setof([X],descendant(X, dima), Result).`,
и ожидаемый ответ на такой запрос может быть таким:
```
Result = [[kolya],[max],[nastya],[sasha],[vasya],[vlad]]
yes
```

Также в некоторых заданиях предлагается реализовать предикаты, опираясь на то, что некоторые предикаты уже
реализованы (`father` и много других из 5.1, `not` из задач 7 семинара). Эти предикаты были реализованы в отдельном
файле, общем для набора тестов: `shared_consult_data.pl`.

2. Реализована серверная часть на Python с использованием фреймворка Flask. 
   
Поскольку интерепретатор есть для языка Prolog, а в курсе изучаются программы на ХЛП (синтаксически схожем языке),
для удобства пользователей  был реализован транслятор с ХЛП на Prolog. Для этого потребовалось рассмотреть все различия 
используемых в курсе подмножеств этих языков, в том числе повозиться с обработкой списков.

Бэкенд устойчив к различному роду ошибок, сообщает о проблемах в ответе на запрос, если что-то идёт не так. API
спроектирован с заделом на возможное дальнейшее развитие. Код пару раз подвергался рефакторингу.

3. Реализована клиентская часть в виде React JS приложения. Интерфейс достаточно адаптивен и функционален. Условия задач
рендерятся из markdown-а, результаты тестирования представлены в наглядном виде, есть возможность загрузки решения из файла.

5. Было подготовлено markdown-описание, **работающее решение и тесты для многих задач с семинаров курса**. [Источник задач](https://mk.cs.msu.ru/images/5/51/MatLog_tasks.pdf).

6. Для удобства пользователей система была развёрнута в виде сайта: [https://prolog-contest.ru](https://prolog-contest.ru).

Предварительно backend и frontend части проекта были Docker-изованы для возможности лёгкого запуска на любом компьютере. (см. Delevopment notes)


### Содействие развитию проекта (contributing)

Мы надеемся, что система будет полезна для подготовки к экзамену и приветствуем любой вклад в развитие проекта.
Этот вклад может состоять в добавлении новых задач в систему, например из [расширенного сборника задач от авторов курса](https://mk.cs.msu.ru/images/8/8e/MatLog_exer.pdf). Для этого нужно сделать fork репозитория, добавить папку для каждой задачи в `api/tests` (+ решение
в папку `api/examples`) аналогично тому, как это сделано сейчас, и сделать pull request.

Если что-то непонятно, [пишите](https://t.me/m_danya_jpg).

## Development notes (ENG)

### Runing a setup with Docker (recommended)
Run frontend+backend with a single command:
```bash
docker-compose up --build -d
```
Then open `localhost:3000` in your browser.

P.S. To make things happen, one should remove `--certfile=server.crt
--keyfile=server.key` from the `api/Dockerfile` and create a
file `react-frontend/.env` with a following content:
```
REACT_APP_BACKEND_URL='http://127.0.0.1:3001'
```


### Running a setup without Docker

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
REACT_APP_BACKEND_URL=https://localhost:3001 npm start
```

### API description

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
            ],
            "test_text": "...",
            "test_consult_text": "..."
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
            ],
            "test_text": "...",
            "test_consult_text": "..."
        },
        {
            "test_number": 3,
            "result": "TL",
            "output_lines": [],
            "correct_lines": [
                "Length = 2",
                "yes"
            ],
            "test_text": "...",
            "test_consult_text": "..."
        },
        {
            "test_number": 4,
            "result": "RE",
            "output_lines": [
                "exception: Fatal Error: local stack overflow (size: 16384 Kb, reached: 16383 Kb, environment variable used: LOCALSZ)"
            ],
            "correct_lines": [
                "Length = 4",
                "yes"
            ],
            "test_text": "...",
            "test_consult_text": "..."
        }
    ],
    "status": 200
}

```

### Submitting and executing programs without a frontend

One can use `api/submit_and_execute.sh` script to submit and execute
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
        ......
    ],
    "status": 200
}

```
