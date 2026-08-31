# 🔋 Battery Health Prediction System

This project is a **Machine Learning-powered web application** built using **Django** that predicts battery health based on input parameters.

---

## 🚀 Features

* Predict battery health using trained ML model
* Clean and responsive UI
* Django-based backend
* Real-time prediction

---

## 🛠️ Tech Stack

* Python
* Django
* Pandas, NumPy
* Scikit-learn
* HTML, CSS

---

## 📂 Project Structure

```
batterylife/
│
├── predictor/
│   ├── model.pkl
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── index.html
│
├── manage.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd batterylife
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run server

```
python manage.py runserver
```

### 5. Open in browser

```
http://127.0.0.1:8000/
```

---

## 📊 Model Information

The model was trained using battery dataset and exported as `model.pkl` using joblib.

---

## 📌 Notes

* Ensure feature inputs match training data
* Model file must be placed inside `predictor/`

---

## 👨‍💻 Author

Dinesh Reddy
