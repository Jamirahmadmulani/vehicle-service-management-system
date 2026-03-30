from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------- MECHANIC MODEL ----------------
class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    bookings = db.relationship("Booking", backref="mechanic", lazy=True)


# ---------------- VEHICLE MODEL ----------------
class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    vehicle_no = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)

    bookings = db.relationship("Booking", backref="vehicle", lazy=True)


# ---------------- BOOKING MODEL ----------------
class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id"),
        nullable=False
    )

    service_type = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Pending")

    mechanic_id = db.Column(
        db.Integer,
        db.ForeignKey("mechanic.id"),
        nullable=True
    )