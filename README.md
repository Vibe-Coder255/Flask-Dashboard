Flask-Dashboard/
│
├── backend/
│   ├── database/                    # All DB connection & query engines
│   │   ├── __init__.py
│   │   ├── postgres.py              # PostgreSQL connection & table inspection
│   │   ├── mysql.py                 # MySQL connection & table inspection
│   │   └── mongodb.py               # MongoDB client & collection inspection
│   │
│   ├── security/                    # Connection validation & endpoint guards
│   │   ├── __init__.py
│   │   ├── validator.py             # Host/port checks, input sanitization, safe URI building
│   │   └── firewall.py              # Guard to restrict unsafe IPs/ports or read-only modes
│   │
│   ├── app.py                       # Main Flask server & API route endpoints
│   └── requirements.txt             # Minimal driver dependencies
│
├── frontend/                        # Front-end dashboard application
│   ├── public/
│   ├── src/
│   │   ├── components/              # Connection bar, tree viewer, data grid
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── LICENSE
└── README.md

