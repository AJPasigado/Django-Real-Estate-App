echo "Fetching changes..."
git fetch

echo "Updating changes..."
git rebase upstream/dev

echo "Installing Requirements..."
pip install -r requirements/base.txt

echo "Migrating database..."
python manage.py migrate

echo "Running Server"
python manage.py runserver

echo "DONE"
