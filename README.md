### Clone the repository
```bash
  git clone https://github.com/wiut00012803/migration_service.git
  cd migration_service
```
### Create & activate a virtual environment
```bash
  python -m venv .venv
  source .venv/bin/activate
```
### Install dependencies
```bash
  pip install -r requirements.txt
```
### Apply migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser 
  bash python manage.py runserver 0.0.0.0:8000
```
  The API will be available at `http://localhost:8000/api/`.