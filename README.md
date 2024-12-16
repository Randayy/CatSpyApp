# The Spy Cat Agency

This is a FastAPI project for The Spy Cat Agency.

## Project Description

The Spy Cat Agency is a management application designed to streamline the processes of assigning and managing spy cats, their missions, and targets. The system allows for the creation, update, and tracking of cats, missions, and targets while integrating third-party services to validate cat breeds.

## Getting Started

Follow these steps to get the application running locally.

### Prerequisites

Make sure you have the following installed on your system:
- Python 3.10 or higher
- PostgreSQL (or any SQL-compatible database)
- `pip` (Python package manager)
- [Postman](https://www.postman.com/) (optional, for testing endpoints)

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Randayy/CatSpyApp.git
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

Start the FastAPI server:
```sh
uvicorn app.main:app --reload
