python3.9 -m ensurepip --upgrade --default-pip
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
