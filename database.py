import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        """Initialize the database connection"""
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create customers and bills tables if they don't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                email VARCHAR(100)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                item_details TEXT,
                total_amount DECIMAL(10,2),
                bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def add_customer(self, name, phone, email):
        """Add a new customer and return the customer ID"""
        self.cursor.execute(
            "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_bill(self, customer_id, item_details, total_amount):
        """Add a bill for a given customer"""
        self.cursor.execute(
            "INSERT INTO bills (customer_id, item_details, total_amount) VALUES (%s, %s, %s)",
            (customer_id, item_details, total_amount)
        )
        self.conn.commit()

    def fetch_bills_with_customer(self):
        """Fetch all bills along with the customer name and total amount"""
        self.cursor.execute("""
            SELECT b.id, c.name, b.total_amount 
            FROM bills b 
            JOIN customers c ON b.customer_id = c.id
        """)
        return self.cursor.fetchall()

    def fetch_bill_details(self, bill_id):
        """Fetch full details of a specific bill"""
        self.cursor.execute("""
            SELECT b.id, c.name, c.phone, c.email, b.item_details, b.total_amount, b.bill_date
            FROM bills b 
            JOIN customers c ON b.customer_id = c.id
            WHERE b.id = %s
        """, (bill_id,))
        return self.cursor.fetchone()

    def close_connection(self):
        """Close the database connection"""
        self.cursor.close()
        self.conn.close()

# Run this only once to ensure tables are created
if __name__ == "__main__":
    db = Database()
    db.create_tables()
    print("Database setup completed successfully!")
