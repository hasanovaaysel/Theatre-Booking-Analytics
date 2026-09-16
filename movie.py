import mysql.connector
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


connection = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="movie_booking_db"
)

cursor = connection.cursor()

print("Connected successfully!")

sql = """
INSERT INTO bookings
(
    customer_id,
    movie_id,
    theatre_id,
    show_date,
    seats_booked,
    ticket_price,
    ticket_amount,
    booking_status,
    payment_method
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i in range(500):

    customer_id = random.randint(1, 20)
    movie_id = random.randint(1, 20)
    theatre_id = random.randint(1, 10)

    seats_booked = random.randint(1, 6)

    start_date = datetime(2026, 1, 1)
    random_days = random.randint(0, 364)

    show_date = start_date + timedelta(days=random_days)

    hour = random.randint(14, 23)
    minute = random.choice([0, 30])

    show_date = show_date.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0
    )

    ticket_price = 8

    if show_date.hour >= 21:
        ticket_price += 1

    if show_date.weekday() in [5, 6]:
        ticket_price += 1

    ticket_amount = seats_booked * ticket_price

    if random.random() < 0.9:
        booking_status = "Confirmed"
    else:
        booking_status = "Cancelled"

    payment_method = random.choice([
        "Cash",
        "Debit Card",
        "Credit Card"
    ])

    booking = (
        customer_id,
        movie_id,
        theatre_id,
        show_date,
        seats_booked,
        ticket_price,
        ticket_amount,
        booking_status,
        payment_method
    )

    cursor.execute(sql, booking)


connection.commit()

print("500 bookings created successfully!")

query = "SELECT * FROM bookings"

df = pd.read_sql(query, connection)

print(df.head(10))
print(df.tail())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())

print(df["ticket_price"])

print(
    df[
        ["movie_id", "seats_booked", "ticket_amount"]
    ]
)

high_value = df[df["ticket_amount"] > 50]
print(high_value)

result = df[
    (df["ticket_amount"] > 20) &
    (df["booking_status"] == "Confirmed")
]

print(result)


sorted_df = df.sort_values(
    "ticket_amount",
    ascending=False
)

print(sorted_df.head(10))

print(df["booking_status"].value_counts())
print(df["payment_method"].value_counts())


total_revenue = df["ticket_amount"].sum()
print("Total Revenue:", total_revenue)

total_bookings = df.shape[0]
print("Total Bookings:", total_bookings)

total_seats = df["seats_booked"].sum()
print("Total Seats Sold:", total_seats)

average_booking = df["ticket_amount"].mean()
print("Average Booking:", average_booking)

median_booking = df["ticket_amount"].median()
print("Median Booking:", median_booking)

print("Maximum Booking:", df["ticket_amount"].max())
print("Minimum Booking:", df["ticket_amount"].min())


movie_booking = (
    df.groupby("movie_id")
    .size()
)

print(movie_booking)


movie_revenue = (
    df.groupby("movie_id")["ticket_amount"]
    .sum()
)

print(movie_revenue)


movie_stats = (
    df.groupby("movie_id")["ticket_amount"]
    .agg(["sum", "max", "min", "mean"])
)

print(movie_stats)


df["show_date"] = pd.to_datetime(df["show_date"])

df["year"] = df["show_date"].dt.year
df["month"] = df["show_date"].dt.month
df["hour"] = df["show_date"].dt.hour
df["weekday"] = df["show_date"].dt.day_name()

df["day_type"] = df["show_date"].dt.day_of_week.map(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)


monthly_revenue = (
    df.groupby("month")["ticket_amount"]
    .sum()
)

print(monthly_revenue)


hourly_revenue = (
    df.groupby("hour")["ticket_amount"]
    .sum()
)

print(hourly_revenue)


maks = monthly_revenue.max()
print("Maximum Monthly Revenue:", maks)


day_type_revenue = (
    df.groupby("day_type")["ticket_amount"]
    .sum()
)

print(day_type_revenue)

cancelled = (
    df["booking_status"] == "Cancelled"
).sum()

cancellation_rate = (
    cancelled / total_bookings
) * 100

print("Cancellation Rate:", cancellation_rate)

confirmed = (
    df["booking_status"] == "Confirmed"
).sum()

print("Confirmed Bookings:", confirmed)

confirmed_rate = (
    confirmed / total_bookings
) * 100

print("Confirmed Rate:", confirmed_rate)

movies = pd.read_sql(
    "SELECT * FROM movies",
    connection
)

print(movies)

movie_data = df.merge(
    movies,
    on="movie_id",
    how="left"
)

print(movie_data)

movie_revenue = (
    movie_data
    .groupby("movie_name")["ticket_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(movie_revenue)

customers = pd.read_sql(
    "SELECT * FROM customers",
    connection
)

customers_data = df.merge(
    customers,
    on="customer_id",
    how="left"
)


customers_analysis = (
    customers_data
    .groupby("customer_id")
    .agg(
        total_bookings=("booking_id", "count"),
        total_spent=("ticket_amount", "sum"),
        total_seats=("seats_booked", "sum")
    )
    .sort_values(
        "total_spent",
        ascending=False
    )
)

print(customers_analysis)




theatres = pd.read_sql(
    "SELECT * FROM theatres",
    connection
)

theatre_data = df.merge(
    theatres,
    on="theatre_id",
    how="left"
)


theatre_analysis = (
    theatre_data
    .groupby("theatre_id")
    .agg(
        total_bookings=("booking_id", "count"),
        total_revenue=("ticket_amount", "sum"),
        total_seats=("total_seats", "sum")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)

print(theatre_analysis)



print("Missing Values:")
print(df.isnull().sum())
print("Duplicate Rows:")
print(df.duplicated().sum())
dff = df.drop_duplicates()
print(dff)

df = df.merge(
    movies[["movie_id", "movie_name"]],
    on="movie_id",
    how="left"
)

df = df.merge(
    theatres[["theatre_id", "theatre_name"]],
    on="theatre_id",
    how="left"
)

print(df)


# MATPLOTLIB



#1. Monthly Revenue

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o",
    label="Revenue"
)
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (AZN)")
plt.grid()
plt.legend()
plt.show()


#2. Top 5 Movies by Revenue

movie_revenue = (
    movie_data
    .groupby("movie_name")["ticket_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_movies = movie_revenue.head(5)

plt.bar(
    top_movies.index,
    top_movies.values
)

plt.title("Top 5 Movies by Revenue")
plt.xlabel("Movie")
plt.ylabel("Revenue (AZN)")
plt.xticks(rotation=15)
plt.show()


#3. Top 5 Movies by Booking Count

movie_booking = (
    movie_data
    .groupby("movie_name")
    .size()
    .sort_values(ascending=False)
)

top_booking_movies = movie_booking.head(5)

plt.bar(
    top_booking_movies.index,
    top_booking_movies.values
)

plt.title("Top 5 Movies by Booking Count")
plt.xlabel("Movies")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=45)
plt.show()


#4. Weekday vs Weekend Revenue

plt.bar(
    day_type_revenue.index,
    day_type_revenue.values
)

plt.title("Weekday vs Weekend")
plt.xlabel("Day Type")
plt.ylabel("Revenue (AZN)")
plt.show()


#5. Booking by Hour

hour_counts = (
    df["hour"]
    .value_counts()
    .sort_index()
)

print(hour_counts)

plt.plot(
    hour_counts.index,
    hour_counts.values,
    marker="o"
)

plt.xlabel("Hour")
plt.ylabel("Number of Bookings")
plt.title("Booking by Hour")
plt.grid()
plt.show()


#6. Booking Amount Distribution

plt.hist(
    df["ticket_amount"],
    bins=10
)

plt.title("Booking Amount Distribution")
plt.ylabel("Frequency")
plt.xlabel("Ticket Amount")
plt.show()


#7. Seats Booked vs Ticket Amount

plt.scatter(
    df["seats_booked"],
    df["ticket_amount"]
)

plt.xlabel("Seats Booked")
plt.ylabel("Ticket Amount")
plt.title("Seats Booked vs Ticket Amount")
plt.show()



df.to_excel(
    "movie_booking_analysis.xlsx",
    index=False
)

print("Excel file created successfully!")



cursor.close()
connection.close()

