# Wishapp

This project is used to demonstrate the use of FastAPI by building a simple REST API for a wish list application.
The project is divided into multiple steps. Each step can be accessed by checking out the respective branch.

## Installation
The project is built with python 3.12. We haven't tested it with the older version, but since it's just using the basic
features of FastAPI, it should work with older versions as well.
We recommend using poetry to manage the dependencies. However, we've also included a `requirements.txt` file for those 
who prefer using pip and virtual envs.

### Poetry
```shell
poetry install
```
### Pip
```shell
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Running the app
```shell
python -m app.server
```

## Steps
### Step 1: Basic FastAPI Application
```shell
git checkout origin/step-1
```
In the first step, we will create a simple FastAPI application with a basic project structure.

### Step 2: Wishapp APIs
```shell
git checkout origin/step-2
```

#### What is an API?
* A set of rules and protocols that allow different software systems to communicate with each other.
* APIs enable interaction between applications without needing direct human intervention.

#### What is a REST API?
* REST = Representational State Transfer
* Key Characteristics:
  * Stateless: Each request from a client to the server must contain all the information needed to process it.
  * Resource-Oriented: Focuses on resources, identified by URLs.
  * Standard HTTP Methods: CRUD operations mapped to HTTP verbs (GET, POST, PUT, DELETE).
  * Popularity: REST is widely used due to its simplicity and scalability.

#### Design considerations
* Direct vs Full Path Endpoints
* New endpoints vs Nested Endpoints
* Singular vs Plural Nouns
* Filtering, Sorting, and Pagination

### Step 3: User Authentication
```shell
git checkout origin/step-3
```
With this step we implement user authentication using JWT tokens.

In order to get the tokens we implement two endpoints:
* `/auth/token`: To get the token. This returns two tokens:
  * token: is a short-lived token the client needs to refresh regularly
  * refresh_token: is a long-lived token that can be used to get a new token
* `/auth/refresh`: To refresh the token via a `refresh_token`.

In addition, we are using a dependency in all existing endpoints to check if the user is authenticated.

### Step 4: DB Integration
```shell
git checkout origin/step-4
```
In this step we integrate the application with a database. We use SQLModel from the FastAPI authoutrs, which in its turn
is using SQLAlchemy as the ORM. For the demo we are using SQLite as the database. However, postgres or any other database 
can be used by changing the connection string in the `config.py` file and using corresponding primary key type in 
`models/base.py`.

In this step we've also introduced `/users` endpoint to add users. Every endpoint was updated to use the injected 
database session and the user resolved from the authentication header.

### Step 5: Services & Testing
```shell
git checkout origin/step-5
```

This step introduces `services` module to separate the business logic from the API endpoints. We also add integrations
tests for the `services/wishlist_service.py` and `routers/users.py` to test objects creation and retrieval from the 
test DB.

### Step 6: Python client generation
```shell
git checkout origin/step-6
```

In this step we generate a python client using openapi-generator-cli. The client is generated in the `clients/python` 
by calling `sh generate.sh python`.
Then we create a virtual environment and install the client using `sh init.sh` in the `clients/python` directory.
Finally, we test the client by running `python create_user.py` and `python get_wishlists.py` in the `clients/python` directory.