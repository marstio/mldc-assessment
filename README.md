# Task Manager CLI

A Python command-line application for managing daily tasks. I built this for the Media Meter / SevenGen technical assessment to demonstrate OOP principles, raw SQL interaction, and basic data analytics.

## Prerequisites

Before running the app, make sure you have:

- **Python 3.x** installed.
- **MySQL Server** running (I used MySQL Workbench for setup).

## Setup Instructions

### 1. Clone or Download

Download this repository and open the folder in your terminal.

### 2. Set up the Virtual Environment

It's best to run this in an isolated environment so dependencies don't clash.

```bash
# Create the environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3\. Install Dependencies

I included a `requirements.txt` file with all the necessary libraries (mysql-connector, python-dotenv, etc.).

```bash
pip install -r requirements.txt
```

### 4\. Database Configuration

1.  **Create the Database:**

    - Open **MySQL Workbench**.
    - Open the file `setup_database.sql` from this folder.
    - Run the script (Lightning Bolt icon) to create the `task_manager_db` database and the `tasks` table.

2.  **Connect the App:**

    - Create a new file in this folder named `.env`.
    - Add your MySQL credentials inside it (no quotes needed):

    ```ini
      DB_HOST=127.0.0.1
      DB_USER=root
      DB_PASSWORD=your_actual_password
      DB_NAME=task_manager_db
    ```

## How to Run

Once the database is ready and requirements are installed, just run:

```bash
python main.py
```

## Features

- **CRUD Operations:** Add, List, Update, and Delete tasks.
- **Filtering:** Easily filter tasks by Pending, In Progress, or Completed status.
- **Analytics Dashboard:** Visual bar charts showing priority breakdown and completion rates.
- **Background Backup:** A background thread simulates auto-backups every 5 minutes (multithreading requirement).
- **Input Validation:** Prevents scheduling tasks in the past and handles invalid date formats.
