/* Users  */

create table Users (
	id int primary key identity, 
	full_name varchar(255)
)

/* Orders */

create table Orders (
	id int primary key identity,
	order_date datetime,
	total_sum decimal(12,2),
	user_id int not null  references Users(id) on delete cascade
)

/* Transactions   */

create table Transactions (
	id int primary key identity,
	typeOfTransaction varchar(255) not null,
	order_id int not null  references Orders(id) on delete cascade
)

/* Products */
create table Products (
	id int primary key identity,
	name varchar(255) not null,
	price decimal(12, 2) not null
)

/* OrderProducts */

create table OrderItems (
	id int primary key identity,
	order_id int not null references Orders(id)  on delete cascade,
	product_id int not null references Products(id) on delete cascade,
	count_of_product int
)




/* ========>>> Tasks  <<<<============ */

-- N=1
declare @product_id int = 1;

if exists (select product_id from OrderItems where product_id = @product_id)
	print 'Ushbu maxsulot sotilgan'
else
	print 'Yoq sotilmagan'


-- N=2
select * from Orders o
full join OrderItems ot
on ot.order_id = o.id

-- N=3

with cte as (
select * ,
row_number() over (partition by o.user_id order by o.order_date desc) as filter_orders
from orders o)

select * from cte
where filter_orders <= 3

--N=4

select * from Transactions t
join Orders o
on t.order_id = o.id
where o.order_date >= '2025-02-02 02:05:44.000'

-- N=5

select top 3 with ties o.user_id, sum(count_of_product) as total_per_user from orders o
join OrderItems ot
on o.id = ot.order_id
group by o.user_id
order by total_per_user desc