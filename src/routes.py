import flask
from flask import Flask, request, abort, redirect, current_app, Blueprint
from werkzeug.exceptions import HTTPException
from datetime import datetime, timezone

from src.data import DataStore
from src.random_id import generate_url_id
from src.random_id import generate_auth_token
from src.validation import validate_request_body

from src.data import SqliteDataStore

routes = Blueprint('routes', __name__, static_folder='static', template_folder='templates') # https://stackoverflow.com/questions/66415003/how-to-import-routes-from-other-file-using-flask

@routes.route("/<urlId>", methods=["GET"])
def redirect(urlId: str):
    """Redirect to the full, target URL for the given `urlId`.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, a reponse with status code `301` and a
            `Location` header corresponding to the target URL. Otherwise, a
            response with status code `404` and a plain text error message.
    """
    validate_url_id_exists(urlId)
    validate_url_id_not_expired(urlId)

    redirect_url = get_data_store().get_direct_url(urlId)
    get_data_store().visit_url_id(urlId, request.remote_addr)
    return flask.redirect(redirect_url, code=301)


@routes.route("/<urlId>/stats", methods=["GET"])
def stats(urlId: str):
    """Return per-client stats about successful redirects for a given `urlId`.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, a reponse with status code `200` and a JSON
            object with numeric counts of successful redirects, per unique
            client IP address. Otherwise, a response with status code `403` or
            `404` and a plain text error message.
    """
    auth_token = request.headers.get('Authorization')
    validate_url_id_exists(urlId)
    validate_auth_token(urlId, auth_token)
    validate_url_id_not_expired(urlId)

    return get_data_store().visits_per_ip(urlId)

# TODO: Clarify requirement for whether the stats should be deleted for the url as well
@routes.route("/<urlId>", methods=["DELETE"])
def delete(urlId: str):
    """Delete an existing shortened URL.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, an empty reponse with status code `204`.
            Otherwise, a response with status code `403` or `404` and a plain
            text error message.
    """
    auth_token = request.headers.get('Authorization')
    validate_url_id_exists(urlId)
    validate_auth_token(urlId, auth_token)
    validate_url_id_not_expired(urlId)

    get_data_store().delete_url(urlId)
    return ('', 204)

@routes.route("/create", methods=["POST"])
def create():
    """Generate a new, unique shortened URL.

    Returns:
        flask.Response: On success, a reponse with status code `200` and a JSON
            object with valid `urlId`, `shortUrl`, and `authToken` values.
            Otherwise, a response with status code `400` and a plain text error
            message.
    """
    # TODO: Clarify requirement for how to validate user submitted ids
    data = request.get_json()

    is_valid, err_msg = validate_request_body(data)
    if not is_valid:
        abort(400, err_msg)

    if "id" in data:
        url_id = data["id"]
        if url_id_is_expired(url_id):
            get_data_store().delete_url_id(url_id)
        elif get_data_store().has_redirect(url_id):
            abort(400, f"URL with id {url_id} already exists")
    else:
        url_id = None
        while url_id is None or get_data_store().has_redirect(url_id):
            url_id = generate_url_id()

    url = data["url"]
    auth_token = generate_auth_token()

    get_data_store().create_url(url_id, url, auth_token)
    short_url = {}
    return {
        "shortUrl": f"{get_server_url()}/{url_id}",
        "urlId": url_id,
        "authToken": auth_token
    }

# TODO: Perform one query to DB for row data per request rather than multiple lookups
# TODO: Look up documentation for making this a decorator/filter
def validate_auth_token(url_id, auth_token):
    if not get_data_store().has_valid_auth_token(url_id, auth_token):
        abort(403, f"Auth token is not valid")

def validate_url_id_exists(url_id):
    if not get_data_store().has_redirect(url_id):
        abort(404, f"URL with id {url_id} does not exist")

def validate_url_id_not_expired(url_id):
    if url_id_is_expired(url_id):
        abort(410, f"URL with id {url_id} is expired. You may now reuse this url id.")

def url_id_is_expired(url_id):
    expire_time = get_data_store().get_expiration(url_id)
    if expire_time is None:
        return False

    expire_time_date = datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    
    return expire_time_date < datetime.now(timezone.utc)

def get_server_url():
    server_name = request.environ.get('SERVER_NAME', 'default_server_name')
    server_port = request.environ.get('SERVER_PORT', 'default_server_port')
    url = f"http://{server_name}:{server_port}"
    return url

# TODO: Find a better approach for creating a singleton
def get_data_store():
    if (SqliteDataStore.instance() is None):
        SqliteDataStore(testing=current_app.config['TESTING'])
    return SqliteDataStore.instance()
