# Lunch Service


## Steps to Run the Project

1. **Clone the Project from GitHub**
   - Create any folder.
   - Navigate to it and run:
     ```bash
     git clone https://github.com/denyshub/TestTask.git
     ```

2. **Set Up the Virtual Environment and Install Dependencies**
   - Navigate to the project folder:
     ```bash
     cd TestTaskInforce
     ```
   - Create and activate a virtual environment:
     ```bash
     python -m venv djvenv
     source venv/bin/activate  # For Windows: djvenv\Scripts\activate
     ```
   - Install the required dependencies:
     ```bash
     pip install -r lunch_service/requirements.txt
     ```

3. **Apply Migrations and Start the Server**
   - Navigate to the root directory of your Django project:
     ```bash
     cd lunch_service
     ```
   - Apply migrations to set up the database:
     ```bash
     python manage.py migrate
     ```
   - Start the server:
     ```bash
     python manage.py runserver
     ```

4. **Open the Browser**
   - Go to: [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)