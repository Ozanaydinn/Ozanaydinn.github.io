Set virtual env: 
$python3 -m venv env 

    Then, if Linux:
    $source env/bin/activate 

    if Windows:
    $cd env
    $.\Scripts\activate 

Set env variables for flask:
    if Linux:
    $export FLASK_APP=app
    $export FLASK_ENV=development

    if Windows:
    $set FLASK_APP=app
    $set FLASK_ENV=development

Before pushing:
$python -m pip freeze > requirements.txt  