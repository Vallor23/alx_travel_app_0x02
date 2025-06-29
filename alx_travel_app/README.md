# Travel Listings App

A Django app for managing travel listings, bookings, and reviews.

## Features

- Manage listings with details and availability  
- Book listings with date validation and cost calculation  
- Leave reviews with ratings and comments  

## Tech Stack

Python 3, Django, SQLite

## Setup

### Installation

1. **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd my-travel-app # or whatever your project directory is named
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt # You'll need to create this file
    ```

    *(You can generate `requirements.txt` by running: `pip freeze > requirements.txt` after installing all your project's dependencies like Django, djangorestframework, etc.)*

### Database Setup

1. **Apply database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Create a superuser (for Django Admin access):**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to set up a username, email, and password.

### Running the Application

1. **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

### Populating Sample Data

To quickly fill your database with sample listings for testing, use the custom management command:

```bash
python manage.py seed
