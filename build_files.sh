pip install -r requirements.txt

python3.12 manage.py makemigrations
python3.12 manage.py migrate 
python3.12 manage.py collectstatic