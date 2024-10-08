# Teamable: Backend

## Getting started

### For local development

Prerequisites:

- Python 3.11
    - Use a virtual environment to run different versions of Python if you already have Python on your
      machine. [Here's an example doing so with virtualenv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
- `Note:` Docker is not needed for local development

Installation:

1. Clone this project.
   ```bash
    git clone git@github.com:Teamable-Analytics/teamable-backend.git
   ```
2. Install all dependencies.
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Create local environment file from sample.
   ```bash
   cp sample.env .env
   ```
4. Create and activate virtual environment.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
6. Apply database migrations.
   ```bash
   python manage.py migrate
   ```
8. Run the project from within the `src` directory with:
   ```bash
   python3 manage.py runserver
   ```

Project Setup (only needs to be run the first time the project is run):

1. Create a superuser in Django
   ```bash
   python3 manage.py createsuperuser
   ```
   Then follow the steps as prompted in the terminal.
2. Log in to [localhost:8000/admin](localhost:8000/admin) using your superuser credentials.
3. Create an `Organization` in the admin dashboard. Use the following details:
    - Name: _(anything you want)_
    - LMS Type: `Canvas`
    - LMS API URL: `https://canvas.ubc.ca` _(do not add a `/` as the end of this URL)_
4. Create a `Course` in the admin dashboard. Use the following details:
    - Name: _(anything you want)_
    - Organization: _(the organization from Step 3 above)_
    - LMS Access Token: _(leave blank)_
    - LMS Course ID: `31084`
    - LMS Opt-in Quiz ID: _(leave blank)_
    - Grade book Attribute: _(leave blank)_
5. Populate your course's LMS Access Token.
    - Follow [this guide](https://www.loom.com/share/d11258d2435942edb2c67e0eaeaad520).
    - Copy your LMS access token into the `Course` using the admin dashboard.
6. Create a normal instructor user.
    1. In the admin dashboard, create a `CourseMember` with the following details:
        - User: _(leave blank)_
        - Sections: _(leave untouched)_
        - Course: _(the course you created in Step 4 above)_
        - Role: `Instructor`
        - First name: _(leave blank)_
        - Last name: _(leave blank)_
        - LMS ID: _(leave blank)_
        - SIS User ID: _(leave blank)_
    2. Create a sign up token for this `CourseMember`.
       1. Go to [http://localhost:8000/admin/app/coursemember/](http://localhost:8000/admin/app/coursemember/)
       2. Select the checkbox for the `CourseMember` created in Step 6.i.
       3. In the "Action:" dropdown, select "Create JWT for..." and click "Go".
       4. You will see a page with raw JSON. It will have 1 key (likely `1`) and the value of that key will be a string. This string is the token.
    3. Follow the README in [Teamable Frontend](https://github.com/Teamable-Analytics/teamable-frontend) to attach login
        credentials to this CourseMember. The token from above is the "Instructor signup token" mentioned in that README.

### Useful commands

Format code using:
```bash
python3 -m black .
```

### Resources

- [Django Documentation](https://docs.djangoproject.com/en/5.0/)