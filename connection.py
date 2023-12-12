import mysql.connector
mydb = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'system123',
        database = 'project')

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE cities 
                     (
                         cityId int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                         name VARCHAR(255) NOT NULL
                      )
                 """)
mycursor.execute("""CREATE TABLE theatres 
                     (
                         theatreId int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                         cityId int NOT NULL, 
                         name VARCHAR(255) NOT NULL,
                         location VARCHAR(255) NOT NULL,
                         rate DECIMAL NOT NULL
                     )
                 """)
mycursor.execute("""CREATE TABLE movies 
                     (
                         movieId int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                         theatreId int NOT NULL, 
                         start_date date NOT NULL, 
                         end_date date NOT NULL,
                         name VARCHAR(255) NOT NULL
                     )
                 """)
mycursor.execute("""CREATE TABLE time 
                         (
                             timeId int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                             theatreId int NOT NULL, 
                             movieId int NOT NULL, 
                             start_slot datetime NOT NULL,
                             end_slot datetime NOT NULL
                         )
                 """)
mycursor.execute("""CREATE TABLE seats 
                     (
                         theatreId int NOT NULL, 
                         movieId int NOT NULL, 
                         timeId int NOT NULL, 
                         seatNumber varchar(255) NOT NULL
                     )
                 """)
mycursor.execute("""CREATE TABLE bookings 
                     (
                         bookingId int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                         name varchar(255) NOT NULL, 
                         email varchar(255) NOT NULL, 
                         phone varchar(10) NOT NULL, 
                         theatre varchar(255) NOT NULL, 
                         city varchar(255) NOT NULL, 
                         movie varchar(255) NOT NULL, 
                         seat varchar(255) NOT NULL, 
                         time datetime NOT NULL,
                         rate decimal NOT NULL
                     )
                 """)
mycursor.execute("""CREATE TABLE meals 
                     (
                         orderId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                         bookingId int NOT NULL,
                         popcorn_large int NOT NULL, 
                         popcorn_medium int NOT NULL,
                         popcorn_small int NOT NULL,
                         coke_large int NOT NULL,
                         coke_medium int NOT NULL,
                         coke_small int NOT NULL,
                         combo int NOT NULL
                     )
                 """)
mycursor.execute("""ALTER TABLE theatres ADD CONSTRAINT FK_Theatres_Cities FOREIGN KEY(cityId)
REFERENCES cities(cityId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE movies ADD CONSTRAINT FK_Movies_Theatres FOREIGN KEY(theatreId)
REFERENCES theatres(theatreId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE time ADD CONSTRAINT FK_Time_Theatres FOREIGN KEY(theatreId)
REFERENCES theatres(theatreId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE time ADD CONSTRAINT FK_Time_Movies FOREIGN KEY(movieId)
REFERENCES movies(movieId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE seats ADD CONSTRAINT FK_Seats_Theatres FOREIGN KEY(theatreId)
REFERENCES theatres(theatreId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE seats ADD CONSTRAINT FK_Seats_Movies FOREIGN KEY(movieId)
REFERENCES movies(movieId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE seats ADD CONSTRAINT FK_Seats_Time FOREIGN KEY(timeId)
REFERENCES time(timeId)
ON DELETE CASCADE""")
mycursor.execute("""ALTER TABLE meals ADD CONSTRAINT FK_Meals_Bookings FOREIGN KEY(bookingId)
REFERENCES bookings(bookingId)
ON DELETE CASCADE""")
sql = "INSERT INTO bookings (name, email, phone, city, theatre, movie, time, seat, rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.execute(sql, ("", "", 0, "", "", "",  "2021-09-21 12:45:46", "", 0))
mydb.commit()
sql = "INSERT INTO meals (bookingId, popcorn_large, popcorn_medium, popcorn_small, coke_large, coke_medium, coke_small, combo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.execute(sql, (1, 350, 330, 300, 120, 100, 80, 400))
mydb.commit()
