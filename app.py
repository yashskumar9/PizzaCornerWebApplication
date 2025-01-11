from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import logging
import json
from prices import TOPPING_PRICES, PIZZA_PRICES, BEVERAGE_PRICES
import re
import smtplib

load_dotenv()
receipt_items = []

my_email = os.getenv('MY_EMAIL')
my_password = os.getenv('MY_PASSWORD')


# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza = db.Column(db.String(50))
    toppings = db.Column(db.String(200))
    beverage = db.Column(db.String(50))
    sub_total = db.Column(db.Float)
    tax = db.Column(db.Float)
    total = db.Column(db.Float)

    def __repr__(self):
        return f'<Order {self.id}>'


# Create the database tables
with app.app_context():
    db.create_all()

# Enable logging for SQLAlchemy to debug database operations
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def receipt_format():
    receipt_text = ["=== RECEIPT ===\n", "Thank you for your order!\n", "--------------------------\n",
                    f"{'Description':<155}{'Unit Price':<20}{'Quantity':<15}{'Price':<15}\n", "-" * 205 + "\n"]

    subtotal = 0
    for item in receipt_items:
        description = ', '.join([f'{item[k]}' for k in ['pizza', 'beverage', 'toppings'] if item.get(k)])
        unit_price = f"${item.get('unit_price', 0.00):.2f}"
        quantity = str(item.get('quantity', 1))
        price = f"${item.get('price', 0.00):.2f}"
        receipt_text.append(f"{description:<155}{unit_price:<20}{quantity:<15}{price:<15}\n")
        subtotal += item.get('price', 0.00)

    receipt_text.append("\n")
    receipt_text.append(f"{'Subtotal':<20}: ${subtotal:.2f}\n")
    receipt_text.append(f"{'Tax (10%)':<20}: ${subtotal * 0.1:.2f}\n")
    receipt_text.append(f"{'Total':<20}: ${subtotal * 1.1:.2f}\n")
    receipt_text.append("\nThank you for visiting! Have a great day!\n")

    return receipt_text


def send_email(email):
    receipt_msg = receipt_format()

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject: Pizza Corner - E-Receipt \n\n{'\n'.join(receipt_msg)}"
        )

    return True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/order')
def add_site():
    return render_template('index.html')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pizza = request.form.get('pizza')
    toppings = request.form.getlist('toppings')
    beverage = request.form.get('beverage')

    # Calculate total price
    total_price = PIZZA_PRICES[pizza]
    toppings_price = sum(TOPPING_PRICES[topping] for topping in toppings)
    beverage_price = BEVERAGE_PRICES[beverage]

    # Store item in session
    if 'cart' not in session:
        session['cart'] = []
    total_price = total_price + toppings_price + beverage_price
    if total_price != 0:
        session['cart'].append({
            'id': len(session['cart']),
            'pizza': pizza,
            'toppings': toppings,
            'beverage': beverage,
            'price': total_price
        })
        session.modified = True

    return redirect(url_for('cart'))


@app.route('/delete_item/<int:index>', methods=['POST'])
def delete_item(index):
    info_cart = session['cart']

    item_to_remove = None
    for idx, item in enumerate(info_cart):
        if item['id'] == index:
            item_to_remove = idx
            break

    if item_to_remove is not None:
        del session['cart'][item_to_remove]

    session['total'] = sum(item['price'] for item in session['cart'])

    flash('Item removed successfully!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    if not session['cart']:
        total = 0
    else:
        total = sum(item['price'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)


@app.route('/finalize_order', methods=['POST'])
def finalize_order():
    try:
        if 'cart' not in session or not session['cart']:
            return render_template('error.html', message='Cart is empty or missing!')

        total_price = 0

        for item in session['cart']:
            unit_price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            price = unit_price * quantity

            total_price += price

            if unit_price == 0:
                continue

            receipt_items.append({
                'pizza': item.get('pizza', 'None'),
                'toppings': item.get('toppings', 'None'),
                'beverage': item.get('beverage', 'None'),
                'unit_price': unit_price,
                'quantity': quantity,
                'price': price,
            })

            new_order = Order(
                pizza='None' if item['pizza'] == 'Select' else item['pizza'],
                toppings=json.dumps(item.get('toppings', 'None')),
                beverage='None' if item['beverage'] == 'Select' else item['beverage'],
                sub_total=price,
                tax=price * 0.1,
                total=price * 1.1
            )
            db.session.add(new_order)

        db.session.commit()

        # Clear the cart
        session.pop('cart', None)

        # Calculate totals and tax
        tax = total_price * 0.1
        total = total_price + tax

        # Pass data to template
        return render_template('checkout.html', items=receipt_items, total=total, tax=tax, subtotal=total_price)

    except Exception as e:
        db.session.rollback()  # Rollback the transaction if any error occurs
        return f"An error occurred: {str(e)}"


@app.route('/e_receipt')
def get_email():
    return render_template('e_receipt.html')


@app.route('/e_receipt', methods=['POST', 'GET'])
def generate_receipt():
    email = request.form.get('email')
    if not is_valid_email(email):
        return redirect(url_for('e_receipt'))

    if send_email(email):
        print('Success')
        return render_template('success.html')

    return render_template('e_receipt.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Ensure that the session is removed after each request."""
    db.session.remove()


if __name__ == '__main__':
    app.run(debug=True)
