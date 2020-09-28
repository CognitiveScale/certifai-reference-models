""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
import os
import sys
import traceback
import importlib
from inspect import getmembers, isfunction
from typing import NamedTuple, Dict, List

from flask import Flask, Response, request
from cortex import Message
import json
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


class EmptyResponse(NamedTuple):
    response: Dict = {"predictions": []}


class EmptyRequest(NamedTuple):
    request: Dict = {"payload": {"instances": []}}


def is_empty(a):
    if isinstance(a, List):
        return all(map(is_empty, a))
    return False


def _validate_message(msg):
    try:
        if msg.payload is None:
            return BadRequest(f'Missing `payload`. Expected format {json.dumps(EmptyRequest().request)}')
        elif not isinstance(msg.payload, Dict):
            return BadRequest(
                f'`payload` must be of type dict. Expected format {json.dumps(EmptyRequest().request)}')
        elif 'instances' not in msg.payload.keys():
            return BadRequest(f'Missing `instances`. Expected format {json.dumps(EmptyRequest().request)}')
        elif not isinstance(msg.payload.get('instances'), List):
            return BadRequest("`instances` must be of type List[Union[a, List a] ")
        elif is_empty(msg.payload.get('instances')):
            return EmptyResponse()
        else:
            return None
    except Exception as e:
        return BadRequest(str(e))


def invoke_fn(f):
    def invoke():
        try:
            req_msg = Message(request.json)
            er = _validate_message(req_msg)
            if isinstance(er, EmptyResponse):
                result = er.response
            elif er:
                error = {"success": False, "error": er.description}
                return Response(response=json.dumps(Message({"payload": error}).to_params()), status=er.code,
                                mimetype="application/json")
            else:
                result = f(req_msg)
            if isinstance(result, Message):
                return Response(response=json.dumps(result.to_params()), status=200, mimetype="application/json")
            return Response(response=json.dumps(Message({"payload": result}).to_params()), status=200,
                            mimetype="application/json")
        except Exception as e:
            error_code = e.code if hasattr(e, 'code') else 500
            description = e.description if hasattr(e, 'description') else str(e)
            error = {"success": False, "error": description}
            app.logger.error(str(e))
            traceback.print_exc()
            return Response(response=json.dumps(Message({"payload": error}).to_params()), status=error_code,
                            mimetype="application/json")

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
            m = 'certifaiReferenceModelServer.' + m
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
    return app


def get_routes():
    path = os.path.abspath(__file__)
    fp = os.path.join(os.path.dirname(path), '..', '.s2i/environment')
    with open(fp, 'r') as fn:
        routes = fn.read().replace("ROUTES=", '')
    return routes


routes = get_routes()
app = assemble_server(routes)


def start_flask_native(addr):
    global app
    host, port = addr.split(':')
    app.run(host=host, port=int(port), threaded=False)


if __name__ == '__main__':
    app = assemble_server(sys.argv[1])
