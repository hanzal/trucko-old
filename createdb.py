from app import app
from models import db
import datetime
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

#add sample entries
from app import User, Agent, Booking, AssignedVehicle, Enquiry, Quote
with app.app_context():
    u1 = User("admin", "hanzal007@gmail.com", "qwerty123", "8281900163", "8089296240", "Valiyangadi House, Panayikulam P.O", "Ernakulam", "Kerala", "Admin")
    u1.is_admin = True
    u1.verified = True
    db.session.add(u1)

    a1 = Agent("Test Agent", "testagent@gmail.com", "qwerty123", "8281900163", "8089296240", "Valiyangadi House, Panayikulam P.O", "Ernakulam", "Kerala", "anytype", "kerala | karnataka", "2015")
    a1.is_admin = True
    a1.verified = True
    db.session.add(a1)

    e1 = Enquiry(1,"Kochi","Kerala","Mangalapuram","Karnatka","Calcium Carbide","<9 Tonnes","Lorry",datetime.datetime.strptime("03/08/2016", '%d/%m/%Y'))
    e2 = Enquiry(2,"Mangalapuram","Karnatka","Kochi","Kerala","Calcium Carbide","<9 Tonnes","Lorry",datetime.datetime.strptime("03/08/2016", '%d/%m/%Y'))
    db.session.add(e1)
    db.session.add(e2)

    eq1 = Quote(1,1,18000)
    eq2 = Quote(1,1,27500)
    eq3 = Quote(1,1,37990)
    eq4 = Quote(1,1,48450)
    db.session.add(eq1)
    db.session.add(eq2)
    db.session.add(eq3)
    db.session.add(eq4)

    av1 = AssignedVehicle(1,"KA26C2355","8281920566","Hanjjjim","51/6564/karna","","0359")
    db.session.add(av1)

    b1 = Booking(1,1,1,"Kochi","Kerala","Mangalapuram","Karnatka","Calcium Carbide","<9 Tonnes",datetime.datetime.strptime("03/08/2016", '%d/%m/%Y'))
    db.session.add(b1)

    db.session.commit()



