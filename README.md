# KUB QA

This repository contains tests for the KUB Education platform.

## Technologies
* Python 3.9

## 1. Overview

The tests cover the following API endpoints:
- **POST /admins** — Create a new admin.
- **GET /admins** — Retrieve a list of admins.
- **GET /admins/{id}** — Retrieve details of a specific admin by ID.
- **PUT /admins/{id}** — Update an admin's details.
- **DELETE /admins/{id}** — Delete an admin.
- **POST /admins/{id}/resend** — Resend the admin password (returns 200 on success or 503 if SMTP failure).

## 2. Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:KUB-Education/KUB-QA.git
   cd ./KUB-QA
   ```
   
2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 3.  Configuration
* BASE_URL:
The tests use the URL https://stage.superadmin.api.kub.education as specified in the OpenAPI spec.

* *Security Header:
The API requires the X-SUPER-ADMIN-KEY header for authentication. Update the headers() fixture in test_admin_api.py with your actual super admin key.

## 4. Running the Tests

**To run all tests, use:**
   ```bash
     pytest
   ```

**To run certain file, use:**
   ```bash
     pytest "path_to_file.py"
   ```

# Formating
- **Black**
  - **Command:** `tox -e black -- path/to/your/code`
  - **Description:** Black is an uncompromising Python code formatter that automatically reformats your code to follow consistent style guidelines (PEP 8).

- **Flake8**
  - **Command:** `tox -e flake8 -- path/to/your/code`
  - **Description:** Flake8 is a linting tool that checks your Python code for errors, stylistic issues, and enforces coding standards.

- **isort**
  - **Command:** `tox -e isort -- path/to/your/code`
  - **Description:** isort automatically sorts and organizes your import statements to maintain a consistent order and improve readability.
