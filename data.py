import mysql.connector
from mysql.connector import Error
import os

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get('password'),
        database="crdms")
    print("Connected to the database")
except Error as e:
    print("Error while connecting to MySQL", e)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM car_brand")



myresult = mycursor.fetchall()

for brand in myresult:
    if brand[1] != 'Porsche' and brand[1] != 'Tata' and brand[1] != 'Mahindra':
        mycursor.execute("UPDATE car_brand SET number_of_vehicles = number_of_vehicles + 2 WHERE name = %s", (brand[1],))
    elif brand[1] == 'Tata' or brand[1] == 'Mahindra':
        mycursor.execute("UPDATE car_brand SET number_of_vehicles = number_of_vehicles + 4 WHERE name = %s", (brand[1],))

mydb.commit()




"CREATE TRIGGER update_vehicle_count AFTER INSERT ON car_model FOR EACH ROW BEGIN UPDATE car_brand SET number_of_vehicles = number_of_vehicles + 1 WHERE brand_id = NEW.brand_id; END;")

