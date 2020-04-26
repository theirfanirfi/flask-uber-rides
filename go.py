from app import db, application, session
from app.models.models import *
from pprint import pprint
passenger_zipcode = 100
from sqlalchemy import text, func
# q = Query([Ride, User], session=session)
rides =  session.query(Ride,User).filter(User.id == Ride.passenger_id).all()
for r in rides:
    pprint(vars(r.User))

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
