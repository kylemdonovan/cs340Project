/*
    OSU CS340 Intro to Databases (Spring 2023)
    Project Step 4 Draft
    Sample Data

    Team 52, 
    Ryu  an Kyle
    2023-05-025

*/

-- disable commits
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- -----------------------------------------------------
-- Table `Regions`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Regions (
  region_id INT NOT NULL AUTO_INCREMENT UNIQUE,
  region_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (`region_id`))
ENGINE = InnoDB;

Insert into Regions (region_name)
Values 
('central America'),
('United States'),
('Western Europe');

-- -----------------------------------------------------
-- Table `Clients`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Clients (
  client_id INT NOT NULL AUTO_INCREMENT UNIQUE,
  region_id INT NOT NULL,
  name VARCHAR(45) NOT NULL,
  address VARCHAR(145) NOT NULL,
  phone VARCHAR(45) NOT NULL,
  email VARCHAR(145) NULL,
  PRIMARY KEY (client_id),
  INDEX `fk_client_Region1_idx` (`region_id` ASC) VISIBLE,
  CONSTRAINT `fk_client_Region1`
    FOREIGN KEY (`region_id`)
    REFERENCES `Regions` (`region_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
    
-- select * from Clients;

Insert into Clients (region_id, name, address, phone, email)
values 
(2,'Ryus kitchen', '10000 Jollyville Rd Austin, TX 78759', '8044932999', 'ryukitchen@gmail.com'
),
(2, 'Kyles sandwich shop', '3939 Parmer Lane Bend, Oregon 19394', '7573214342', 'KyleSandwich@gmail.com'),
(1,'#1 Tacos', '4939 45th Street, Mexico city, Mexico ', '9499993929', 'Num1Tacos@gmail.com'),
( 3, 'Fish n chips', '3991 6th street, Britain, England', '3993292945', 'fishnchips@gmail.com');

-- -----------------------------------------------------
-- Table `Sales_history`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE  Sales_history (
  sales_history_id INT NOT NULL AUTO_INCREMENT UNIQUE,
  client_id INT NOT NULL,
  date DATE NOT NULL,
  total_cost DECIMAL(20,2) NOT NULL,
  refund DECIMAL(20,2) NULL,
  PRIMARY KEY (sales_history_id),
  INDEX `fk_sales_history_client1_idx` (client_id ASC) VISIBLE,
  CONSTRAINT `fk_sales_history_client1`
    FOREIGN KEY (client_id)
    REFERENCES Clients (client_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

Insert into Sales_history (client_id, date, total_cost, refund)
Values
(1, '2022-12-20', 2044.64, null),
(3, '2022-12-19', 266666.66, null),
(3, '2022-12-17', 23256.56, 23256.56);
-- -----------------------------------------------------
-- Table `Foods`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Foods (
  food_id INT NOT NULL AUTO_INCREMENT UNIQUE,
  region_id INT,
  food_name VARCHAR(145) NOT NULL,
  price DECIMAL(11,2) NOT NULL,
  PRIMARY KEY (food_id),
  INDEX `fk_Foods_Regions1_idx` (region_id ASC) VISIBLE,
  CONSTRAINT `fk_Foods_Regions1`
    FOREIGN KEY (region_id)
    REFERENCES `Regions` (region_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

Insert into Foods (region_id, food_name, price)
Values
(2, "corn", 1.29),
(2, "ribeye", 19.99),
(1, "beans", 1.09);
-- -----------------------------------------------------
-- Table `Sales_history_has_food`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE  Sales_history_has_food (
  sales_history_id INT NOT NULL,
  food_id INT NOT NULL,
  count INT NOT NULL,
  PRIMARY KEY (`sales_history_id`, `food_id`),
  INDEX `fk_sales_history_has_food_food1_idx` (`food_id` ASC) VISIBLE,
  INDEX `fk_sales_history_has_food_sales_history1_idx` (`sales_history_id` ASC) VISIBLE,
  CONSTRAINT `fk_sales_history_has_food_sales_history1`
    FOREIGN KEY (sales_history_id)
    REFERENCES Sales_history (sales_history_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sales_history_has_food_food1`
    FOREIGN KEY (food_id)
    REFERENCES Foods (food_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

insert into Sales_history_has_food (sales_history_id, food_id, count)
values(1,2,356),(2,1,22),(3,2,45);


-- -----------------------------------------------------
-- Table `Inventories`
-- -----------------------------------------------------
CREATE or replace TABLE Inventories (
  inventory_id INT NOT NULL AUTO_INCREMENT UNIQUE,
  client_id INT NOT NULL,
  food_id INT NOT NULL,
  item_count INT NOT NULL,
  units VARCHAR(45) NOT NULL,
  PRIMARY KEY (inventory_id),
  CONSTRAINT `fk_Inventories_Clients1`
    FOREIGN KEY (client_id)
    REFERENCES `Clients` (client_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Inventories_Foods1`
    FOREIGN KEY (`food_id`)
    REFERENCES `Foods` (food_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

insert into Inventories (client_id, food_id, item_count, units)
Values 
(1,1,20, 'lbs'),
(1,2,356, 'lbs'),
(2,3,22,'lbs'),
(2,1,11,'lbs');

SET FOREIGN_KEY_CHECKS=1;
COMMIT;

select * from Foods;
-- Drop table Clients, Foods, Inventories, Regions, Sales_history, Sales_history_has_food;