
echo "BUILD START"
python 3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput --clear
echo "BUILD END"