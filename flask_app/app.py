from flask import Flask

from flask_app.blueprints.average_victims_bp import average_victims_bp
from flask_app.blueprints.most_active_groups_bp import active_groups_bp

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')

app.register_blueprint(average_victims_bp)
app.register_blueprint(active_groups_bp)

if __name__ == '__main__':
    app.run(debug=True)
