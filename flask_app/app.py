from flask import Flask
from flask_app.blueprints.victims_average_bp import victims_average_bp
from flask_app.blueprints.index_bp import index_bp
from flask_app.blueprints.most_active_groups_bp import active_groups_bp
from flask_app.blueprints.unique_groups_bp import unique_groups_bp
from flask_app.blueprints.correlation_victims_for_events_bp import corr_victims_for_events_bp

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')

app.register_blueprint(index_bp)
app.register_blueprint(victims_average_bp)
app.register_blueprint(active_groups_bp)
app.register_blueprint(unique_groups_bp)
app.register_blueprint(corr_victims_for_events_bp)

if __name__ == '__main__':
    app.run(debug=True)
