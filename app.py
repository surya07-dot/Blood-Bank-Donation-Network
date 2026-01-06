from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


# MODELS
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Donor(db.Model):
    __tablename__ = "donors"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    last_donated = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BloodRequest(db.Model):
    __tablename__ = "blood_requests"
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(150), nullable=False)
    hospital_name = db.Column(db.String(200), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending / Approved / Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BloodStock(db.Model):
    __tablename__ = "blood_stock"
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(5), unique=True, nullable=False)
    units_available = db.Column(db.Integer, nullable=False, default=0)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ROUTES
def register_routes(app):
    @app.route("/")
    def index():
        stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        donors_count = Donor.query.count()
        pending_requests = BloodRequest.query.filter_by(status="Pending").count()
        return render_template(
            "index.html",
            stock=stock,
            donors_count=donors_count,
            pending_requests=pending_requests,
        )

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash("Logged in successfully!", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard"))
            else:
                flash("Invalid email or password", "danger")

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match", "warning")
                return render_template("register.html")

            existing = User.query.filter_by(email=email).first()
            if existing:
                flash("Email already registered, please login.", "warning")
                return redirect(url_for("login"))

            user = User(name=name, email=email)
            user.set_password(password)
            # First registered user becomes admin by default (simple logic)
            if User.query.count() == 0:
                user.is_admin = True
            db.session.add(user)
            db.session.commit()
            flash("Account created! You can now login.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    @app.route("/donor/register", methods=["GET", "POST"])
    def donor_register():
        if request.method == "POST":
            full_name = request.form.get("full_name")
            age = int(request.form.get("age") or 0)
            gender = request.form.get("gender")
            blood_group = request.form.get("blood_group")
            phone = request.form.get("phone")
            email = request.form.get("email")
            city = request.form.get("city")
            last_donated_str = request.form.get("last_donated")

            last_donated = None
            if last_donated_str:
                try:
                    last_donated = datetime.strptime(last_donated_str, "%Y-%m-%d").date()
                except ValueError:
                    flash("Invalid last donated date format.", "warning")

            donor = Donor(
                full_name=full_name,
                age=age,
                gender=gender,
                blood_group=blood_group,
                phone=phone,
                email=email,
                city=city,
                last_donated=last_donated,
            )
            db.session.add(donor)

            # Increase stock by 1 unit for that blood group (simple logic)
            stock = BloodStock.query.filter_by(blood_group=blood_group).first()
            if not stock:
                stock = BloodStock(blood_group=blood_group, units_available=1)
                db.session.add(stock)
            else:
                stock.units_available += 1

            db.session.commit()
            flash("Donor registered successfully! Thank you for saving lives.", "success")
            return redirect(url_for("donor_register"))

        return render_template("donor_register.html")

    @app.route("/request-blood", methods=["GET", "POST"])
    def request_blood():
        if request.method == "POST":
            patient_name = request.form.get("patient_name")
            hospital_name = request.form.get("hospital_name")
            blood_group = request.form.get("blood_group")
            units = int(request.form.get("units") or 0)
            phone = request.form.get("phone")

            blood_request = BloodRequest(
                patient_name=patient_name,
                hospital_name=hospital_name,
                blood_group=blood_group,
                units=units,
                phone=phone,
            )
            db.session.add(blood_request)
            db.session.commit()
            flash("Blood request submitted successfully! We will contact you soon.", "success")
            return redirect(url_for("request_blood"))

        return render_template("request_blood.html")

    @app.route("/inventory")
    def inventory():
        stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        return render_template("inventory.html", stock=stock)

    @app.route("/dashboard")
    @login_required
    def dashboard():
        donors = Donor.query.order_by(Donor.created_at.desc()).limit(5).all()
        recent_requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).limit(5).all()
        stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        # Use React-powered dashboard
        return render_template(
            "dashboard_react.html",
            donors=donors,
            recent_requests=recent_requests,
            stock=stock,
        )

    @app.route("/requests/manage/<int:request_id>/<string:action>")
    @login_required
    def manage_request(request_id, action):
        if not current_user.is_admin:
            flash("Only admin users can manage requests.", "danger")
            return redirect(url_for("dashboard"))

        blood_request = BloodRequest.query.get_or_404(request_id)
        if action not in ["approve", "reject"]:
            flash("Invalid action.", "warning")
            return redirect(url_for("dashboard"))

        if action == "approve":
            stock = BloodStock.query.filter_by(blood_group=blood_request.blood_group).first()
            if not stock or stock.units_available < blood_request.units:
                flash("Not enough stock to approve this request.", "danger")
                return redirect(url_for("dashboard"))

            stock.units_available -= blood_request.units
            blood_request.status = "Approved"
        else:
            blood_request.status = "Rejected"

        db.session.commit()
        flash(f"Request {action}d successfully.", "success")
        return redirect(url_for("dashboard"))

    # API ENDPOINTS FOR REACT COMPONENTS
    @app.route("/api/stats")
    @login_required
    def api_stats():
        """Get dashboard statistics for React components"""
        total_donors = Donor.query.count()
        total_requests = BloodRequest.query.count()
        pending_requests = BloodRequest.query.filter_by(status="Pending").count()
        approved_requests = BloodRequest.query.filter_by(status="Approved").count()
        
        return {
            "total_donors": total_donors,
            "total_requests": total_requests,
            "pending_requests": pending_requests,
            "approved_requests": approved_requests
        }

    @app.route("/api/blood-stock")
    def api_blood_stock():
        """Get blood stock data for React charts"""
        stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        return {
            "stock": [
                {"blood_group": s.blood_group, "units": s.units_available}
                for s in stock
            ]
        }

    @app.route("/api/recent-donors")
    @login_required
    def api_recent_donors():
        """Get recent donors for React components"""
        donors = Donor.query.order_by(Donor.created_at.desc()).limit(10).all()
        return {
            "donors": [
                {
                    "id": d.id,
                    "full_name": d.full_name,
                    "blood_group": d.blood_group,
                    "city": d.city,
                    "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for d in donors
            ]
        }

    @app.route("/api/recent-requests")
    @login_required
    def api_recent_requests():
        """Get recent blood requests for React components"""
        requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).limit(10).all()
        return {
            "requests": [
                {
                    "id": r.id,
                    "patient_name": r.patient_name,
                    "hospital_name": r.hospital_name,
                    "blood_group": r.blood_group,
                    "units": r.units,
                    "status": r.status,
                    "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for r in requests
            ]
        }


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
