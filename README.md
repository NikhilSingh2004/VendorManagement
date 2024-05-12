# Vendor Management System (API)

Welcome to the Vendor Management System API! This API provides functionality for managing vendors, purchase orders, and performance records.

## Clone the project

To get started with the project, you can clone the repository to your local machine using the following command:

`git clone https://github.com/NikhilSingh2004/VendorManagement.git`

After cloning the repository, you can navigate to the project directory.

## Install Packages

After cloning the repository you will have to create an python environment to install the required the packages.

I would suggest you to create an environment using 'virtualenv', install virtualenv if not already

`pip install virtualenv`

Now create an virtual environment using the command:

`virtualenv <venv_name>`

After that run the following command:

`venv/scripts/activate`

Now if everything goes right then the <venv_name> given by you should appear in (<venv_name>) at the starting of the path.

Now Install the Packages after activating the virtual environment.

`pip install -r requirements.txt`

## API Documentation

The API documentation provides details about the endpoints, request and response formats, and authentication mechanisms. You can find the API documentation hosted on postman.

Here's how you can access the API documentation:

1. Start the server.
2. Open a web browser.
3. Navigate to `https://documenter.getpostman.com/view/34873005/2sA3JNaL31`

## Run Test Cases

The project includes unit tests to ensure the correctness of the implemented functionalities. To run the test cases, follow these steps:

1. Navigate to the project directory.
2. Activate your virtual environment (if you're using one).
3. Run the following command:

`python manage.py test`

This command will execute all the unit test cases and provide the test results.
