BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "rides" (
	"id"	INTEGER NOT NULL,
	"driver_id"	INTEGER,
	"passenger_id"	INTEGER,
	"zipcode"	INTEGER(11) NOT NULL,
	"from_loc"	VARCHAR(150) NOT NULL,
	"to_loc"	VARCHAR(150) NOT NULL,
	"isStarted"	INTEGER,
	"isEnded"	INTEGER,
	"isPaid"	INTEGER,
	"isConfirmed"	INTEGER,
	"passenger_ratings"	INTEGER,
	"driver_ratings"	INTEGER,
	"distance"	INTEGER NOT NULL,
	"driver_review_for_passenger"	VARCHAR(255),
	"passenger_review_for_driver"	VARCHAR(255),
	"price"	INTEGER NOT NULL,
	"ride_date"	DATETIME NOT NULL,
	FOREIGN KEY("passenger_id") REFERENCES "users"("id"),
	FOREIGN KEY("driver_id") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"surname"	VARCHAR(100) NOT NULL,
	"email"	VARCHAR(100) NOT NULL UNIQUE,
	"password"	VARCHAR(150) NOT NULL,
	"zipcode"	INTEGER(11),
	"roles"	VARCHAR(10),
	"profile_image"	VARCHAR(255),
	"profile_description"	VARCHAR(255),
	"gender"	INTEGER NOT NULL,
	"member_since"	DATETIME NOT NULL,
	"charges_per_kilo"	INTEGER,
	PRIMARY KEY("id")
);
INSERT INTO "rides" ("id","driver_id","passenger_id","zipcode","from_loc","to_loc","isStarted","isEnded","isPaid","isConfirmed","passenger_ratings","driver_ratings","distance","driver_review_for_passenger","passenger_review_for_driver","price","ride_date") VALUES (1,1,3,'0','x','s',1,1,1,1,NULL,4,14,NULL,'greate, driving experience with ....',280,'2020-04-15 09:54:06.086396');
INSERT INTO "users" ("id","name","surname","email","password","zipcode","roles","profile_image","profile_description","gender","member_since","charges_per_kilo") VALUES (1,'Driver','one','d@d.com','pbkdf2:sha256:150000$R2oTdQEE$f5f5cea8ee36dcab901248558e65a02484c3ebafd91232faadb217a998448a3b','4321','Driver','0',NULL,1,'2020-04-15 07:48:43.227485',0);
INSERT INTO "users" ("id","name","surname","email","password","zipcode","roles","profile_image","profile_description","gender","member_since","charges_per_kilo") VALUES (2,'Passenger','one','p@p.com','pbkdf2:sha256:150000$eHAXkb6e$7c64881cf081b43da03006f454b24aa0e5e1348ab2cc3487d1b40e63a5b122a4','0','Driver','0',NULL,1,'2020-04-15 07:54:07.929207',0);
INSERT INTO "users" ("id","name","surname","email","password","zipcode","roles","profile_image","profile_description","gender","member_since","charges_per_kilo") VALUES (3,'Passenger','one','pp@p.com','pbkdf2:sha256:150000$l2nISPJQ$cd9f8485389744405967b3e1aa17ff2c623ce5394b9b6aa4a82438f2c601b6db','1234','Passenger','1.png','hello this is passsenger one profile description....',1,'2020-04-15 07:55:14.421361',0);
COMMIT;
