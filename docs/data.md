# Data

## Export data from fly.io

    fly ssh console -C 'python /code/manage.py dumpdata --natural-foreign --exclude contenttypes --exclude auth --exclude sessions --exclude admin --exclude courses.accesscode --indent 2' > db.json

## Import fixture

    python manage.py loaddata db.json
