from flask import Flask, Blueprint, request, jsonify, abort, make_response, current_app as app

app = Flask(__name__)


@app.route("/")
def get_best_deal():
    request_url = request.args.get("request_url", None)

    if request_url is None:
        abort(make_response(jsonify(error="request url argument not given"), 400))

    return "<p>Hello, World!</p>"
