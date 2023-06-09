-- select from tables

select * from Regions;

select * from Clients;

select * from Sales_history;

select * from Foods;

select * from Inventories;

select * from Sales_history_has_food;

-- join select for inventories
select Inventories.inventory_id, Clients.name, Foods.food_name, Inventories.item_count From Inventories
Inner join Clients ON Inventories.client_id = Clients.client_id
Inner join Foods ON Inventories.food_id = Foods.food_id;
	
-- join select for sales_history
select Sales_history.sales_history_id, Clients.name, Sales_history.date, Sales_history.total_cost, Sales_history.refund 
From Sales_history
Inner join Clients ON Sales_history.client_id = Clients.client_id;


-- insert statements;
-- Query for add a new character functionality with colon : character being used to 
-- denote the variables that will have data from the backend programming language

Insert into Regions (region_name)
Values (:region_name);

Insert into Clients (region_id, name, address, phone, email)
values (:region_id, :name, :address, :phone, :email);

Insert into Sales_history (client_id, date, total_cost, refund)
Values (:client_id, :date, :total_cost, :refund);

Insert into Foods (region_id, food_name, price)
Values (:region_id, :food_name, :price);

insert into Sales_history_has_food (sales_history_id, food_id, count)
values (:sales_history_id, :food_id, :count);

insert into Inventories (client_id, food_id, item_count)
Values (:client_id, :food_id, :item_count);

-- update

Update Regions
SET region_name = :region_name_input
Where region_id = :region_id_input;

Update Clients
SET 
region_id = :region_id_input,
name = :name_input,
address = :address_input,
phone = :phone_input,
email = :email_input
WHERE client_id = :client_id_input;

Update Sales_history
SET
client_id = :client_id_input,
date = :date_input,
total_cost = :total_cost_input,
refund = :refund_input
Where sales_history_id = sales_history_id_input;

Update Foods
SET
region_id = :region_id_input,
food_name = :food_name_input,
price = :price_input
Where food_id = food_id_input;


-- delete
Delete from Clients where client_id = :client_id;
Delete from Regions where region_id = :region_id;
Delete from Foods where food_id = :food_id;
Delete from Sales_history where sales_history_id = :sales_history_id;

