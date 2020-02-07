How to install Python Env:
* clone this repo
* install python 3.7 onto your computer, you can run python -v to verify the version you have

(these next step assume you are at the root level of the project)
* create a virtual environment for python using the following:
    * run the following command to install virtualenv `pip3 install virtualenv`
    * `mkdir venv`
    * `virtualenv venv -p python3.7`
    * `source venv/bin/activate`

* now install the requirements by typing `pip3 install -r requirements.txt`
* You will need to update some libraries manually
* navigate to
    * `venv/lib/python3.7/site-packages/flask_restplus/api.py`
    * `venv/lib/python3.7/site-packages/flask_restplus/model.py`
    * `venv/lib/python3.7/site-packages/flask_restplus/fields.py`
    and change `from werkzeug import cached_property` to `from werkzeug.utils import cached_property`
* you can now run the python webserver by typing `python3 backend/public/app.py`
