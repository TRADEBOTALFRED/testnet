# testnet
A test environment for analyzing the effectiveness of strategies


virtualenv --python=python3 myvenv
source myvenv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py loaddata service/fixtures/timeframes.yaml
python manage.py loaddata service/fixtures/markets.yaml
python manage.py loaddata service/fixtures/pairs.yaml


http://trolsoft.pythonanywhere.com/api/cron/