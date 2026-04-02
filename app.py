from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Mechanic, Vehicle, Booking

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Create Tables
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template('home.html')




@app.route('/user')
def user_dashboard():
    bookings = Booking.query.all()
    return render_template('user/dashboard.html', bookings=bookings)

@app.route('/user/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':

        # First Vehicle
        vehicle = Vehicle(
            customer_name=request.form['customer_name'],
            vehicle_no=request.form['vehicle_no'],
            model=request.form['model'],
            brand=request.form['brand'],
            year=request.form['year']
        )

        db.session.add(vehicle)
        db.session.commit()

        booking1 = Booking(
            vehicle_id=vehicle.id,
            service_type=request.form['service_type'],
            problem=request.form['problem']
        )

        db.session.add(booking1)

        # Second Vehicle (only if filled)
        if request.form.get('customer_name1'):

            vehicle1 = Vehicle(
                customer_name=request.form['customer_name1'],
                vehicle_no=request.form['vehicle_no1'],
                model=request.form['model1'],
                brand=request.form['brand1'],
                year=request.form['year1']
            )

            db.session.add(vehicle1)
            db.session.commit()

            booking2 = Booking(
                vehicle_id=vehicle1.id,
                service_type=request.form['service_type1'],
                problem=request.form['problem1']
            )

            db.session.add(booking2)

        db.session.commit()

        return redirect(url_for('user_dashboard'))

    return render_template('user/add_booking.html')




@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/admin/mechanics', methods=['GET', 'POST'])
def mechanics():
    if request.method == 'POST':
        mechanic = Mechanic(
            name=request.form['name'],
            email=request.form['email']
        )
        db.session.add(mechanic)
        db.session.commit()

    mechanics = Mechanic.query.all()
    return render_template('admin/mechanics.html', mechanics=mechanics)


@app.route('/admin/vehicles')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('admin/vehicles.html', vehicles=vehicles)


@app.route('/admin/bookings', methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        booking = Booking.query.get(request.form['booking_id'])

        if booking:
            booking.mechanic_id = request.form['mechanic_id']
            booking.status = request.form['status']
            db.session.commit()

    bookings = Booking.query.all()
    mechanics = Mechanic.query.all()

    return render_template(
        'admin/bookings.html',
        bookings=bookings,
        mechanics=mechanics
    )


if __name__ == "__main__":
    app.run(debug=True)
