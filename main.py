from flask import Flask, render_template, redirect, url_for, request
from controller import DbManagement


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Creating the homepage"""
    return render_template("index.html")


@app.route('/insert/category', methods=['GET'])
def insert_category():
    """It will return the Insert Category's page"""
    return render_template("insert_category.html")


@app.route('/insert/category/send', methods=['POST'])
def send_category():
    """It will send the category for the database to receive and insert it"""
    data = request.form
    try: DbManagement().insert_category(data["name"].title())
    except: pass
    return redirect(url_for("insert_category"))


@app.route('/insert/product', methods=['GET'])
def insert_product():
    """It will return the Insert Product's page"""
    categories = DbManagement().get_categories()
    return render_template("insert_product.html", categories=categories)


@app.route('/insert/product/send', methods=['POST'])
def send_product():
    """It will send the product for the database to receive and insert it"""
    data = request.form
    try: DbManagement().insert_product(data["name"].title(), data["price"], data["amount"], data["category-name"].title())
    except: pass
    return redirect(url_for("insert_product"))


@app.route('/reduce', methods=['GET'])
def reduce_inventory():
    """It will return the Reduce Inventory's page """
    return render_template('reduce_inventory.html')


@app.route('/reduce/send', methods=['POST'])
def send_reduce():
    """It will send the product and the amount for the database to receive,
    remove it and recalculate the total"""
    data = request.form
    try: DbManagement().reduce_inventory(data)
    except: pass
    return redirect(url_for("reduce_inventory"))


@app.route('/remove/product', methods=['GET'])
def remove_product():
    """It will return the Remove Product's page"""
    return render_template("remove_product.html")


@app.route('/remove/product/send', methods=['POST'])
def send_remove_product():
    """It will send the product for the database to receive and remove it"""
    data = request.form
    try: DbManagement().remove_product(data["name"].title())
    except: pass
    return redirect(url_for("remove_product"))


@app.route('/remove/category', methods=['GET'])
def remove_category():
    """It will return the Remove Category's page """
    return render_template('remove_category.html')


@app.route('/remove/category/send', methods=['POST'])
def send_remove_category():
    """It will send the category for the database to receive and remove it"""
    data = request.form
    try: DbManagement().remove_category(data["name"].title())
    except: pass
    return redirect(url_for("remove_category"))


@app.route('/view/products', methods=['GET'])
def view():
    """It will return the View Product's page"""
    values = DbManagement().get_totals()
    products = DbManagement().get_products()
    return render_template("view.html", products=products, values=values)

if __name__ == '__main__':
    app.run(debug=True)