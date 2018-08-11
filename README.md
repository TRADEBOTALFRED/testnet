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
http://trolsoft.pythonanywhere.com/data/candles/?pair=ETHBTC&timeframe=60&from_date=2018-08-08&limit=10

http://localhost:8000/api/cron/
http://localhost:8000/data/candles/?pair=ETHBTC&from_date=2018-08-08&timeframe=5