""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
import os
import sys
import traceback
import importlib
from inspect import getmembers, isfunction
from flask import Flask, Response, request, jsonify
from cortex import Message

app = Flask(__name__)


def invoke_fn(f):
    def invoke():
        try:
            req_msg = Message(request.json)
            result = f(req_msg)
            if isinstance(result, Message):
                return jsonify(result.to_params())
            return jsonify(Message({"payload": result}).to_params())
        except Exception as e:
            error = {"success": False, "error": str(e)}
            app.logger.error(str(e))
            traceback.print_exc()
            return jsonify(Message({"payload": error}).to_params())

    return invoke


@app.route("/health")
def health():
    return Response(response="OK!", status=200, mimetype="text/plain")


def assemble_server(routes):
    if not routes:
        raise ValueError("ROUTES must be passed")
        exit(-1)

    routes = [r.strip() for r in routes.split(",")]
    for route in routes:
        try:
            ep, m, f = route.split(":")
        except ValueError:
            raise ValueError("Invalid route specified: %s" % route)

        user_module = importlib.import_module(m)
        user_function = next(
            filter(
                lambda o: o[0] == f,
                [o for o in getmembers(user_module) if isfunction(o[1])],
            )
        )[1]

        print("Adding route: /%s using function %s:%s" % (ep, m, f))
        app.add_url_rule("/%s" % ep, ep, invoke_fn(user_function), methods=["POST"])

    app.run(host="0.0.0.0", port=5111, threaded=False)


if __name__ == '__main__':
    assemble_server(sys.argv[1])