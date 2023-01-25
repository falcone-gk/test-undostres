# Test virtual UNDOSTRES

## Technologies
- Python version: 3.10.9
- request version: 2.28.2
- Test library: unittest

## Installing virtual environment

Create a **virtual environment** to install all packages required to run the tests:
```
python -m venv venv
```

If using **Windows** then open **PowerShell** and go to the project directory and run to activate virtual environment.
```
venv/Scripts/activate
```

If using **Linux** then you should run the next command:
```
source venv/bin/activate
```

Installing all required packages:
```
pip install -r requirements.txt
```

## Run all the test
To make tests to the API we are using unittest library. So, to run all the test we run this command:
```
python -m unittest
```
