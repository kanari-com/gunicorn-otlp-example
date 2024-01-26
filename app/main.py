from flask import Flask, jsonify

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/items/<item_id>")
def items(item_id):
    return jsonify(item=item_id)