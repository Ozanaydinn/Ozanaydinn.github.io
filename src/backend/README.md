Set virtual env: 
$python3 -m venv venv 

    Then, if Linux:
    $source env/bin/activate 

    if Windows:
    $.\venv\Scripts\activate 

Set env variables for flask:
    if Linux:
    $export FLASK_APP=application
    $export FLASK_ENV=development

    if Windows:
    $set FLASK_APP=application
    $set FLASK_ENV=development

Before pushing:
$python -m pip freeze > requirements.txt  