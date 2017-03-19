from werkzeug import generate_password_hash
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """The base class model for Users, Agents
    User role can be 'client' or 'agent' or 'admin' """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique = True)
    mobilenumber = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    pwdhash = db.Column(db.String, nullable=False)

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    lastlogin_on = db.Column(db.DateTime)

    authenticated = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default = False)
    verified = db.Column(db.Boolean, default = False)
    user_role = db.Column(db.String, nullable=False)
    user_active = db.Column(db.Boolean, default=True)

    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    enquiry = db.relationship('Enquiry', backref='user', lazy='dynamic')

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


    def __init__(self, name, email, password, mobilenumber, phonenumber, address, city, state, user_role):
        self.name = name
        self.email = email
        self.mobilenumber = mobilenumber
        self.pwdhash = generate_password_hash(password)
        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()
        self.user_role = user_role
        self.address = address
        self.state = state
        self.city = city


    def __repr__(self):
        return '<id: %r - email: %r - role:%r>' %(self.id, self.email, self.user_role)

class Agent(db.Model):
    """The database model for Agent"""
    __tablename__="agent"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique = True)
    mobilenumber = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    pwdhash = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime)
    trucktypes = db.Column(db.String, nullable=False)
    favroutes = db.Column(db.String, nullable=False)
    rank = db.Column(db.Integer, nullable=False, default = 0)
    yearestablished = db.Column(db.String, nullable=False)

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    lastlogin_on = db.Column(db.DateTime)

    authenticated = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default = False)
    user_active = db.Column(db.Boolean, default=True)


    bookings = db.relationship('Booking', backref='agent', lazy='dynamic')

    quotes = db.relationship('Quote', backref='agent', lazy='dynamic')


    def __init__(self, name, email, password, mobilenumber, phonenumber, address, city, state, trucktypes, favroutes, yearestablished):
        self.name = name
        self.email = email
        self.mobilenumber = mobilenumber
        self.pwdhash = generate_password_hash(password)
        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()
        self.address = address
        self.state = state
        self.city = city
        self.trucktypes = trucktypes
        self.favroutes = favroutes
        self.yearestablished = yearestablished

class Booking(db.Model):
    """The database model for Bookings"""
    __tablename__="booking"
    id = db.Column(db.Integer, primary_key=True)
    clientid = db.Column(db.Integer, db.ForeignKey('user.id'))
    agentid = db.Column(db.Integer, db.ForeignKey('agent.id'))
    quoteid = db.Column(db.Integer, db.ForeignKey('quote.id'))
    source = db.Column(db.String, nullable=False)
    sourcestate = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    destinationstate = db.Column(db.String, nullable=False)
    material = db.Column(db.String, nullable=False)
    weight = db.Column(db.String, nullable=True)
    date = db.Column(db.Date)
    payementtype = db.Column(db.String, nullable=True , default="Cash")
    quoteamount = db.Column(db.Integer, nullable=True)


    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    journeystarted = db.Column(db.Boolean, default = False)
    journeycompleted = db.Column(db.Boolean, default = False)
    payementdone = db.Column(db.Boolean, default = False)
    lrcreated = db.Column(db.Boolean, default = False)
    vehicleassigned = db.Column(db.Boolean, default = False)

    assignedvehicles = db.relationship('AssignedVehicle', backref='booking', lazy='dynamic')



    def __init__(self, clientid, agentid, quoteid, source, sourcestate, destination, destinationstate, material, weight, date):
        self.clientid = clientid
        self.agentid = agentid
        self.quoteid = quoteid
        self.source = source
        self.sourcestate = sourcestate
        self.destination = destination
        self.destinationstate = destinationstate
        self.material = material
        self.weight = weight
        self.date = date

        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()

class AssignedVehicle(db.Model):
    """The database model for Vehicles Assigned to clients"""
    __tablename__="assignedvehicle"
    id = db.Column(db.Integer, primary_key=True)
    bookingid = db.Column(db.Integer, db.ForeignKey('booking.id'))
    vehiclenumber = db.Column(db.String, nullable=True)
    drivermobnumber = db.Column(db.String, nullable=True)
    drivername = db.Column(db.String, nullable=True)
    driverlicencenumber = db.Column(db.String, nullable=True)
    trackingid = db.Column(db.String, nullable=True)
    lrnumber = db.Column(db.String, nullable=True)

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)


    def __init__(self, bookingid, vehiclenumber, drivermobnumber, drivername, driverlicencenumber, trackingid, lrnumber):
        self.bookingid = bookingid
        self.vehiclenumber = vehiclenumber
        self.drivermobnumber = drivermobnumber
        self.drivername = drivername
        self.driverlicencenumber = driverlicencenumber
        self.trackingid = trackingid
        self.lrnumber = lrnumber

        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()


class Enquiry(db.Model):
    """The database model for Enquiries"""
    __tablename__="enquiry"
    id = db.Column(db.Integer, primary_key=True)
    clientid = db.Column(db.Integer, db.ForeignKey('user.id'))
    agentid = db.Column(db.Integer, db.ForeignKey('agent.id'))
    source = db.Column(db.String, nullable=False)
    sourcestate = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    destinationstate = db.Column(db.String, nullable=False)
    weight = db.Column(db.String, nullable=True)
    material = db.Column(db.String, nullable=False)
    trucktype = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    lowestquote = db.Column(db.Integer, nullable=True)

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)



    cancelled = db.Column(db.Boolean, default = False)
    failedenquiry = db.Column(db.Boolean, default = False)
    confirmed = db.Column(db.Boolean, default = False)
    valid = db.Column(db.Boolean, default = True)
    processed = db.Column(db.Boolean, default = False)

    quotes = db.relationship('Quote', backref='enquiry', lazy='dynamic')

    def __init__(self, clientid, source, sourcestate, destination, destinationstate, material, weight, trucktype, date):
        self.clientid = clientid
        self.source = source
        self.sourcestate = sourcestate
        self.destination = destination
        self.destinationstate = destinationstate
        self.material = material
        self.weight = weight
        self.date = date
        self.trucktype = trucktype

        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()


class Quote(db.Model):
    """The database model for Enquiries"""
    __tablename__="quote"
    id = db.Column(db.Integer, primary_key=True)
    enquiryid = db.Column(db.Integer, db.ForeignKey('enquiry.id'))
    agentid = db.Column(db.Integer, db.ForeignKey('agent.id'))
    quoteamount = db.Column(db.Integer, nullable=False)

    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    accepted = db.Column(db.Boolean, default = False)

    quotes = db.relationship('Booking', backref='quote', lazy='dynamic')

    def __init__(self, enquiryid, agentid, quoteamount):
        self.enquiryid = enquiryid
        self.agentid = agentid
        self.quoteamount = quoteamount

        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()
