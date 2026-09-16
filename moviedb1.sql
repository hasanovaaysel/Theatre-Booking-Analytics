CREATE DATABASE movie_booking_db;
use movie_booking_db;
create table customers(
customer_id int primary key auto_increment,
customer_name varchar(30),
gender varchar(10),
city varchar(50),
signup_date date
);
create table movies(
movie_id int primary key auto_increment,
movie_name varchar(100),
genre varchar(20),
language varchar(15),
duration  int
);
create table theatres(
theatre_id int primary key auto_increment,
theatre_name varchar(20),
city varchar(20),
total_seats int
);
create table bookings(
booking_id int primary key auto_increment,
customer_id int,
movie_id int,
theatre_id int,
show_date datetime,
seats_booked int,
ticket_amount decimal(10,2),
booking_status VARCHAR(20),
payment_method VARCHAR(30),
foreign key(customer_id) references customers(customer_id),
foreign key(movie_id) references movies(movie_id),
foreign key(theatre_id) references theatres(theatre_id)
);
INSERT INTO customers
(customer_name, gender, city, signup_date)
VALUES
('Aysel Mammadova', 'Female', 'Baku', '2026-01-05'),
('Murad Aliyev', 'Male', 'Ganja', '2026-01-08'),
('Nigar Hasanli', 'Female', 'Sumqayit', '2026-01-11'),
('Elvin Quliyev', 'Male', 'Baku', '2026-01-14'),
('Leyla Abbasova', 'Female', 'Ganja', '2026-01-17'),
('Kamran Aliyev', 'Male', 'Baku', '2026-01-20'),
('Zahra Mammadli', 'Female', 'Sumqayit', '2026-01-23'),
('Orkhan Huseynov', 'Male', 'Mingachevir', '2026-01-26'),
('Fatima Rzayeva', 'Female', 'Baku', '2026-01-29'),
('Tural Ibrahimov', 'Male', 'Ganja', '2026-02-02'),
('Aylin Gasimova', 'Female', 'Baku', '2026-02-05'),
('Rauf Mammadov', 'Male', 'Shaki', '2026-02-08'),
('Sevinc Aliyeva', 'Female', 'Baku', '2026-02-11'),
('Emin Babayev', 'Male', 'Sumqayit', '2026-02-14'),
('Gunel Hasanli', 'Female', 'Ganja', '2026-02-17'),
('Samir Quliyev', 'Male', 'Baku', '2026-02-20'),
('Lale Abdullayeva', 'Female', 'Mingachevir', '2026-02-23'),
('Nihad Karimov', 'Male', 'Baku', '2026-02-26'),
('Sabina Valiyeva', 'Female', 'Ganja', '2026-03-01'),
('Javid Mustafayev', 'Male', 'Sumqayit', '2026-03-04');
INSERT INTO movies
(movie_name, genre, language, duration)
VALUES
('The Last Mission', 'Action', 'English', 142),
('Baku Nights', 'Drama', 'Azerbaijani', 118),
('Shadow Code', 'Thriller', 'English', 128),
('Love in Baku', 'Romance', 'Azerbaijani', 112),
('The Silent House', 'Horror', 'English', 105),
('Beyond Mars', 'Sci-Fi', 'English', 136),
('Funny Neighbours', 'Comedy', 'Azerbaijani', 101),
('The Forgotten Road', 'Drama', 'Turkish', 124),
('City Hunters', 'Action', 'Turkish', 139),
('Little Stars', 'Animation', 'English', 94),
('Midnight Call', 'Horror', 'Turkish', 108),
('Code 404', 'Thriller', 'English', 121),
('Summer Story', 'Romance', 'Azerbaijani', 110),
('The Last Kingdom', 'Action', 'English', 151),
('Family Weekend', 'Comedy', 'Azerbaijani', 99),
('Ocean Mystery', 'Adventure', 'English', 130),
('Lost Memories', 'Drama', 'Turkish', 117),
('Robot World', 'Sci-Fi', 'English', 126),
('The Detective', 'Thriller', 'Azerbaijani', 115),
('Magic Planet', 'Animation', 'English', 97);
INSERT INTO theatres
(theatre_name, city, total_seats)
VALUES
('Park Cinema Flame Towers', 'Baku', 300),
('Cinema Plus 28 Mall', 'Baku', 250),
('Park Cinema Metro Park', 'Baku', 220),
('Cinema Plus Ganjlik Mall', 'Baku', 280),
('Ganja Mall Cinema', 'Ganja', 200),
('Ganja Cinema Center', 'Ganja', 180),
('Sumqayit Cinema', 'Sumqayit', 220),
('Mingachevir Cinema', 'Mingachevir', 160),
('Shaki Cinema', 'Shaki', 150),
('Baku City Cinema', 'Baku', 260);
ALTER TABLE theatres
MODIFY theatre_name VARCHAR(150);
ALTER TABLE bookings
ADD COLUMN ticket_price DECIMAL(10,2);
DESCRIBE bookings;
INSERT INTO bookings
(customer_id, movie_id, theatre_id, show_date, seats_booked,
 ticket_price, ticket_amount, booking_status, payment_method)
VALUES
(1, 3, 1, '2026-01-05 18:30:00', 2, 10.00, 20.00, 'Confirmed', 'Debit Card'),
(2, 7, 2, '2026-01-08 20:00:00', 3, 12.00, 36.00, 'Confirmed', 'Credit Card'),
(3, 5, 3, '2026-01-12 16:00:00', 1, 8.00, 8.00, 'Cancelled', 'Cash'),
(4, 10, 4, '2026-01-15 19:30:00', 4, 10.00, 40.00, 'Confirmed', 'Debit Card');
SELECT count(*)
FROM bookings;
SELECT *
FROM theatres;

UPDATE bookings
SET ticket_price =
    8
    + CASE
        WHEN HOUR(show_date) >= 21 THEN 1
        ELSE 0
      END
    + CASE
        WHEN WEEKDAY(show_date) + 1 IN (6, 7) THEN 1
        ELSE 0
      END;
      SET SQL_SAFE_UPDATES = 0;
      
UPDATE bookings
SET ticket_amount= seats_booked * ticket_price;

select count(*) from bookings; #Total Bookings
select sum(seats_booked) from bookings;#Total Tickets Sold
select sum(ticket_amount) from bookings;#Total Revenue
select avg(ticket_price) from bookings;


select m.movie_id,m.movie_name,
sum(b.seats_booked) as total_tickets
from movies m
join bookings b
	on m.movie_id=b.movie_id
group by m.movie_id,m.movie_name
order by total_tickets desc;

select m.movie_id,m.movie_name,sum(b.ticket_amount) as total_revenue
from movies m 
join bookings b on m.movie_id=b.movie_id
group by m.movie_id,m.movie_name
order by total_revenue desc;

SELECT
    show_date,
    WEEKDAY(show_date) + 1 AS day_number,
    CASE
        WHEN WEEKDAY(show_date) + 1 IN (6, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type
FROM bookings;

SELECT
    CASE
        WHEN WEEKDAY(show_date) + 1 IN (6, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY day_type;

select 
	case
		when weekday(show_date)+1 in(6,7) then 'weekend'
		else 'weekday'
	end as day_type,
	sum(ticket_amount) as total_revenue
from bookings 
group by day_type;

select 
hour(show_date) as show_hour,
count(*) as total_bookings
from bookings
group by show_hour
order by total_bookings desc limit 5;

SELECT
    payment_method,
    COUNT(*) AS total_bookings,
    SUM(ticket_amount) AS total_revenue
FROM bookings
GROUP BY payment_method;

SELECT
    booking_status,
    COUNT(*) AS total_booking
FROM bookings
GROUP BY booking_status;
