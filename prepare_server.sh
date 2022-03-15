echo "Fetching changes..."
git fetch

echo "Updating changes..."
git rebase origin/dev

echo "Installing Requirements..."
pip install -r requirements/base.txt

echo "Migrating database..."
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic

sudo supervisorctl restart {{ program_name }}
echo "DONE"
