from flask import Flask
from flask_app.blueprints import index_bp, victims_average_bp, active_groups_bp, unique_groups_bp, \
    corr_victims_for_events_bp

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')

app.register_blueprint(index_bp)
app.register_blueprint(victims_average_bp)
app.register_blueprint(active_groups_bp)
app.register_blueprint(unique_groups_bp)
app.register_blueprint(corr_victims_for_events_bp)

if __name__ == '__main__':
    app.run(debug=True)
