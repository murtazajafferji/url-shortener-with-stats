# Backend Code Challenge

## Problem

Implement a simple URL shortening web service (like [tinyurl](http://tinyurl.com/)) using the Python [Flask](http://flask.pocoo.org/docs) (or similar) web framework. This service will allow clients to create and delete unique identifiers for an arbitrary set of URLs and, provided a valid identifier, redirect a client to the target URL.

## Requirements (completed)

 1. Expose an endpoint to create a new shortened URL.
    * must optionally accept a user-provided ID for the shortened URL, otherwise generate one randomly
    * must not accept or generate a duplicate ID
    * must validate that IDs are non-empty and only contain alphanumeric characters
    * must include in the response a unique "authorization" token, which is different from the URL ID and may be used to delete or get additional stats about the shortened URL
    * must include in the response the shortened URL, constructed as follows: `http://{serverHostname}:{serverPort}/{urlId}`
 2. Expose an endpoint to delete an existing shortened URL.
    * must only allow deletion if the "authorization" token that was generated on creation is provided with the request
 3. Redirect valid, shortened URLs to the original full URL.
    * must keep track of successful redirects, per unique client IP address
 4. Expose an endpoint to retrieve stats about successful redirects for a shortened URL.
    * must only return stats if the "authorization" token that was generated on creation is provided with the request
    * must report counts of successful redirects per unique client IP address over the lifetime of the shortened URL

### Additional Requirements (completed)

 * Your code is expected to run on Python 3.7+.
 * You may use Flask as the web framework, but may use another web framework if you so choose.
 * You are free to use any third-party Python modules that are installable via `pip`. If you do, you must add the relevant dependencies to the `requirements.txt` file.
 * You may use the provided modules in the `db` package to intialize and interface with a SQLite database, but you may use another datastore (persistent or in-memory, relational or non-relational) of your choosing. In this case, you must *write code* to setup the database schema and *document* your database configuration or any additional setup that is required to run your application.

### Optional Requirements (completed)

 * Set a default expiration time when a shortened URL is created. After the time has expired, the shortened URL should fail to redirect, and the web service should not allow further operations on the expired URL ID, but should allow a new shortened URL to be created with that ID.
 * Prevent simple DoS or brute force attacks by restricting the number of requests a particular client can make to the service within a certain timeframe.

# Running
Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
```commandline
python -m venv url-shortener
```
Once you’ve created a virtual environment, you may activate it.

On Windows, run:
```commandline
url-shortener\Scripts\activate
```
On Unix or MacOS, run:
```commandline
source url-shortener/bin/activate
```
Run the following commands install Python modules and initialize the database
```commandline
pip install -r requirements.txt
python -m src.db.setup
```
Run the following command to start the Flask application
```commandline
python run.py
```

# Testing
The test suite can be run against a single Python version which requires pip install pytest and optionally pip install pytest-cov (these are included if you have installed dependencies from requirements.testing.txt)

To run the unit tests with a single Python version:
Run the following command to install the required packages
```commandline
py.test -v
```
to also run code coverage:
```commandline
py.test -v --cov-report xml --cov=reducepy
```
To run the unit tests against a set of Python versions:
```commandline
tox
```
On Windows, run:
```commandline
python -m pytest -v
```