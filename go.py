from app.models.models import *

passenger_zipcode = 100

#sqlalchemy getting drivers
s1 = User.query.filter(User.roles=='Driver',User.zipcode >= passenger_zipcode)
s2 = User.query.filter(User.roles=='Driver',User.zipcode <= passenger_zipcode)
s3 = s1.union(s2).order_by(User.zipcode.asc())


matched_drivers_zipcode = []

#zipcodes of all the drivers will be added to a list
#to find out the closest ones

for s in s3:
    matched_drivers_zipcode.append(s.zipcode)


closest_drivers = []
refined_second = []

#through this function closest zipcode will be found and returned
#which will be stored in the @closest_drivers list
def takeClosest(num,collection):
   return min(collection,key=lambda x:abs(x-num))

for i in matched_drivers_zipcode:
    closest = takeClosest(passenger_zipcode,matched_drivers_zipcode)
    closest_drivers.append(closest)
    matched_drivers_zipcode.remove(closest)

for j in closest_drivers:
    closest = takeClosest(passenger_zipcode,closest_drivers)
    refined_second.append(closest)
    closest_drivers.remove(closest)

print(refined_second)


print("Closest Drivers:")
#now all the drivers matching the closest zipcodes will be fetched.
drivers = User.query.filter(User.zipcode.in_(refined_second)).all()
for d in drivers:
    print(d.name + " | "+str(d.zipcode)+ " | "+d.roles)


