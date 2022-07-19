# 篮球之境

## Installation

create & activate virtual env then install dependency:

with venv/virtualenv + pip:

```sh
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

python -m venv .env
source .env/bin/activate  # use `source .env\Scripts\activate` on Windows
pip install -r requirements.txt
```

generate fake data then run:

```sh
flask forge
flask run #

# Running on http://127.0.0.1:5000/
```

Test account:

* email: `admin@owen.com`
* password: `123456`

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
