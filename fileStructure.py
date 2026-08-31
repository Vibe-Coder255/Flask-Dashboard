from pathlib import Path

# Project scaffold without root metadata files (README.md, LICENSE, .gitignore)
project_structure = {
    "Flask-Dashboard": {
        "backend": {
            "files": [".env.example", "requirements.txt", "run.py"],
            "app": {
                "files": ["__init__.py", "config.py"],
                "api": {
                    "files": ["__init__.py", "auth.py", "users.py", "dashboard.py"]
                },
                "models": {
                    "files": ["__init__.py", "user.py", "metric.py"]
                },
                "services": {
                    "files": ["__init__.py", "analytics.py"]
                },
                "utils": {
                    "files": ["__init__.py", "auth_guard.py"]
                }
            },
            "tests": {
                "files": ["conftest.py", "test_auth.py", "test_dashboard.py"]
            }
        },
        "frontend": {
            "files": [".env.example", "package.json", "vite.config.js"],
            "public": {
                "files": ["favicon.ico"]
            },
            "src": {
                "files": ["App.jsx", "main.jsx"],
                "assets": {
                    "files": ["styles.css"]
                },
                "components": {
                    "files": ["Navbar.jsx", "Sidebar.jsx", "StatCard.jsx"]
                },
                "pages": {
                    "files": ["Dashboard.jsx", "Analytics.jsx", "Login.jsx"]
                },
                "services": {
                    "files": ["api.js"]
                }
            }
        }
    }
}

def create_scaffold(base_path: Path, node: dict):
    for key, val in node.items():
        if key == "files":
            for filename in val:
                file_path = base_path / filename
                if not file_path.exists():
                    file_path.touch()
                    print(f"[FILE] {file_path}")
        else:
            dir_path = base_path / key
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"[DIR]  {dir_path}")
            if isinstance(val, dict):
                create_scaffold(dir_path, val)

if __name__ == "__main__":
    current_directory = Path.cwd()

    # Detect if the script is already running inside the root 'Flask-Dashboard' folder
    if current_directory.name == "Flask-Dashboard":
        root_data = project_structure["Flask-Dashboard"]
        create_scaffold(current_directory, root_data)
    else:
        create_scaffold(current_directory, project_structure)

    print("\nFile tree created successfully.")