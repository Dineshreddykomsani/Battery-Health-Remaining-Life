# Battery Health / Remaining Useful Life

A Django application that estimates a battery's remaining useful life (RUL) from eight operating measurements. It provides a responsive HTML/CSS interface and performs inference with the project's existing Decision Tree, Random Forest, and XGBoost regression artifacts.

## Important model note

This repository contains pre-trained model files in `predictor/`. The application does not retrain, replace, or modify them. The models expect these inputs, in this exact order:

1. `Cycle_Index`
2. `Discharge Time (s)`
3. `Decrement 3.6-3.4V (s)`
4. `Max. Voltage Dischar. (V)`
5. `Min. Voltage Charg. (V)`
6. `Time at 4.15V (s)`
7. `Time constant current (s)`
8. `Charging time (s)`

`scikit-learn==1.7.1` is pinned because that is the version recorded in the existing scikit-learn model artifacts.

## Local setup

Requires Python 3.11 (see `.python-version`).

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/. Before committing or deploying, run:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

## Configuration

| Variable | Local default | Hosted value |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | development-only fallback | a unique secret |
| `DJANGO_DEBUG` | `True` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | comma-separated allowed domains |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | empty | comma-separated `https://` origins when needed |

## Render deployment

The repository includes `render.yaml` and a `Procfile`. Create a Render Web Service from this repository; Render installs the pinned dependencies, runs `collectstatic`, generates `DJANGO_SECRET_KEY`, and launches Gunicorn. Add the final public hostname to `DJANGO_ALLOWED_HOSTS` if you use a custom domain, and set `DJANGO_CSRF_TRUSTED_ORIGINS` to that `https://` domain for form posts.

SQLite is retained because the application has no persisted prediction data. Render's filesystem is ephemeral, so use a managed PostgreSQL database only if persistent Django data is added later.
