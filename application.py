from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, url_for, redirect, session, request
from forms import Register, Login, Contribution
import stripe

########APP SETUP #############
app=application=Flask(__name__)
app.secret_key = 'si3mshady'

######## MONGO DB SETUP ###########
conn = MongoClient("mongodb://localhost:27017/")
db = conn['ForksOfJuly_Reunion']
current_collection = db['FamilyReunion']

#########STRIPE "Dummy Data" PAYMENT SETUP############

publishable_key = "pk_test_atLiopi1CRNnG8miSlCSbt7D00EIWF79mX"
stripe.api_key = "sk_test_Q9gqAZWXMHJQlG8UMgN5QQCu00o847hV1k"


def check_username_exist(username):
    if current_collection.find_one({"username": username}):
        return True

############## VIEWS #######################
@app.route('/',methods=["GET"])
def home():
    return render_template('home.html', pk=publishable_key)


@app.route('/register', methods=["GET","POST"])
def register():
    register_form = Register()
    if register_form.validate_on_submit():
        first = register_form.firstname.data
        last = register_form.lastname.data
        username = register_form.username.data
        if check_username_exist(username):
            flash("Username already in use!")
            return redirect(url_for("register"))
        password_hash = generate_password_hash(password=register_form.password.data)
        current_collection.insert({"firstname": first, "lastname": last, "username":username,
                                   "hashed_pw": password_hash})
        flash(f"Thank you for registering {first}!")
        return redirect(url_for("register"))
    return render_template('register.html', form=register_form)

@app.route('/login', methods=["GET","POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        username = login_form.username.data
        passwd = login_form.password.data
        hp = current_collection.find_one({"username":username})['hashed_pw']
        if not check_password_hash(hp,passwd):
            flash("Incorrect username or password!")
            return redirect(url_for('login'))
        session['logged_in'] = True
        flash(f"You are logged in {username}!")
        return redirect(url_for('login'))
    return  render_template('login.html', form=login_form)


@app.route('/contribution',methods=["GET","POST"])
def contribution():
    inventory = Contribution()
    if inventory.validate_on_submit():
        username = inventory.username.data
        item = inventory.item.data
        quantity = inventory.quantity.data
        current_collection.update({"username": username}, {"$set": {"quantity": quantity, "item": item}})
        flash(f"Thank you for contributing {username}!")
        return redirect(url_for('home'))
    return render_template('contribution.html', form=inventory)

@app.route('/charge', methods=['POST'])
def charge():
    amount = 50
    customer = stripe.Customer.create(
        email='si3mshady@si3mshady.com',
        source=request.form['stripeToken']
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Forth of July'
    )
    return redirect(url_for('thankYou'))

@app.route('/thankYou')
def thankYou():
    return render_template('thankyou.html')


@app.route('/list')
def list():
    data = current_collection.find({})
    data = [i for i in data]
    try:
        items_dict = {i['username']: i['item'] for i in data}
    except KeyError:
        items_dict = False
    return render_template('list_all.html', items_dict=items_dict)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash("You have logged out!")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


#Practice creating basic websites with Flask, MongoDB, that registers users and accepts "dummy" payments with Stripe
#Elliott Arnold 7-3-19


#https://stripe.com/docs/testing
