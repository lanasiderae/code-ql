from flask import request
import os

@app.route("/danger")
def danger():
    user_input = request.args.get("value")
    eval(user_input)  # This should trigger semgrep rule: python.lang.security.eval-use.eval-use
    return "ok"
