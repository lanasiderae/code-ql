import os
import flask
import hashlib
import requests
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
engine = SQLAlchemy()

@app.route("/insert/person")
def insert_person():
    name = flask.request.args.get("name")
    lastname = "you don't get to pick >:)"

    # String concatenation using + operator
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('" + name + "')")

    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (firstname, lastname) VALUES ('" + name + "','" + lastname + "')")

    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('" + lastname +"')")

    # Format strings with %
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (name))

    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (flask.request.args.get("name")))

    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (lastname))

    # Format strings with .format
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('{}')".format(name))

    # Format strings  using fstrings
    # ruleid: tainted-sql-string
    engine.execute(f"SELECT FROM person WHERE name='{name}'")

    # Query without concatenation
    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('Frodon Sacquet')")

    # Query using prepared statement with named parameters
    # ok: tainted-sql-string
    stmt = text("INSERT INTO table (name) VALUES(:name)")
    engine.execute(stmt, name=name)

    # SQL Composition and prepared statement
    # ok: tainted-sql-string
    query = select(literal_column("users.fullname", String) + ', ' + literal_column("addresses.email_address").label("title")).where(and_(literal_column("users.id") == literal_column("addresses.user_id"), text("users.name BETWEEN 'm' AND 'z'"), text("(addresses.email_address LIKE :x OR addresses.email_address LIKE :y)"))).select_from(table('users')).select_from(table('addresses'))
    engine.execute(query, {"x":"%@aol.com", "y":name}).fetchall()

@app.route("/insert/person/path")
def insert_person(path):
    name = path
    lastname = "you don't get to pick >:)"

    # String concatenation using + operator
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('" + name + "')")

    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (firstname, lastname) VALUES ('" + name + "','" + lastname + "')")

    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('" + lastname +"')")

    # Format strings with %
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (name))

    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (flask.request.args.get("name")))

    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('%s')" % (lastname))

    # Format strings with .format
    # ruleid: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('{}')".format(name))

    # Format strings  using fstrings
    # ruleid: tainted-sql-string
    engine.execute(f"SELECT FROM person WHERE name='{name}'")

    # Query without concatenation
    # ok: tainted-sql-string
    engine.execute("INSERT INTO person (name) VALUES ('Frodon Sacquet')")

    # Query using prepared statement with named parameters
    # ok: tainted-sql-string
    stmt = text("INSERT INTO table (name) VALUES(:name)")
    connection.execute(stmt, name=name)

    # SQL Composition and prepared statement
    # ok: tainted-sql-string
    query = select(literal_column("users.fullname", String) + ', ' + literal_column("addresses.email_address").label("title")).where(and_(literal_column("users.id") == literal_column("addresses.user_id"), text("users.name BETWEEN 'm' AND 'z'"), text("(addresses.email_address LIKE :x OR addresses.email_address LIKE :y)"))).select_from(table('users')).select_from(table('addresses'))
    engine.execute(query, {"x":"%@aol.com", "y":name}).fetchall()
# semgrep_tests/test_format_in_deferred_gettext.py
from pycroft.helpers.i18n import deferred_gettext
# FAIL
msg = deferred_gettext("Hello, {}.{}!").format("user", "domain")
# PASS
msg_ok = deferred_gettext("Hello, {}.{}!").format("user", "domain").to_json()

# semgrep_tests/test_format_in_gettext.py
from pycroft.helpers.i18n import gettext
# FAIL
msg = gettext("Hi {}!").format("world")
# PASS
msg_ok = gettext("Hi {}!").format("world")

# semgrep_tests/test_log_event_with_format.py
# FAIL
log_warn_event("Alert: {} exceeded".format("limit"))
# PASS
log_warn_event(deferred_gettext("Alert: {} exceeded").format("limit").to_json())

# semgrep_tests/test_use_format_instead_of_strftime.py
from datetime import datetime
now = datetime.now()
# FAIL
bad = now.strftime("%Y-%m-%d")
# PASS
good = f"{now:%Y-%m-%d}"

# semgrep_tests/test_do_not_call_get_with_keywords.py
import pycroft.model
# FAIL
u = pycroft.model.User.get(id=123)
# PASS
u = pycroft.model.User.get(123)

# semgrep_tests/test_secure_name_for_password_fields.py
from wtforms import PasswordField
# FAIL
class Login:
    mypass = PasswordField("Password")
# PASS
class LoginFixed:
    secret_mypass = PasswordField("Password")

# semgrep_tests/alembic/versions/test_dont_use_datetimetz.py
from pycroft.model.types import DateTimeTz
# FAIL
x = DateTimeTz()
# PASS
import sqlalchemy as sa
y = sa.types.DateTime(timezone=True)

# semgrep_tests/alembic/versions/test_dont_use_models.py
# FAIL
import pycroft.model
# PASS
import sqlalchemy as sa

# semgrep_tests/pycroft/helpers/test_dont_use_models_in_helpers.py
# FAIL
from pycroft.model import User
# PASS
from sqlalchemy import Column

# semgrep_tests/tests/test_dont_commit_session.py
# FAIL
session.commit()
# PASS
session.flush()

# semgrep_tests/pycroft/model/test_prefer_back_populates.py
# FAIL
relationship("Group", backref=sqlalchemy.orm.backref("users"))
# PASS
relationship("Group", back_populates="users")

# semgrep_tests/web/test_pydantic_optional.py
from pydantic import BaseModel
# FAIL
class Example(BaseModel):
    email: str | None
# PASS
class ExampleFixed(BaseModel):
    email: str | None = None

# semgrep_tests/web/test_commit_in_context.py
# FAIL
with session.begin_nested():
    session.commit()
# PASS
with session.begin_nested():
    session.flush()

# semgrep_tests/web/test_flask_endpoint_typing.py
@app.route("/ping")
def ping():
    return "pong"  # FAIL

@app.route("/pong")
def pong() -> ResponseReturnValue:
    return "pong"  # PASS

# semgrep_tests/pycroft/templates/mail/test_no_plain_a_tags.html
<!-- FAIL -->
<a href="https://example.com">Visit</a>
<!-- PASS -->
{{ link.render_link("Visit", "https://example.com") }}
