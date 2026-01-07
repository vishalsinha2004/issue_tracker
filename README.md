🐞 Issue Tracker API (Django REST Framework)

A production‑ready Issue Tracking Backend API built with Django REST Framework, supporting full CRUD operations, bulk actions, CSV import, reporting, filtering, pagination, and audit timelines.

This project was developed as part of a Python Developer technical assignment and follows REST best practices, clean architecture, and scalable design principles.

---

🚀 Features

✅ Core Features

* Create, read, update, and delete issues (CRUD)
* Optimistic concurrency control using versioning
* Assign issues to users
* Add comments to issues
* Manage labels (tags) on issues

✅ Advanced Features

* Bulk status update (transactional)
* CSV import for bulk issue creation
* Timeline / audit history for each issue (BONUS)
* Reports:

  * Top assignees by issue count
  * Average issue resolution time

✅ API Utilities

* Filtering (status, assignee, labels, date range)
* Search (title, description)
* Ordering (created date, resolved date, status)
* Pagination (page‑based)

---

🛠 Tech Stack

* Backend Framework: Django 5 + Django REST Framework
* Database: SQLite (can be swapped with PostgreSQL/MySQL)
* Filtering: django‑filter
* API Style: RESTful JSON APIs
* Tools: DRF Browsable API, Postman

---

📁 Project Structure


issue_tracker/
├── apps/
│   ├── issues/
│   │   ├── models.py        # Issue, Comment, Label, History models
│   │   ├── serializers.py   # DRF serializers (including CSV import)
│   │   ├── views.py         # ViewSets, actions, reports
│   │   ├── filters.py       # Issue filters
│   │   ├── pagination.py   # Custom pagination
│   │   └── urls.py          # Issue routes
│   └── users/               # User management
├── issue_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sample_data/
│   └── issues_sample.csv    # Sample CSV for import
└── manage.py


---

🔗 API Endpoints

🔹 Issues

GET    /api/issues/
POST   /api/issues/
GET    /api/issues/{id}/
PATCH  /api/issues/{id}/
DELETE /api/issues/{id}/

🔹 Comments

POST /api/issues/{id}/comments/

🔹 Labels


PUT /api/issues/{id}/labels/

🔹 Bulk Status Update

POST /api/issues/bulk_status/

🔹 CSV Import

POST /api/issues/import_csv/

🔹 Timeline (BONUS)


GET /api/issues/{id}/timeline/

🔹 Reports

GET /api/reports/top-assignees/
GET /api/reports/latency/


---

 📄 CSV Import Details

 Accepted CSV Format

title,description,status
Login bug,Login fails with correct credentials,open
UI alignment issue,Button overlaps text,in_progress


Import Response


{
  "total": 6,
  "created": 6,
  "failed": []
}


* CSV upload uses multipart/form‑data
* Each row is processed independently
* API returns a structured summary response

---

🔍 Filtering & Pagination Examples


GET /api/issues/?status=open
GET /api/issues/?search=login
GET /api/issues/?ordering=-created_at
GET /api/issues/?page=2


---

🧪 How to Run Locally

# Clone repository
git clone <repo-url>
cd issue_tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver


Open:

http://127.0.0.1:8000/api/issues/


---

 🧠 Design Highlights

* Uses DRF ViewSets & custom actions for clean routing
* Transaction‑safe bulk updates
* Serializer‑based validation
* Clear separation of concerns (filters, pagination, reports)
* REST‑compliant HTTP methods (GET, POST, PATCH, DELETE)

---

## 👨‍💻 Author

Vishal Sinha
Python / Django Backend Developer
LinkedIn: (https://www.linkedin.com/in/vishal-sinha2004/)

---

✅ Assignment Status

✔ All required features implemented
✔ Bonus features included
✔ Production‑ready code structure

---

> This project demonstrates real‑world backend development practices using Django REST Framework.
