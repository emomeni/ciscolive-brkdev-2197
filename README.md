# Hands-free automation! 4 steps to build an event-driven automation workflow

Supplementary material for the Cisco Live EMEA 2024 session BRKDEV-2197.


## Before you start
The examples shown in the Cisco Live breakout are available for you in this repository. To get started, make sure you have following completed:

### Prepare your developer environment
- Install Python version 3
- Install Git
- Install a code editor, for example Visual Studio Code

Not sure how to do these? DevNet has great learning material to get you through these steps. You will need a free DevNet account to access the material, so register [here](https://developer.cisco.com/) if you haven't, and enjoy the learning labs to get your developer environment started:

* Windows: https://developer.cisco.com/learning/modules/dev-setup/dev-win/step/1
* Mac: https://developer.cisco.com/learning/modules/dev-setup/dev-mac/step/1
* Linux (CentOS): https://developer.cisco.com/learning/modules/dev-setup/dev-centos/step/1
* Linux (Ubuntu): https://developer.cisco.com/learning/modules/dev-setup/dev-ubuntu/step/1

### Clone the repository and install required libraries
When you have your developer environment up and running, make sure you install all libraries and modules required for your scripts. To keep your developer environment tidy, make sure to activate your virtual environment before installing the libraries.

Clone this repository to the environment in which your are working:
```bash
git clone https://github.com/cskoglun/BRKOPS-2103.git
```

Install the requirements to have all the necessary libraries for the code examples to work.

```bash
pip install -r requirements.txt 
```

### Set your environment variables

Use the `env.template` file to define your environment variables.

```bash
cp env.template env
```

```bash
source env
```

## Run the pyATS testcases

> **Note**! pyATS is not supported on Windows

To run the testcases separately:

```bash
python tests/ping_testcase.py
python tests/interface_testcase.py
```

To run the testcases in a small workflow:
```bash
python run_testcases.py
```

To run testcases and send a Webex message regarding the results:
```bash
python run_testcases_with_webex.py
```

## Authors & Maintainers
People responsible for the creation and maintenance of this project:
* Juulia Santala jusantal@cisco.com
* Palmer Sample psample@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).