# Flask-Dashboard
Static Dashboard Website using Flask framework

# File Structure
Flask-Dashboard/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory (create_app), extensions init
│   │   ├── config.py            # Development, Testing, Production configs
│   │   │
│   │   ├── api/                 # REST API blueprints/routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Login, Register, JWT handling
│   │   │   ├── users.py         # User management endpoints
│   │   │   └── dashboard.py     # Metrics, stats, chart data endpoints
│   │   │
│   │   ├── models/              # Database models (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── metric.py
│   │   │
│   │   ├── services/            # Business logic & data processing
│   │   │   ├── __init__.py
│   │   │   └── analytics.py
│   │   │
│   │   └── utils/               # Decorators, helpers, validators
│   │       ├── __init__.py
│   │       └── auth_guard.py
│   │
│   ├── tests/                   # Backend unit and integration tests
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_dashboard.py
│   │
│   ├── .env.example             # Backend environment variables template
│   ├── requirements.txt         # Flask, flask-cors, flask-jwt-extended, etc.
│   └── run.py                   # Entry point to run the backend server
│
├── frontend/                    # React / Vite / Plain SPA setup
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/              # Static images, icons, global styling
│   │   │   └── styles.css
│   │   ├── components/          # Reusable UI elements (Navbar, Sidebar, Cards)
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── StatCard.jsx
│   │   ├── pages/               # Full dashboard view pages
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Login.jsx
│   │   ├── services/            # Axios / Fetch client for backend API calls
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── .env.example             # Frontend env vars (e.g. VITE_API_BASE_URL)
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── LICENSE
└── README.md