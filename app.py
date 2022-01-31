from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import EmailType


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Inventory(db.Model):
    i_id = db.Column(db.Integer, primary_key=True)
    v_name = db.Column(db.String(200), nullable=False)
    v_count = db.Column(db.Integer, nullable=False)
   
class Customers(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name =  db.Column(db.String(500), nullable=False)
    c_email = db.Column(EmailType, nullable=False)
    c_phone = db.Column(db.Integer)
    
class Rentals(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    c_name =  db.Column(db.String(500), nullable=False)
    rental_date = db.Column(db.String(200), nullable=False)
    return_date = db.Column(db.String(200), nullable=True)
    vehicle_type = db.Column(db.String(200), nullable=False)
    

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    from app import db
    db.create_all()
    if request.method == 'POST':
        cname = request.form['c_name']
        cemail = request.form['c_email']
        cphone = request.form['c_phone']
        
        cst = Customers(c_name=cname, c_email=cemail, c_phone=cphone)
        db.session.add(cst)
        db.session.commit()
        flash('Customer Details added Succesfully', 'insertion')
        return redirect(url_for('customer'))
        
    allcustomer = Customers.query.all()
    return render_template('customer.html', allcustomer=allcustomer)

@app.route("/customer/delete/<int:c_id>")
def customerdelete(c_id):
    cust = Customers.query.filter_by(c_id=c_id).first()
    db.session.delete(cust)
    db.session.commit()
    flash('Customer Details Deleted Successfully', 'deletion')
    return redirect(url_for('customer'))

@app.route('/rental', methods=['GET', 'POST'])
def rentals():
    if request.method == 'POST':
        vehicletype = request.form['v_type']
        res = Inventory.query.filter_by(v_name=vehicletype).first()
        if res.v_count <= 0:
            flash(' "{}" cannot be rented as it is already booked'.format(res.v_name))
            return redirect(url_for('rentals'))
        else:
            cname = request.form.get('c_name')
            
            rentaldate = datetime.strptime(request.form['rental_date'], '%Y-%m-%d')
            if request.form['return_date'] == '':
                returndate = ''
            else:
                returndate = datetime.strptime(request.form['return_date'], '%Y-%m-%d')
            vehicletype = request.form['v_type']
            
        
            rental = Rentals(c_name=cname, rental_date=rentaldate, return_date=returndate, vehicle_type=vehicletype)
            db.session.add(rental)
            db.session.commit()
            
            res.v_count -= 1
            db.session.add(res)
            db.session.commit()
            flash('Booking added Succesfully', 'insertion')
            return redirect(url_for('rentals'))
    
    allcustomer = Customers.query.all()
    allbooking = Rentals.query.all()
    allinventory = Inventory.query.all() 
    return render_template('rental.html', allcustomer=allcustomer, allbooking = allbooking, allinventory=allinventory)

@app.route("/rental/delete/<int:r_id>/<name>")
def rentaldelete(r_id, name):
    rental = Rentals.query.filter_by(r_id=r_id).first()
    db.session.delete(rental)
    db.session.commit()
    
    res = Inventory.query.filter_by(v_name=name).first()
    res.v_count += 1
    db.session.add(res)
    db.session.commit()
    flash('Booking Deleted and Inventory Updated', 'deletion')
    return redirect(url_for('rentals'))
    


@app.route('/inventory')
def inventory():  
    invent = Inventory.query.first()  
    if not invent:
        add_inventory1 = Inventory(v_name ='bikes', v_count= 2)
        add_inventory2 = Inventory(v_name ='cycle', v_count= 3)
        add_inventory3 = Inventory(v_name ='car', v_count= 1)
        add_inventory4 = Inventory(v_name ='boat', v_count= 2)
        db.session.add_all([add_inventory1, add_inventory2, add_inventory3, add_inventory4])
        db.session.commit()
    allinventory = Inventory.query.all()  
    return render_template('inventory.html', allinventory=allinventory)


@app.route('/developer')
def developer():
    return render_template('developer.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    
