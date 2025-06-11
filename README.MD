# 0. Version
version = 0.1.0

# 1. SETUP
## 1.1. VENV
Creating virtual environment

    $ python3 -m venv .venv

activate virtual environment

    $ source .venv/bin/activate

Install dependencies:

    (.venv)$ pip install -r requirements.txt

installs FastAPI along with a set of recommended optional dependencies—such as uvicorn, httpx, and others—primarily for running and testing FastAPI applications.

    (.venv)$ pip install "fastapi[standard]"



## 1.2. espeak
ref to Note nr1.

install espeak

    $ sudo apt update
    $ sudo apt install espeak -y

## 1.3 TTS models
ref to Note nr2.
Notebook with scripts in the ./notebooks directory

    (.venv)$ python3 -m ipykernel install --user --name=myenv --display-name "Python (myenv)"
    (.venv)$ jupyter notebook

after running jupyter, change **kelner** to "Python (myenv)"
     
# 2. RUN
activate virtual environment

    $ source .venv/bin/activate

run server

    (.venv)$ fastapi dev app/main.py

# 3. NOTE

Note nr1: This application must be run on WSL (Windows Subsystem for Linux) or a native Linux environment. It relies on phonemizer, which in turn requires espeak to be natively installed. espeak does not work properly on Windows without a native Linux layer.

Note nr2: The contents of models, datasets, and vocoder are stored locally, in the ./models directory, to simplify the process of making them available to the application. Because of this, they must be downloaded manually first. Download scripts are provided as Jupyter notebooks in the ./notebooks directory