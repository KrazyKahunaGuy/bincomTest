cd
cd Documents/GitClones/bincomTest
source venv/bin/activate
export FLASK_APP=main:app
export FLASK_ENV=development

export DB_HOST=sql3.freemysqlhosting.net
export DB_USER=sql3491953
export DB_PASSWORD=rId1dFwymW
export DB_NAME=sql3491953
export DB_PORT=3306
gunicorn main:app --bind 0.0.0.0:5000