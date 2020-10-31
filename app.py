from flask import Flask, request, render_template, url_for, redirect, flash, session, g, send_file, abort
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug import generate_password_hash, check_password_hash
from flask_seasurf import SeaSurf #for csrf protection
import os
import datetime
import requests as req
import pytz
app = Flask(__name__)


app.config.from_object('config')

from models import User, Agent, Booking, AssignedVehicle, Enquiry, Quote
from models import db

db.init_app(app)
csrf = SeaSurf(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    session['next_url'] = request.path
    return redirect('/login')


@app.before_request
def before_request():
    g.user = current_user


def newenquiry(data):

    src = data['source'].split(", ")
    dest = data['destination'].split(", ")
    app.logger.info(src)
    app.logger.info(dest)

    if not 1 in src or not 1 in dest:
        flash('Please select place from the list.' , 'warning')
        return False

    clientid = 01
    source = src[0]
    sourcestate = src[1]
    destination = dest[0]
    destinationstate = dest[1]
    material = data['material']
    weight = data['weight']
    date = datetime.datetime.strptime(data['date'], '%d/%m/%Y')
    trucktype = data['trucktype']

    new_enquiry= Enquiry(clientid, source, sourcestate, destination, destinationstate, material, weight, trucktype, date)
    app.logger.info(new_enquiry)
    db.session.add(new_enquiry)
    db.session.commit()
    return True

def updateenquiry(data,enquiryid,clientid):
    enquiry = Enquiry.query.filter_by(id=enquiryid).first()
    enquiry.clientid = clientid

    src = data['source'].split(", ")
    dest = data['destination'].split(", ")
    app.logger.info(src)
    app.logger.info(dest)

    try:
        src[1]
    except IndexError:
        flash('Please select Source from the list.' , 'warning')
        return False
    try:
        dest[1]
    except IndexError:
        flash('Please Destination place from the list.' , 'warning')
        return False

    enquiry.source = src[0]
    enquiry.sourcestate = src[1]
    enquiry.destination = dest[0]
    enquiry.destinationstate = dest[1]
    enquiry.material = data['material']
    enquiry.weight = data['weight']
    enquiry.date = datetime.datetime.strptime(data['date'], '%d/%m/%Y')

    db.session.commit()
    return True

def deleteenquiry(id):
    enquiry = Enquiry.query.filter_by(id=id).first()
    db.session.delete(enquiry)
    db.session.commit()
    return True


def confirm_booking(enquiryid, quoteid):
    quote = Quote.query.filter_by(id=quoteid).first()
    enquiry = Enquiry.query.filter_by(id=enquiryid).first()
    clientid = enquiry.clientid
    agentid = enquiry.agentid
    quoteid = quote.id
    source = enquiry.source
    sourcestate = enquiry.sourcestate
    destination = enquiry.destination
    destinationstate = enquiry.destinationstate
    material = enquiry.material
    weight = enquiry.weight
    date = enquiry.date
    quoteamount = quote.quoteamount

    new_booking = Booking(clientid, agentid, quoteid, source, sourcestate, destination, destinationstate, material, weight, date)
    quote.accepted = True
    enquiry.confirmed = True
    app.logger.info(new_booking)
    db.session.add(new_booking)
    db.session.commit()


def loginfn(data):
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if not user.verified:
            flash('Please wait for verification of your account.' , 'warning')
            return False
        if check_password_hash(user.pwdhash, password):
            user.authenticated = True
            user.lastlogin_on = datetime.datetime.utcnow()
            db.session.commit()
            login_user(user)
            return True
        flash('Username or Password is invalid' , 'warning')
        return False
    else:
        flash('Username or Password is invalid' , 'warning')
        return False

def register(data):
    app.logger.info(repr(data))

    place = data['city'].split(", ")

    name = data['name']
    email = data['email']
    mobilenumber = data['mobilenumber']
    phonenumber = data['phonenumber']
    address = data['address']
    city = place[0]
    state = place[1]

    password = data['password']
    passwordconfirm = data['passwordconfirm']
    user_role = 'client'

    error = False

    user = User.query.filter_by(email=email).first()
    if user:

        error = True
        flash('Email already registered','warning')
    if password != passwordconfirm:
        error = True
        flash("Passwords don't match",'warning')
    if len(mobilenumber) != 10 or not mobilenumber.isdigit():
        error = True
        flash("Mobile number is invalid",'warning')
    if error:
        app.logger.info("Error=")
        return False
    else:
        if user_role == 'agent':
            trucktypes = request.form['trucktyes']
            favroutes = request.form['favroutes']
            yearestablished = request.form['yearestablished']

            newuser = Agent(name, email, password, mobilenumber, phonenumber, address, city, state, usere_role, trucktypes, favroutes, yearestablished)

        elif user_role == 'client':
            newuser = User(name, email, password, mobilenumber, phonenumber, address, city, state, user_role)

        newuser.lastlogin_on = datetime.datetime.utcnow()
        newuser.updated_on = datetime.datetime.utcnow()
        newuser.authenticated = True
        db.session.add(newuser)
        db.session.commit()
        return True




def err(val):
    if val == "404":
        return render_template("error404.html",page="error404")
    if val == "401":
        return render_template("error401.html",page="error401")
    else:
        return render_template("unknownerror.html",page="unknownerror")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html",page="home")

    if request.method == 'POST':
        app.logger.info(repr(request.form))
        if newenquiry(request.form) :
            flash('Enquiry submitted successfully our executive will call you back within 10 minutes' , 'success')
            return redirect(url_for('index'))
        else:
            return render_template("index.html",page="home")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if g.user is not None and g.user.is_authenticated:
            return redirect(url_for('clienthome'))
        return render_template('registerlogin.html',page="registerlogin")

    elif request.method == 'POST':
        if request.form['formtype'] == "login" :
            if loginfn(request.form):
                next_url = session.get('next_url', '/')
                return redirect(next_url)
                # return redirect(url_for('clienthome'))
            else:
                return render_template('registerlogin.html',page="registerlogin", oldform = request.form)
        if request.form['formtype'] == "register" :
            if register(request.form):
                return render_template('index.html',page="registerlogin")
            else:
                return render_template('registerlogin.html',page="registerlogin", oldform = request.form)

@app.route('/logout')
@login_required
def logout():
    g.user.authenticated = False
    db.session.commit()
    logout_user()
    flash('Logged out successfully.' , 'success')
    return redirect(url_for('login'))


@app.route('/contact')
def contactus():
    return render_template("contactus.html",page="contact")


##################################################################################################
############################################# USER ##############################################
##################################################################################################


@app.route('/user', methods=['GET', 'POST'])
@login_required
def clienthome():
    if request.method == 'GET':
        enquiries =  Enquiry.query.filter_by(clientid=g.user.id).all()
        bookings =  Booking.query.filter_by(clientid=g.user.id).all()
        return render_template('profile.html', enquiries=enquiries, bookings=bookings)

    elif request.method == 'POST':
        app.logger.info(repr(request.form))

        if request.form['formtype'] == "newenquiry" :
            if newenquiry(request.form) :
                flash('Enquiry submitted successfully our executive will call you back within 10 minutes' , 'success')
                return redirect(url_for('clienthome'))

        elif request.form['type'] == "deleteenquiry" :
            if deleteenquiry(request.form['id']):
                flash('Enquiry submitted successfully our executive will call you back within 10 minutes' , 'success')
                return redirect(url_for('clienthome'))


@app.route('/user/edit',methods=['GET','POST'])
@login_required
def edituser():
    user = g.user
    error = False
    if request.method == 'GET':
        return render_template('edituser.html',page="edituser", user=user)

    elif request.method == 'POST':
        app.logger.info(repr(request.form))
        edittype = request.form['edittype']
        if edittype == 'changepassword':
            oldpassword = request.form['old-password']
            newpassword = request.form['new-password']
            passwordconfirm = request.form['password-confirm']
            if newpassword != passwordconfirm:
                error = True
                flash("Passwords don't match",'warning')

            if not check_password_hash(g.user.pwdhash, oldpassword):
                error = True
                flash("Current Password is invalid",'warning')
            if error:
                return render_template('edituser.html',page="edituser",user=user)
            else:
                g.user.pwdhash = generate_password_hash(newpassword)
                g.user.updated_on = datetime.datetime.utcnow()
                db.session.commit()
                flash("Password changed succesfully.",'success')
                return render_template('edituser.html',page="edituser",user=user)

        elif edittype == 'userdetails':
            usrname = request.form['name']
            mobno = request.form['mobilenumber']
            password = request.form['password']
            phoneno = request.form['phonenumber']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            if len(mobno) != 10 or not mobno.isdigit():
                error = True
                flash("Mobile number is invalid",'warning')

            if error:
                return render_template('edituser.html',page="edituser",user=user)
            else:
                g.user.name = usrname
                g.user.mobilenumber = mobno
                g.user.phonenumber = phonenumber
                g.user.address =address
                g.user.city = city
                g.user.state = state
                g.user.updated_on = datetime.datetime.utcnow()
                db.session.commit()
                flash("Profile updated succesfully.",'success')
                return render_template('edituser.html',page="edituser",user=user)



@app.route('/user/enquiry/<enquiryid>', methods=['GET', 'POST'])
@login_required
def editenquiy(enquiryid):
    enquiry = Enquiry.query.filter_by(id=int(enquiryid)).first()
    if enquiry:
        if request.method == 'GET':
            if enquiry.clientid == g.user.id or g.user.is_admin:
                return render_template("editenquiry.html",page="editenquiry", enquiry=enquiry)
            else:
                err(401)

        elif request.method == 'POST':
            if enquiry.clientid == g.user.id or g.user.is_admin:
                if updateenquiry(request.form,enquiryid,g.user.id) :
                    flash('Your enquiry is updated.' , 'success')
                    return render_template("editenquiry.html",page="editenquiry", enquiry=enquiry)
                else :
                    app.logger.info(repr("error"))
                    return render_template("editenquiry.html",page="editenquiry", enquiry=enquiry)
            else:
                err(401)
    else:
        err(404)

@app.route('/user/booking/<bookingid>', methods=['GET'])
def viewbooking(bookingid):
    booking = Booking.query.filter_by(id=int(bookingid)).first()
    if booking:
        if request.method == 'GET':
            if booking.clientid == g.user.id or g.user.is_admin:
                return render_template("viewbooking.html",page="viewbooking", booking=booking)
            else:
                err(401)
        else:
            err(401)
    else:
        err(404)

##################################################################################################
############################################# ADMIN ##############################################
##################################################################################################


@app.route('/admin/users',methods=['GET','POST'])
@login_required
def admin_users():
    if g.user.is_admin:
        if request.method == 'POST':
            app.logger.info(request.form)
            formtype = request.form['formtype']
            user_id = request.form['userid']
            user = User.query.get(int(user_id))
            if formtype == 'approve':
                user.verified = True
                db.session.add(user)
            elif formtype == 'reject':
                if user.verified == False:
                    db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin_users'))

        unverifiedusers = User.query.filter_by(verified=False).order_by(User.id.desc()).all()
        verified = User.query.filter_by(verified=True).order_by(User.id.desc()).all()
        return render_template('admin-users.html', unverifiedusers = unverifiedusers, verified=verified, page="admin-users" )

@app.route('/admin/enquiries', methods=['GET','POST'])
@login_required
def admin_enquiries():
    if g.user.is_admin:
        if request.method == 'GET':
            newenquiries = Enquiry.query.filter(Enquiry.valid==True, Enquiry.processed==False).order_by(Enquiry.date.desc()).all()
            processedenquiries = Enquiry.query.filter(Enquiry.valid==True, Enquiry.processed==True).order_by(Enquiry.date.desc()).all()
            app.logger.info(repr(newenquiries))
            app.logger.info(repr(processedenquiries))
            return render_template('admin-enquiries.html',page="admin-enquiries", newenquiries=newenquiries, processedenquiries=processedenquiries)
        if request.method == 'POST':
            formtype = request.form['formtype']
            enquiry_id = request.form['enquiryid']
            enquiry = Enquiry.query.get(int(enquiry_id))
            app.logger.info(repr(enquiry))
            if formtype == 'processed':
                enquiry.processed = True
                db.session.add(enquiry)
            db.session.commit()
            return redirect(url_for('admin_enquiries'))

    else:
        return render_template('message.html',heading="Unauthorised Access",message="This page is out of your league...",route="edituser",routemsg="Click here to go back")

@app.route('/admin/enquiries/<enqid>', methods=['GET','POST'])
@login_required
def admin_viewenquiry(enqid):
    if g.user.is_admin:
        enquiry = Enquiry.query.filter_by(id=enqid).first()
        quotes = Quote.query.filter_by(enquiryid=enqid).all()
        if enquiry:
            app.logger.info(repr("Get enquiry " + str(enquiry)))
            if request.method == 'GET':
                app.logger.info(repr("Get enquiry no: " + str(enquiry.id)))
                return render_template('admin-viewenquiry.html',page="admin-enquiry", enquiry=enquiry, quotes=quotes)
            if request.method == 'POST':
                app.logger.info(repr("Cinfirm Quote"))
                if request.form['formtype'] == "confirm":
                    if confirm_booking(request.form['enquiryid'],request.form['quoteid']):
                        flash("Enquiry not found",'success')
                        return render_template('admin-viewenquiry.html',page="admin-enquiry", enquiry=enquiry, quotes=quotes)
                    else:
                        flash("Error while booking",'warning')
                        return render_template('admin-viewenquiry.html',page="admin-enquiry", enquiry=enquiry, quotes=quotes)
                else:
                    flash("Unknown request",'warning')
                    return render_template('admin-viewenquiry.html',page="admin-enquiry", enquiry=enquiry, quotes=quotes)

        app.logger.info(repr("No Enquiry"))
        flash("Enquiry not found",'warning')
        return redirect(url_for('admin_enquiries'))
    else:
        app.logger.info(repr("Error not admin"))
        return render_template('message.html',heading="Unauthorised Access",message="This page is out of your league...",route="edituser",routemsg="Click here to go back")


@app.route('/test/<template>')
def test(template):
    """ Route for quickly testing templates under development"""
    return render_template(template+'.html')


def utc_to_local(utc_dt):
    """Used for converting time stored as UTC to Asia/Kolkata timezone and
    display it in preferred formats. Depends on pytz"""

    local_tz = pytz.timezone('Asia/Kolkata')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050)
