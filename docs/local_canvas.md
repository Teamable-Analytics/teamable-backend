## Backend Development (with Local Canvas Instance)
> IMPORTANT: These instructions were taken from another project, so you won't be able to follow them exactly.

>  Local canvas installation is only required if you need the LTI login/launch process as a part of the development/testing. For example, you need to test whether a code should only work for certain user group(s)/course(s).

#### 1. Pre-requisite: Clone course-insights repo and create public.pem, private.pem, and public-jwk.json files for local course-insights application
1. Make sure you activate the Python virtual environment you created for this project.
1. Use the `/backend/generate_jwk/generate_jwk.py` script to create public.pem, private.pem, and public-jwk.json files.
    - 2.1. Go to `/course-insights/backend/generate_jwk` folder.
    - 2.2. Type `python generate_jwk.py`.
        - This will generate `private.pem`, `public.pem`, and `pubcli_jwk.json` files into the `conf/development` folder.

#### 2. How to launch the local instance of Canvas-lms
1. Clone the canvas-lms repo. `git clone https://github.com/instructure/canvas-lms.git`
1. Locate `config/security.yml` file. Update the value for `lti_iss` from `https://canvas.instructure.com` to `http://canvas.docker`.
1. Go to the repo directory. `cd canvas-lms`
1. Run the automated setup script. `./script/docker_dev_setup.sh`.
    - This process will ask you to create an admin user. Remember the credentials you provide.
1. When the setup is complete, start the app by typing `docker compose up -d`.
1. On the web browser, type `http://canvas.docker`. This will bring up the login page.
1. Use the admin credentials from step 4 to log in.

#### 3. How to create a new course on local Canvas LMS

1. Type `http://canvas.docker` on your browser.
1. Log in using the administrator credentials you created during the Canvas installation.
1. From the Canvas Dashboard page, click `Start a New Course`.
    - Enter course name and click `Create course`.

#### 4. How to add Course Insights to a Canvas course

1. On the main Canvas admin page.
    - 1.1. Click `Admin` on the left side menu.
    - 1.2. Select your admin account. ex) Test Account
    - 1.3. Click `developer key` on the left side menu.
1. Create a developer key for course-insights LTI key.
    - 2.1. Click `+ Developer Key`.
    - 2.2. Click `+ LTI Key`.
    - 2.3. On the Configure page, select `Paste JSON`.
    - 2.4. On the `LTI 1.3 Configuration`, copy and paste the JSON data from `/conf/development/canvas/developer_key.json`.
    - 2.5. Update `kid` and `n` value under `public_jwk` in the copy-and-pasted JSON data.
        - The values for `kid` and `n` can be found from `/conf/development/public_jwk.json`.
    - 2.6. Provide `Key Name`. ex) Course Insights LTI
    - 2.7. Click `Save` button.
1. Go to the new Canvas course page that you created.
1. Add course-insights to your course.
    4.1. Click `Settings` from the left-side menu.
    4.2. Click `Apps` -> `+App`.
    4.3. For configuration type, select `By Client ID`.
    4.4. For Client ID, provide the developer key ID that you created from step 9. It's the long integer value that appears in the Details column of the Developer Keys page.
    4.5. Click `Submit`.
1. Refresh the page and you will see the `course-insights` link on the left-side menu.
1. Click the `course-insights` link and it will start the LTI login and launch process, and bring up the course-insights application page.