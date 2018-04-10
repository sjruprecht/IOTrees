# IOTrees

RPi3 setup guide in progress...


apt update
apt install -y libsm6 libfontconfig1 libxrender1 libxtst6
pip install imgaug keras opencv-python


Local Development Setup
-----------------------

### Repository

Clone this repository with:

    git clone https://github.com/sjruprecht/IOTrees.git


### Virtual Environment

#### Setting up

1. Install [pipenv](https://docs.pipenv.org/):

       sudo pip install pipenv

1. Inside the project directory, use `pipenv` with python 3.6 to create a virtual environment:

       cd IOTrees
       pipenv install --python $(which python3.6) --ignore-pipfile --dev

1. Activate the virtual environment:

       pipenv shell

1. Set up paths inside of the virtual environment:

       pipenv run pip install -e .

#### Usage

You can now either run a command in the virtual environment by prefixing it with `pipenv run`, or by activating a
shell inside of the virtual environment.

    # Run a command without having activated the shell
    pipenv run python foo

    # Or activate the shell first, then run a command
    pipenv shell
    python foo

There are two commands available in this repository. Example usages:

    # This detects EABs in the given image, saves debug images, and prints the number found
    detect --image examples/EAB-on-purple-trap.jpg --debug-images

    # This runs the above detection, and then sends that information to the given serial port
    eab_find --image examples/EAB-on-purple-trap.jpg --tty /dev/tty

If you get an error about command not found, make sure that you have the virtual environment activated
and that you've run `pipenv run pip install -e .`.
