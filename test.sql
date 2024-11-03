Create table Customer (
Customer_ID VARCHAR(4) PRIMARY KEY,
Phone_No INT(10) NOT NULL,
Customer_Name VARCHAR(20) NOT NULL,
DL_Number VARCHAR(10) NOT NULL UNIQUE,
Pan_Card BOOLEAN NOT NULL,
Pan_Card_Number VARCHAR(10) UNIQUE,
City VARCHAR(10),
Street_Name VARCHAR(20),
Pincode INT(6) NOT NULL
);


Create table Dealership (
Dealership_ID VARCHAR(4) Primary Key,
Name VARCHAR(20) NOT NULL,
City VARCHAR(10),
Street_Name VARCHAR(20) NOT NULL,
Pincode INT(6) NOT NULL
);

Create table Car_Brand (
Brand_ID VARCHAR(4) PRIMARY KEY,
Name VARCHAR(20) NOT NULL,
Number_of_Vehicles INT(5) NOT NULL,
Dealership_ID VARCHAR(4),
FOREIGN KEY(Dealership_ID) REFERENCES Dealership(Dealership_ID)
);


Create table Car_Model (
Reg_No VARCHAR(10) NOT NULL PRIMARY KEY,
Engine_No VARCHAR(4) UNIQUE NOT NULL,
Chassis_No VARCHAR(4) UNIQUE NOT NULL,
Color VARCHAR(10), 
Name VARCHAR(20),
No_of_seats INT(1) CHECK (No_of_seats >= 2),
Price INT(5), 
Type VARCHAR(10),
Brand_ID VARCHAR(4),
foreign key (Brand_ID) references Car_Brand(Brand_ID)
);


Create table Insurance (
Insurance_ID INT(4) NOT NULL PRIMARY KEY,
Date_of_Allocation DATE,
Date_of_Expiry DATE,
Company VARCHAR(15)
); 


Create table Service (
Service_ID INT(4) NOT NULL PRIMARY KEY,
Last_service_Date DATE,
Next_service_Date DATE,
Last_service_cost INT(6),
Reg_No VARCHAR(10) NOT NULL,
foreign key(Reg_No) references Car_Model(Reg_No)
); 


Create table Delivery (
Delivery_ID INT(4) NOT NULL PRIMARY KEY,
Delivery_Date DATE,
Return_Date DATE,
Location VARCHAR(20),
POC CHAR(10)
); 


Create table Payment (
Transaction_ID INT(4) NOT NULL PRIMARY KEY,
Payment_Date DATE,
Payment_Status BOOLEAN,
Mode VARCHAR(8),
Discount FLOAT CHECK (Discount > 0.0 and Discount < 0.40) DEFAULT 0.0,
Tax FLOAT CHECK (Tax > 0.0)
); 


CREATE TABLE Penalty (
Transaction_ID INT(4),
Amount INT,
Reason VARCHAR(10) CHECK (Reason IN ('Late', 'Damage', 'IAE')),
PRIMARY KEY (Transaction_ID),
FOREIGN KEY (Transaction_ID) REFERENCES Payment(Transaction_ID)
);

Create table Booking (
Booking_ID VARCHAR(4) PRIMARY KEY,
Booking_Date Date,
Reg_No VARCHAR(10) NOT NULL,
Transaction_ID INT(4) NOT NULL,
Insurance_ID INT(4) NOT NULL,
Delivery_ID INT(4) NOT NULL,
foreign key(Reg_No) references Car_Model(Reg_No),
foreign key(Transaction_ID) references Payment(Transaction_ID),
foreign key(Insurance_ID) references Insurance(Insurance_ID),
foreign key(Delivery_ID) references Delivery(Delivery_ID)
);

Create table Connection (
Dealership_ID VARCHAR(4),
Customer_ID VARCHAR(4),
Booking_ID VARCHAR(4),
CONSTRAINT dfk FOREIGN KEY(Dealership_ID) REFERENCES Dealership(Dealership_ID),
CONSTRAINT cfk FOREIGN KEY(Customer_ID) REFERENCES Customer(Customer_ID),
CONSTRAINT bfk FOREIGN KEY(Booking_ID) REFERENCES Booking(Booking_ID),
PRIMARY KEY(Dealership_ID, Customer_ID, Booking_ID)
);



INSERT INTO car_brand VALUES 
("B1", "Porsche", 1, "D1"),
("B2", "Tata", 5, "D1"),
("B3", "Mahindra", 4, "D1"),
("B4", "Maruti Suzuki", 6, "D1"),
("B5", "Honda", 3, "D1"),
("B6", "Hyundai", 4, "D1"),
("B7", "Kia", 2, "D1"),
("B8", "Toyota", 5, "D1"),
("B9", "Ford", 2, "D1"),
("B10", "Renault", 3, "D1");

INSERT INTO car_model VALUES 
("KA02AB5555", "E448", "C900", "Green", "911 GT3RS", 2, 25000, "Sports Car", "B1"),
("KA01AB1234", "E123", "C123", "Red", "Tata Nexon", 5, 12000, "SUV", "B2"),
("KA02BC5678", "E124", "C124", "Blue", "Mahindra Scorpio", 7, 15000, "SUV", "B3"),
("KA03CD9012", "E125", "C125", "White", "Maruti Swift", 4, 8000, "Hatchback", "B4"),
("KA04DE3456", "E126", "C126", "Silver", "Honda City", 5, 11000, "Sedan", "B5"),
("KA05EF7890", "E127", "C127", "Black", "Hyundai Creta", 5, 14000, "SUV", "B6"),
("KA06FG1122", "E128", "C128", "Gray", "Kia Seltos", 5, 13000, "SUV", "B7"),
("KA07GH3344", "E129", "C129", "Green", "Toyota Fortuner", 7, 25000, "SUV", "B8"),
("KA08IJ5566", "E130", "C130", "Orange", "Ford EcoSport", 5, 13500, "SUV", "B9"),
("KA09KL7788", "E131", "C131", "Yellow", "Renault Duster", 5, 12000, "SUV", "B10"),
("KA10MN9900", "E132", "C132", "Red", "Tata Harrier", 5, 18000, "SUV", "B2"),
("KA11OP1123", "E133", "C133", "Blue", "Mahindra XUV500", 7, 16000, "SUV", "B3"),
("KA12QR4567", "E134", "C134", "White", "Maruti Baleno", 5, 10000, "Hatchback", "B4"),
("KA13ST8901", "E135", "C135", "Black", "Honda Amaze", 5, 9500, "Sedan", "B5"),
("KA14UV2345", "E136", "C136", "Silver", "Hyundai Verna", 5, 11500, "Sedan", "B6"),
("KA15WX6789", "E137", "C137", "Gray", "Kia Carnival", 7, 21000, "MPV", "B7"),
("KA16YZ1234", "E138", "C138", "Green", "Toyota Innova", 7, 23000, "MPV", "B8"),
("KA17AB5678", "E139", "C139", "Orange", "Ford Endeavour", 7, 27000, "SUV", "B9"),
("KA18CD9012", "E140", "C140", "Yellow", "Renault Kwid", 5, 8000, "Hatchback", "B10"),
("KA19EF3456", "E141", "C141", "Red", "Tata Tiago", 5, 8500, "Hatchback", "B2"),
("KA20GH7890", "E142", "C142", "Blue", "Mahindra Bolero", 7, 14000, "SUV", "B3"),
("KA21IJ1122", "E143", "C143", "White", "Maruti Ertiga", 7, 14500, "MPV", "B4"),
("KA22KL3344", "E144", "C144", "Silver", "Honda CR-V", 5, 22000, "SUV", "B5"),
("KA23MN5566", "E145", "C145", "Black", "Hyundai Tucson", 5, 19500, "SUV", "B6"),
("KA24OP7788", "E146", "C146", "Gray", "Kia Sonet", 5, 12500, "SUV", "B7"),
("KA25QR9900", "E147", "C147", "Green", "Toyota Camry", 5, 24000, "Sedan", "B8"),
("KA26ST1123", "E148", "C148", "Orange", "Ford Figo", 5, 8500, "Hatchback", "B9"),
("KA27UV4567", "E149", "C149", "Yellow", "Renault Triber", 7, 9500, "MPV", "B10"),
("KA28WX8901", "E150", "C150", "Red", "Tata Altroz", 5, 10500, "Hatchback", "B2"),
("KA29YZ2345", "E151", "C151", "Blue", "Mahindra Thar", 4, 18500, "SUV", "B3");

INSERT INTO car_model VALUES 
-- Tata Cars (B2)
("KA30AB1122", "E152", "C152", "Red", "Harrier", 5, 18000, "SUV", "B2"),
("KA31BC2233", "E153", "C153", "Blue", "Safari", 7, 19000, "SUV", "B2"),

-- Mahindra Cars (B3)
("KA32CD3344", "E154", "C154", "White", "KUV100", 5, 8500, "Hatchback", "B3"),
("KA33DE4455", "E155", "C155", "Black", "TUV300", 7, 16500, "SUV", "B3"),

-- Maruti Suzuki Cars (B4)
("KA34EF5566", "E156", "C156", "Gray", "Ciaz", 5, 11000, "Sedan", "B4"),
("KA35FG6677", "E157", "C157", "Silver", "S-Presso", 5, 7000, "Hatchback", "B4"),

-- Honda Cars (B5)
("KA36GH7788", "E158", "C158", "Green", "Jazz", 5, 9500, "Hatchback", "B5"),
("KA37IJ8899", "E159", "C159", "Orange", "WR-V", 5, 11500, "SUV", "B5"),

-- Hyundai Cars (B6)
("KA38KL9900", "E160", "C160", "Red", "Aura", 5, 10500, "Sedan", "B6"),
("KA39MN1011", "E161", "C161", "Blue", "Venue", 5, 12000, "SUV", "B6"),

-- Kia Cars (B7)
("KA40OP1122", "E162", "C162", "White", "Carnival", 7, 21000, "MPV", "B7"),
("KA41QR2233", "E163", "C163", "Black", "Rio", 5, 9000, "SUV", "B7"),

-- Toyota Cars (B8)
("KA42ST3344", "E164", "C164", "Silver", "Corolla", 5, 23000, "Sedan", "B8"),
("KA43UV4455", "E165", "C165", "Gray", "Yaris", 5, 24000, "Sedan", "B8"),

-- Ford Cars (B9)
("KA44WX5566", "E166", "C166", "Red", "Aspire", 5, 11500, "Sedan", "B9"),
("KA45YZ6677", "E167", "C167", "Green", "Freestyle", 5, 13000, "SUV", "B9"),

-- Renault Cars (B10)
("KA46AB7788", "E168", "C168", "Orange", "Lodgy", 7, 18000, "MPV", "B10"),
("KA47BC8899", "E169", "C169", "Blue", "Captur", 5, 12500, "SUV", "B10"),

-- Additional Tata Cars (B2)
("KA48CD9900", "E170", "C170", "White", "Tigor", 5, 9000, "Sedan", "B2"),
("KA49DE1011", "E171", "C171", "Gray", "Zest", 5, 9500, "Sedan", "B2"),

-- Additional Mahindra Cars (B3)
("KA50EF1122", "E172", "C172", "Silver", "Marazzo", 7, 17500, "MPV", "B3"),
("KA51FG2233", "E173", "C173", "Black", "XUV300", 5, 14000, "SUV", "B3");




-- Insert data into service table for each registration number
INSERT INTO service (Service_ID, Last_service_Date, Next_service_Date, Last_service_cost, Reg_No)
SELECT
    ROW_NUMBER() OVER (ORDER BY reg_no) AS Service_ID,  -- Unique service ID
    DATE_ADD('2024-11-05', INTERVAL -FLOOR(RAND() * 240) DAY) AS Last_service_Date,  -- Random date within the past 8 months to today
    DATE_ADD(DATE_ADD('2024-11-05', INTERVAL -FLOOR(RAND() * 240) DAY), INTERVAL 6 MONTH) AS Next_service_Date,  -- 6 months after Last_service_Date
    FLOOR(RAND() * 4000) + 1000 AS Last_service_cost,  -- Random cost between 1000 and 5000
    reg_no  -- Registration number
FROM car_model;


CREATE TRIGGER update_vehicle_count AFTER INSERT ON car_model FOR EACH ROW BEGIN UPDATE car_brand SET number_of_vehicles = number_of_vehicles + 1 WHERE brand_id = NEW.brand_id; END;


DELIMITER //

CREATE PROCEDURE UpdateCarPrice(
    IN p_registration_number VARCHAR(20),
    IN p_new_price INT,
)
BEGIN
    -- Declare variable to check if the car exists
    DECLARE car_exists INT;
    
    -- Check if the car exists
    SELECT COUNT(*) INTO car_exists
    FROM cars
    WHERE registration_number = p_registration_number;
    
    -- If car exists, update the price
    IF car_exists > 0 THEN
        UPDATE cars
        SET price = p_new_price
        WHERE registration_number = p_registration_number;
        
        SELECT 'Car price updated successfully' AS message;
    ELSE
        SELECT 'Car not found' AS message;
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateCarPrice(
    IN p_registration_number VARCHAR(20),
    IN p_new_price INT
)
BEGIN
    DECLARE car_exists INT;
    
    SELECT COUNT(*) INTO car_exists
    FROM car_model
    WHERE reg_no = p_registration_number;
    
    IF car_exists > 0 THEN
        UPDATE car_model
        SET price = p_new_price
        WHERE reg_no = p_registration_number;
    END IF;
END //

DELIMITER ;