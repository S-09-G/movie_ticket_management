## database connections
import mysql.connector
mydb = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'system123',
        database = 'project')

mycursor = mydb.cursor()

import getpass
import datetime

def check_date_valid(date):
    day, month, year = date.split('/')
    isValidDate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False
        print("Invalid date")
    return isValidDate

def fetch_cities_from_db(query):
    mycursor.execute(query)
    cities = mycursor.fetchall()
    for city in cities:
        print(str(city[0]) + ". " + city[1])
    return cities

def fetch_theatres_from_db(query):
    mycursor.execute(query)
    theatres = mycursor.fetchall()
    for theatre in theatres:
        print(str(theatre[0]) + ". " + theatre[1] + ", " + theatre[2] + " ( Price : ₹" + str(theatre[3]) + " )")
    return theatres

def input_theatres():
    theatres = []
    theatre = input("Enter new theatre name (Press 'n' to exit): ")
    while theatre is not 'N' and theatre is not 'n':
        location = input("Enter location : ")
        rate = input("Enter price : ")
        val = (theatre, location, rate) 
        theatres.append(val)
        theatre = input("Enter new theatre name (Press 'n' to exit): ")
    return theatres

def insert_theatres(index):
    theatres = input_theatres()
    for theatre in theatres :
        sql = "INSERT INTO theatres (cityId, name, location, rate) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (index, theatre[0],theatre[1], theatre[2]))
    mydb.commit()
    if len(theatres) != 0:
        print("Theatre(s) inserted.")

def delete_theatres_from_db(index):
    sql = "DELETE FROM theatres WHERE theatreId = " + str(index)
    mycursor.execute(sql)
    mydb.commit()
    print("Theatre(s) deleted")

def fetch_prices_from_db(theatreId):
    mycursor.execute("SELECT rate from theatres WHERE theatreId = " + str(theatreId))
    theatres = mycursor.fetchall()
    for theatre in theatres:
        print("Current price : " + str(theatre[0]))
    return theatres

def get_date_for_movie():
    ##Check validity of date
    is_valid_date = False
    while is_valid_date is False:
        start_date = input("Enter start date in dd/mm/yyyy: ")
        is_valid_date = check_date_valid(start_date)
    day,month,year = start_date.split("/")
    start_date = datetime.date(int(year), int(month), int(day))
    is_valid_date = False

    while is_valid_date is False:
        end_date = input("Enter end date in dd/mm/yyyy: ")
        is_valid_date = check_date_valid(end_date)
    day,month,year = end_date.split("/")
    end_date = datetime.date(int(year), int(month), int(day))
    return start_date, end_date

def fetch_movies_from_db(query):
    mycursor.execute(query)
    movies = mycursor.fetchall()
    for movie in movies:
        print(str(movie[0]) + ". " + movie[1])
    return movies

def input_movies():
    movies = []
    movie = input("Enter new movie name (Press 'n' to exit): ")
    while movie is not 'N' and movie is not 'n':
        start_date, end_date = get_date_for_movie()
        val = (movie, start_date, end_date)
        movies.append(val)
        movie = input("Enter new movie name (Press 'n' to exit): ")
    return movies
        
def insert_movies(index):
    movies = input_movies()
    for movie in movies :
        sql = "INSERT INTO movies (theatreId, name, start_date, end_date) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (index, movie[0],movie[1], movie[2]))
    mydb.commit()
    if len(movies) != 0:
        print("Movie(s) inserted.")
            
def delete_movies_from_db(index):
    sql = "DELETE FROM movies WHERE movieId = " + str(index)
    mycursor.execute(sql)
    mydb.commit()
    print("Movie(s) deleted")

def fetch_date_from_db(movieId):
    now = datetime.date.today() + datetime.timedelta(days=1)
    next7 = datetime.date.today() + datetime.timedelta(days=7)
    mycursor.execute("SELECT start_date, end_date FROM movies WHERE movieId = " + str(movieId) + 
    " and (start_date <= %s and end_date >= %s) or (start_date <= %s and end_date >= start_date)", (now, now, next7))
    dates = mycursor.fetchall()
    return dates, now, next7
        
def fetch_time_slots_from_db(query):
    mycursor.execute(query)
    time_slots = mycursor.fetchall()
    for time_slot in time_slots:
        print(str(time_slot[0]) + ". " + str(time_slot[1].time()))
    return time_slots

def input_time_slots(movieId):
    sql = "SELECT start_date, end_date FROM movies WHERE movieId = " + str(movieId)
    mycursor.execute(sql)
    date = mycursor.fetchone()
    time_slots = []
    time_slot = input("Enter new time slot (hh:mm) (Press 'n' to exit): ")
    while time_slot is not 'N' and time_slot is not 'n':
        time_slot = datetime.datetime.strptime(time_slot, '%H:%M').time()
        start_slot = datetime.datetime.combine(date[0],time_slot)
        end_slot = datetime.datetime.combine(date[1],time_slot)
        time_slots.append((start_slot, end_slot))
        time_slot = input("Enter new time slot (hh:mm) (Press 'n' to exit): ")
    return time_slots

def insert_time_slots(theatreId, movieId):
    time_slots = input_time_slots(movieId)
    for time in time_slots:
        sql = "INSERT INTO time (theatreId, movieId, start_slot, end_slot ) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (theatreId, movieId, time[0], time[1]))
    mydb.commit()
    if len(time_slots) != 0:
        print("Time slot(s) inserted.")

def delete_time_slots_from_db(index):
    sql = "DELETE FROM time WHERE timeId = " + str(index)
    mycursor.execute(sql)
    mydb.commit()
    print("Time slot(s) deleted")

def fetch_seats_from_db(theatreId, movieId, timeId): 
    query = "SELECT seatNumber, timeId from seats WHERE theatreId = " + str(theatreId) + " and movieId = " + str(movieId) + " and timeId = " + str(timeId)
    mycursor.execute(query)
    seats = dict(mycursor.fetchall())
    return seats

def insert_seat(theatreId, movieId, timeId, seat):
    sql = "INSERT INTO seats (theatreId, movieId, timeId, seatNumber) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (theatreId, movieId, timeId, seat))
    mydb.commit()

def insert_meals(meals):
    mycursor.execute("SELECT bookingId from bookings")
    ids = mycursor.fetchall()
    sql = "INSERT INTO meals (bookingId, popcorn_large, popcorn_medium, popcorn_small, coke_large, coke_medium, coke_small, combo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (ids[len(ids)-1][0], meals[1], meals[2], meals[3], meals[4], meals[5], meals[6], meals[7]))
    mydb.commit()

def print_seat_matrix(seats):
    print()
    for i in range(26):
        print("*", end = "")
    print(" Select seat ", end = "")
    for i in range(25):
        print("*", end = "")
    print()
    
    for i in range(0, 10, 1):
        for j in range(1, 16, 1):
            seat = chr(65+i) + str(j)
            if seat in seats :
                if len(seat) == 2:
                    print("o  ", end = " ")
                else:
                    print(" o  ", end = " ")
            else:
                print(seat + " ", end = " ")
        print()
    
def get_theatres_dict(index):
    theatres = fetch_theatres_from_db("SELECT theatreId, name, location, rate FROM theatres WHERE cityId = " + str(index))
    theatres_dict = {}
    for theatre in theatres:
        theatres_dict[theatre[0]] = theatre[1:]
    return theatres_dict
    
def add_city():
    cities = []
    city = input("Enter new city name (Press 'n' to exit): ")
    while city is not 'N' and city is not 'n':
        cities.append(city)
        city = input("Enter new city name (Press 'n' to exit): ")
    for city in cities :
        sql = "INSERT INTO cities (name) VALUES (%s)"
        mycursor.execute(sql, (city,))
    mydb.commit()
    if len(cities) != 0:
        print("Cities inserted.")
    
def remove_city():
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0 :
        index = int(input("Enter city id to be removed : "))
        is_present = index in cities
        if is_present : 
            sql = "DELETE FROM cities WHERE cityId = " + str(index)
            mycursor.execute(sql)
            mydb.commit()
            print("City deleted")
        else:
            print("Invalid City Id")
    else:
        print("No cities found")
                
def add_theatre():
    ##Get all cities from DB
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        ##check if id is a valid choice
        index = int(input("Enter city id in which new theatre(s) is to be added : "))
        is_present = index in cities
        if is_present:
            insert_theatres(index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")
        
def remove_theatre():
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        index = int(input("Enter city id in which theatre is to be removed : "))
        is_present = index in cities
        if is_present : 
            check_if_theatre_present("22", index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")
        
def add_movie():
    print("Enter following details to add new movie : ")
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        index = int(input("Enter city id in which new movie(s) is to be added : "))
        is_present = index in cities
        if is_present : 
            check_if_theatre_present("31", index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")
            
        
def remove_movie():
    print("Enter following details to remove movie : ")
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        index = int(input("Enter city id in which movie is to be removed : "))
        is_present = index in cities
        if is_present : 
            check_if_theatre_present("32", index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")

def add_time_slots():
    print("Enter following details to add new time slot : ")
    ##Get all cities from DB
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        index = int(input("City Id : "))
        is_present = index in cities
        if is_present : 
            check_if_theatre_present("41", index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")
        
def remove_time_slots():
    print("Enter following details to remove time slot : ")
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        index = int(input("City Id : "))
        is_present = index in cities
        if is_present : 
            check_if_theatre_present("42", index)
        else:
            print("Invalid City Id")
    else:
        print("No cities found")

def check_if_theatre_present(option, index):
    theatres = get_theatres_dict(index)
    if len(theatres) != 0:
        theatreId = int(input("Theatre Id : "))
        is_present = theatreId in theatres
        if is_present : 
            if option is "31":
                insert_movies(index)
            elif option is "22":
                delete_theatres_from_db(index)
            else:
                check_if_movie_present(theatreId,option)
        else:
            print("Invalid theatre Id")
    else:
        print("No theatres found")
                
def check_if_movie_present(theatreId, option):
    movies = dict(fetch_movies_from_db("SELECT movieId, name FROM movies WHERE theatreId = " + str(theatreId)))
    if len(movies) != 0:
        movieId = int(input("Movie Id : "))
        is_present = movieId in movies
        if is_present : 
            if option is "41":
                insert_time_slots(theatreId, movieId)
            elif option is "32":
                delete_movies_from_db(movieId)
            else:
                check_if_time_slot_present(theatreId, movieId, option)
        else :
           print("Invalid movie Id") 
    else:
        print("No movies found")

def check_if_time_slot_present(theatreId, movieId, option):
    time_slots = dict(fetch_time_slots_from_db("SELECT timeId, start_slot from time WHERE theatreId = " + str(theatreId) + " and movieId = " + str(movieId)))
    if len(time_slots) != 0:
        timeId = int(input("Time Id : "))
        is_present = timeId in time_slots
        if is_present :
            delete_time_slots_from_db(timeId)   
        else:
            print("Invalid time Id")
    else:
        print("No time slots found")
    
def admin_add(option):
        if option == 1:
                add_city()
        elif option == 2:
                add_theatre()
        elif option == 3:
                add_movie()
        elif option == 4:
                add_time_slots()
                        
def admin_remove(option):
        if option == 1:
                remove_city()
        elif option == 2:
                remove_theatre()
        elif option == 3:
            remove_movie()
        elif option == 4:
            remove_time_slots()

def edit_price():
    cities = dict(fetch_cities_from_db("SELECT * FROM cities"))
    if len(cities) != 0:
        cityId = int(input("Enter city id where theatre is located : "))
        is_present = cityId in cities
        if is_present : 
            theatres = get_theatres_dict(cityId)
            if len(theatres) != 0:
                theatreId = int(input("Enter theatre id for which price is to be changed : "))
                is_present = theatreId in theatres
                if is_present : 
                    fetch_prices_from_db(theatreId)
                    price = input("Enter new price : ")
                    mycursor.execute("UPDATE theatres SET rate = " + price + " WHERE theatreId = " + str(theatreId))
                    mydb.commit()
                    print("Record updated")
                else:
                    print("Invalid Theatre Id")
            else:
                print("No theatres found")
        else:
            print("Invalid City Id")
    else:
        print("No cities found")

def print_confirmation(query):
    mycursor.execute(query)
    records = mycursor.fetchall()
    if len(records) != 0:
        booking = records[len(records) - 1]

        print()
        for i in range(26):
            print("*", end = "")
        print(" BOOKING CONFIRMATION ", end = "")
        for i in range(25):
            print("*", end = "")
        print("\n")

        print("     Booking Id.    : " + str(booking[0]))
        print("     Name           : " + booking[1])
        print("     Mobile Number  : +91 " + booking[2])
        print("     E-mail address : " + booking[3])
        print("     City           : " + booking[4])
        print("     Theatre        : " + booking[5])
        print("     Movie          : " + booking[6])
        print("     Time           : " + str(booking[7]))
        print("     Seat           : " + booking[8])
        print("     Price          : ₹" + str(booking[9]))
        print()
        for i in range(26):
            print("*", end = "")
        print(" Booking.com ", end = "")
        for i in range(34):
            print("*", end = "")
    else:
        print("Invalid Booking Id")
        
def booking_confirm(cityId, theatreId, movieId, timeId, date, seat, meal_rate):
    print("\nPlease enter your details : ")
    name = input("Name : ")
    email = input("E-mail address : ")
    isValid = "@" in email and email[0].isalpha() and (".com" in email or ".co.in" in email)
    while isValid is not True:
        email = input("Please enter a valid E-mail address : ")
        isValid = "@" in email and email[0].isalpha() and (".com" in email or ".co.in" in email)
    phone = input("Mobile Number : ")
    isValid = len(phone) == 10 and phone.isdigit() and phone[0] is not "0"
    while isValid is not True:
        phone = input("Please enter a valid Mobile Number : ")
        isValid = len(phone) == 10 and phone.isdigit() and phone[0] is not "0"
    mycursor.execute("SELECT name FROM cities WHERE cityId = " + str(cityId))
    city = mycursor.fetchone()[0]
    mycursor.execute("SELECT name, rate FROM theatres WHERE theatreId = " + str(theatreId))
    res = mycursor.fetchone()
    theatre = res[0]
    rate = res[1]
    mycursor.execute("SELECT name FROM movies WHERE movieId = " + str(movieId))
    movie = mycursor.fetchone()[0]
    mycursor.execute("SELECT start_slot FROM time WHERE timeId = " + str(timeId))
    t = mycursor.fetchone()[0]
    time = datetime.datetime.combine(date, t.time())
    sql = "INSERT INTO bookings (name, email, phone, city, theatre, movie, time, seat, rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (name, email, phone, city, theatre, movie, time, seat, rate + meal_rate))
    mydb.commit()
    print_confirmation("SELECT bookingId, name, phone, email, city, theatre, movie, time, seat, rate FROM bookings")

def refreshment(cityId, theatreId, movieId, timeId, date, seat):
    ch = input(("Do you want to add a meal? (Enter 'y' or 'n')"))
    mycursor.execute("SELECT * FROM meals WHERE orderId = 1 and bookingId = 1")
    rates = mycursor.fetchone()
    meal_rate = 0 
    if ch == 'Y' or ch == 'y':
        print("1. Popcorn (L) - ₹" + str(rates[2]) +"\n2. Popcorn(M) - ₹"+ str(rates[3]) +"\n3. Popcorn(S) - ₹"+ str(rates[4]) +"\n4. Coke(L) - ₹" + str(rates[5]) + "\n5. Coke(M) - ₹" + str(rates[6]) + "\n6. Coke(S) - ₹" + str(rates[7]) + "\n7. Combo - ₹" + str(rates[8]))
        more = 'y'
        meals = dict.fromkeys(range(8),0) #initialise dict with 0 value with numbers as keys
        while more is 'y' or more is 'Y' :
            choice = int(input("Enter choice : "))
            if choice in range(1,8,1):
                num = int(input("Enter quantity : "))
                if num > 0 :
                    meals[choice] = meals[choice] + num
                else:
                    print("Not added")
            else:
                print("Invalid choice")
            more = input("Want to add anything else?(Enter 'y' or 'n')")
        for i in range(1, 8, 1):
            meal_rate = meal_rate + (meals[i]*rates[i+1])
        print("Your extra charge for meal is ₹: " + str(meal_rate))
        insert_meals(meals)
    booking_confirm(cityId, theatreId, movieId, timeId, date, seat, meal_rate)
    
    
def seat(cityId, theatreId, movieId, timeId, date):
    seats = dict(fetch_seats_from_db(theatreId, movieId, timeId))
    print_seat_matrix(seats)
    seat = input("\n\nEnter choice (Enter 0 to go Back): ")
    while seat in seats:  #Already booked
        print("Already booked. Please choose another one")
        seat = input("\n\nEnter choice (Enter 0 to go Back): ")
    if len(seat) == 2:
        if (seat[0] >= 'A' and seat[0] <= 'J') and (int(seat[1]) >= 1 and int(seat[1]) <= 9):
            insert_seat(theatreId, movieId, timeId, seat) 
            refreshment(cityId, theatreId, movieId, timeId, date, seat)
        else:
            print("Invalid choice")
    elif len(seat) == 3:
        if (seat[0] >= 'A' and seat[0] <= 'J') and (int(seat[1]) == 1) and (int(seat[2]) >= 0 and int(seat[1]) <= 5):
            insert_seat(theatreId, movieId, timeId, seat) 
            refreshment(cityId, theatreId, movieId, timeId, date, seat)
        else:
            print("Invalid choice")
    elif seat is 0 :
        time_slot(cityId, theatreId, movieId)
    else:
        print("Invalid choice")
        
def time_slot(cityId, theatreId, movieId, date):
    print("\n********** Select time **********")
    time_slots = dict(fetch_time_slots_from_db("SELECT timeId, start_slot FROM time WHERE theatreId = " + str(theatreId) + " and movieId = " + str(movieId)))
    print("0. Back")
    timeId = int(input("Enter choice : "))
    if timeId in time_slots:
        seat(cityId, theatreId, movieId, timeId, date)
    elif timeId == 0:
        date(cityId, theatreId, movieId)
    else:
        print("Invalid choice")
        
def date(cityId, theatreId, movieId):
    print("\n********** Select date **********")
    dates, now, next7 = fetch_date_from_db(movieId)
    start_date = now if dates[0][0] < now else dates[0][0]
    end_date = dates[0][1] if dates[0][1] < next7 else next7
    dates = {}
    for i in range(0,(end_date-start_date).days + 1,1):
        date = start_date + datetime.timedelta(days=i)
        dates[i+1] = date
    for key, value in dates.items():
        print(str(key) + ". " + str(value))
    print("0. Back")
    dateId = int(input("Enter choice : "))
    if dateId in dates:
        time_slot(cityId, theatreId, movieId, dates[dateId])
    elif dateId == 0:
        movie(cityId, theatreId)
    else:
        print("Invalid choice")
        
def movie(cityId, theatreId):
    print("\n********** Select movie **********")
    movies = dict(fetch_movies_from_db("SELECT movieId, name FROM movies WHERE theatreId = " + str(theatreId)))
    print("0. Back")
    movieId = int(input("Enter choice : "))
    if movieId in movies:
        date(cityId, theatreId, movieId)
    elif movieId == 0:
        theatre(cityId)
    else:
        print("Invalid choice")
                
def theatre(cityId):
    print("\n********** Select theatre **********")
    theatres = get_theatres_dict(cityId)
    print("0. Back")
    theatreId = int(input("Enter choice : "))
    if theatreId in theatres:
        movie(cityId, theatreId)
    elif theatreId == 0:
        city()
    else:
        print("Invalid choice")
        
def city():
    print("\n********** Select your city **********")
    cities = dict(fetch_cities_from_db("SELECT cityId, name from cities"))
    print("0. Exit")
    cityId = int(input("Enter choice : "))
    if cityId in cities:
        theatre(cityId)
    elif cityId == 0:
        print("Thank you for visiting Booking.com!")
    else:
      print("Invalid choice")
    
def cancel_booking(booking_id):
    mycursor.execute("SELECT bookingId, phone FROM bookings")
    ids = dict(mycursor.fetchall())
    if booking_id != 1 and booking_id in ids :
        phone = input("Enter registered mobile number : ")
        if phone == ids[booking_id]:
            mycursor.execute("DELETE FROM bookings WHERE bookingId = " + str(booking_id))
            mydb.commit()
            print("Booking has been cancelled")
        else:
            print("Oops..No records matched")
    else:
        print("Invalid booking Id")
                    
def admin_menu():
        print("\nSelect an option\n1. Edit city\n2. Edit theatre\n3. Edit movie\n4. Edit time\n5. Back")
        choice = int(input("Enter choice : "))
        if choice in range(1,5,1):
                if choice == 2:
                    print("\nSelect an option\n1. Add\n2. Remove\n3. Change price\n")
                else:
                    print("\nSelect an option\n1. Add\n2. Remove\n")
                option = int(input("Enter choice : "))
                if option == 1:
                        admin_add(choice)
                        admin_menu()
                elif option == 2:
                        admin_remove(choice)
                        admin_menu()
                elif choice == 2 and option == 3:
                        edit_price()
                        admin_menu()
                else:
                        print("Invalid choice")
        elif choice == 5:
                main_menu()
        else:
                print("Invalid choice")
                
def main_menu():
        choice = 0
        while choice != 5:
            print("\nSelect an option\n1. Admin\n2. New Booking\n3. Print booking confirmation\n4. Cancel Booking\n5. Exit")
            try : #check that only numbers are entered
                choice = int(input("Enter choice : "))
                if choice == 1:
                    print("Enter password : ")
                    password = getpass.getpass()
                    if(password == "admin"):
                            admin_menu()
                    else:
                            print("Incorrect password")
                elif choice == 2:
                    city()
                elif choice == 3:
                    booking_id = input("Enter Booking Id : ")
                    print_confirmation("SELECT bookingId, name, phone, email, city, theatre, movie, time, seat, rate FROM bookings WHERE bookingId = " + booking_id)
                elif choice == 4:
                    booking_id = int(input("Enter Booking Id : "))
                    cancel_booking(booking_id)
                elif choice == 5:
                    print("Exiting application...")
                else:
                    print("Please enter a valid choice") 
            except ValueError:
                print("Please enter a valid number")
                
print("\n***** Welcome to Booking.com : Movie Tickets Booking Platform *****")
main_menu()
