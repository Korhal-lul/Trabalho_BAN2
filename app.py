from flask import Flask

from controllers.cliente_controller import cliente_bp

app = Flask(__name__)

app.register_blueprint(cliente_bp)

@app.route("/")
def home():
    return """
    <h1>Sistema Transportadora</h1>
    """

if __name__ == "__main__":
    app.run(debug=True)