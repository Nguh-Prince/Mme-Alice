# Prerequisites
- Python 3.8+
- virtualenv python package

# Installation
- Create a new directory to store the project: **mkdir project-dir**
  - Change into the directory: **cd project-dir**
- Create a virtual environment: **virtualenv environment**
  - Activate the environment:
    - Windows: **environment\Scripts\activate**
    - Linux / Mac: **source environment/bin/activate**
  **NB: This step can be skipped if you'd prefer to directly install the necessary packages in your computer, although this is not best practice** 
- Clone or download the repository: **git clone git@github.com:Nguh-Prince/Mme-Alice.git**
  - If you downloaded the repository, please copy the downloaded folder into the project-dir folder
- Cd into the cloned directory: cd Mme-Alice
- Make sure your virtual environment is activated and run: **pip install -r requirements.txt**
  - If you did not create a virtual environment, you can still just run the command to install the necessary packages directly into your computer
- Run the server: **python manage.py runserver**
  - You can also specify the port number to run the server over, using the following syntax: **python manage.py runserver 0.0.0.0:799**
- Open the link to ther server on your local browser and you should be all set