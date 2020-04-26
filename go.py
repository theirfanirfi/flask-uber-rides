from app import db, application
from app.models.models import *
from pprint import pprint
import sys
passenger_zipcode = 10121
s_p_zipcode = str(passenger_zipcode)
from sqlalchemy import text

s1 = User.query.filter(User.roles == 'Driver', User.zipcode >= passenger_zipcode)
s2 = User.query.filter(User.roles == 'Driver', User.zipcode <= passenger_zipcode)
drivers = s1.union(s2).order_by(User.zipcode.asc())
# drivers = db.engine.execute(text("SELECT users.id, name, (select avg(driver_ratings) from rides where driver_id = users.id) as avg_ratings FROM users where roles='Driver'"
#                                  " and (zipcode >= "+s_p_zipcode+" or zipcode <= "+s_p_zipcode+") order by avg_ratings DESC"))
closest_drivers = []
minimum = sys.maxsize  # Largest possible integer in Python

for d in drivers:  # Finds the shortest distance
    distance = abs(d.zipcode - passenger_zipcode)
    if distance < minimum:
        minimum = distance

for d in drivers:  # Get list of drivers who are at the shortest distance
    distance = abs(d.zipcode - passenger_zipcode)
    if distance == minimum:
        closest_drivers.append(d.id)

list = str(tuple(closest_drivers)).replace(',)', ')')
drivers = db.engine.execute(text("SELECT *, (select avg(driver_ratings) from rides where driver_id = users.id) as avg_ratings FROM users where id in %s order by avg_ratings DESC" %list))
# print(list)
# best_drivers = db.engine.execute(text(
#     "select *,users.id as d_id, avg(driver_ratings) as ratings from users join rides on rides.driver_id = users.id where users.id in %s "
#     " order by ratings DESC" % list))
# print(str(list))
# bds = best_drivers.fetchall()
# print(str(len(bds)))
# if len(bds) > 0:
#     print('best driver displayed: ')
#     for d, c in best_drivers, closest_drivers:
#         print(d.name +" | "+ str(d.d_id)+ " | "+str(d.ratings))
#         print(c.name +" | "+ str(c.id))
# else:
#     print('closest driver displayed: ')
for cd in drivers:
    print(cd.name+ " | "+str(cd.avg_ratings)+" | "+str(cd.id))


from sqlalchemy import text, func
# q = Query([Ride, User], session=session)
# rides =  session.query(Ride,User).filter(User.id == Ride.passenger_id).all()
# for r in rides:
#     pprint(vars(r.User))

# reviews = db.session.query(Ride).join(User, User.id == Ride.driver_id).all()
# reviews = db.engine.execute(text("SELECT * from rides LEFT JOIN users on users.id=rides.driver_id"))
# for r in reviews:
#     print(r.surname)
# pprint(rides[0])
#
#sqlalchemy getting drivers
# s1 = User.query.filter(User.roles=='Driver',User.zipcode >= passenger_zipcode)
# s2 = User.query.filter(User.roles=='Driver',User.zipcode <= passenger_zipcode)
# drivers = s1.union(s2).order_by(User.zipcode.asc())
#
# drivers.join(User, User.id == Ride.driver_id).all()
#
# drivers
# matched_drivers_zipcode = []
#
# #zipcodes of all the drivers will be added to a list
# #to find out the closest ones
#
# for s in s3:
#     matched_drivers_zipcode.append(s.zipcode)
#
#
# closest_drivers = []
# refined_second = []
#
# #through this function closest zipcode will be found and returned
# #which will be stored in the @closest_drivers list
# def takeClosest(num,collection):
#    return min(collection,key=lambda x:abs(x-num))
#
# for i in matched_drivers_zipcode:
#     closest = takeClosest(passenger_zipcode,matched_drivers_zipcode)
#     closest_drivers.append(closest)
#     matched_drivers_zipcode.remove(closest)
#
# for j in closest_drivers:
#     closest = takeClosest(passenger_zipcode,closest_drivers)
#     refined_second.append(closest)
#     closest_drivers.remove(closest)
#
# print(refined_second)
#
#
# print("Closest Drivers:")
# #now all the drivers matching the closest zipcodes will be fetched.
# drivers = User.query.filter(User.zipcode.in_(refined_second)).all()
# for d in drivers:
#     print(d.name + " | "+str(d.zipcode)+ " | "+d.roles)

# import sys
#
#
#
# # drivers = User.query.filter(User.roles=="Driver"); #All the drivers (error since no module Driver in my project)
#
# closest_drivers = []
# minimum= sys.maxsize #Largest possible integer in Python
#
# for d in drivers: #Finds the shortest distance
#     distance = abs(d.zipcode - passenger_zipcode)
#     if distance < minimum:
#         minimum = distance
#
#
# for d in drivers: #Get list of drivers who are at the shortest distance
#     distance = abs(d.zipcode - passenger_zipcode)
#     if distance == minimum:
#         closest_drivers.append(d)
#
#
# best_driver = None
# maximum = 0
#
# for d in closest_drivers: #Now I get the best diver, the one with the highest rating in the database
#     print(d.name+ " | zipcode: "+str(d.zipcode)+ " role: "+d.roles)
#     # if d.rating > maximum:
#     #     best_driver = d
#
# # print(closest_drivers)
