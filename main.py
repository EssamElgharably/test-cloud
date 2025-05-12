# from app.infrastructure.db.models import Base
# from app.infrastructure.db.session import engine
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
# from app.interfaces.routes.auth_routes import auth_bp
# from app.interfaces.routes.appointment_routes import appointment_bp
# from app.interfaces.routes.doctor_routes import doctor_bp
# from app.interfaces.routes.billing_routes import billing_bp

# Create all tables
# Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder='app/frontend')
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/doctor/dashboard")
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

@app.route("/staff/dashboard")
def staff_dashboard():
    return render_template("staff_dashboard.html")

# Register Blueprints
# app.register_blueprint(auth_bp, url_prefix="/api/auth")
# app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
# app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
# app.register_blueprint(billing_bp, url_prefix="/api/billing")

if __name__ == "__main__":
    app.run(debug=True)