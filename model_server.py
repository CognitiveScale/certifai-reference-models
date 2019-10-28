import json
import config as cfg
from predict import predict
from example_utils import set_root
from flask import Flask, request, Response

# supress sklearn warnings
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

HOST = cfg.server['host']
PORT = cfg.server['port']
JSON_MIME = 'application/json'
ALLOWED_EXTENSIONS = set(['pkl'])
app = Flask(__name__)
set_root(cfg.server['EXAMPLES_FOLDER'])


@app.route('/<model_name>/predict', methods=['POST'])
def predict_endpoint(model_name):
    try:
        req = json.loads(request.data)
        instances = req.get('payload', {}).get('instances', [])
        results = predict(model_name, instances)
        json_resp = json.dumps({'payload': results})

        return Response(status=200,
                        response=json_resp,
                        mimetype=JSON_MIME)

    except Exception as e:
        app.logger.error("Caught exception while processing request.", exc_info=True)
        return Response(status=500,
                        response=json.dumps(
                            {'payload': {'error': str(e)}}),
                        mimetype=JSON_MIME)


if __name__ == '__main__':
    set_root(cfg.server['EXAMPLES_FOLDER'])
    app.run(host=HOST, port=PORT, threaded=False)
