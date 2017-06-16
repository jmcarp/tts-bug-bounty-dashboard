#! /bin/bash

set -e

if [ "$1" == "--remigrate" ]; then
  rm dashboard/migrations/0001_initial.py
  python manage.py makemigrations
fi

rm -f db.sqlite3

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth.models import User

user = User.objects.create_user('root', 'root@gsa.gov', 'test123',
                                is_superuser=True, is_staff=True)
user.save()
EOF

echo 'Created superuser "root" w/ password "test123".'

python manage.py h1sync