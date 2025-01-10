
# Developing a Web Application for Pizza Corner

A dynamic web application developed to enhance the operations of Pizza Corner, a newly established pizza business. This application features an intuitive interface for managing items, processing customer orders, and generating invoices, making it a complete solution for running a pizza shop efficiently.

![pizza_icon1](https://github.com/user-attachments/assets/2aa23281-3df2-46d7-adcc-6fcb34442dc7)

## 📖 Table of Contents

1. About the Project
2. Features
3. Technologies Used
4. Setup and Installation
5. Database Structure
6. Usage
7. License

## 1. About the Project

This project is designed to cater to the requirements of Pizza Corner by providing an all-in-one platform for:

* Managing pizza types, toppings, and beverages.
* Handling customer orders and shopping cart functionality.
* Generating invoices with detailed item descriptions, taxes, and total amounts.

## 2. Features

1. Item Management

* Add, edit, and delete pizzas, toppings, and beverages.
* Categorize items into veg and non-veg options.

2. Order Management

* Add items to the cart with specified quantities and toppings.
* Automatically calculate item subtotals.

3. Invoice Generation

* Display order details including items, quantities, taxes, and the total amount.
* Save orders to a database for future reference.

4. User-Friendly Interface

* Responsive design for seamless usage on desktops and mobile devices.
## 3. Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Dependencies: Flask-SQLAlchemy, Jinja2
## 4. Setup and Installation

Prerequisites:
- Python 3.8 or higher
- pip (Python package installer)


1. Install dependancies:

```bash
  pip install -r requirements.txt

```
2. Run the Application:

```bash
  python app.py
```

3. Access the Application in your Browsers:

```bash
  http://127.0.0.1:5000/
```
    
## 5. Database and Structure

The project uses SQLite as its database, stored in the instance folder. Key tables include:

- Items: Stores details about pizzas, toppings, and beverages.
- Orders: Saves order details, including items, prices, and quantities.
- 
## 6. Usage

* Homepage: General welcome message about the company.
![Screenshot 2025-01-10 005359](https://github.com/user-attachments/assets/f7a86a82-7e25-4af2-92e1-d19df160463c)

* Menupage: Browse through available pizzas and beverages.
![Screenshot 2025-01-10 005444](https://github.com/user-attachments/assets/521523c5-e6e3-45e8-a39c-89d4f5d48e13)

* Cart: Add items to the cart and modify quantities.
![Screenshot 2025-01-10 005653](https://github.com/user-attachments/assets/4fe30df3-9dba-4cc3-adc0-c9f3c1dda261)

* Checkout: Finalize orders, view tax calculations, and download invoices.
![Screenshot 2025-01-10 005740](https://github.com/user-attachments/assets/13bf8d16-64b0-4fac-b569-f9bbb6da03ec)

## Contact

For any inquiries or feedback, please contact:
- Developer: Yashvvinie Santhakumar
- Email: yashvvinie2000@gmail.com
