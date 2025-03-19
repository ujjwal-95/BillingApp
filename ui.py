from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QListWidget
)
from database import Database

class BillingUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Application")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Billing Form
        self.customer_name = QLineEdit(self)
        self.customer_name.setPlaceholderText("Enter Customer Name")
        layout.addWidget(self.customer_name)

        self.customer_phone = QLineEdit(self)
        self.customer_phone.setPlaceholderText("Enter Phone Number")
        layout.addWidget(self.customer_phone)

        self.customer_email = QLineEdit(self)
        self.customer_email.setPlaceholderText("Enter Email Address")
        layout.addWidget(self.customer_email)

        self.item_details = QTextEdit(self)
        self.item_details.setPlaceholderText("Enter Item Details")
        layout.addWidget(self.item_details)

        self.total_amount = QLineEdit(self)
        self.total_amount.setPlaceholderText("Enter Total Amount")
        layout.addWidget(self.total_amount)

        self.save_button = QPushButton("Save Bill", self)
        self.save_button.clicked.connect(self.save_bill)
        layout.addWidget(self.save_button)

        # List of Bills
        self.bill_list = QListWidget(self)
        self.bill_list.itemClicked.connect(self.show_bill_details)
        layout.addWidget(self.bill_list)

        # Bill Details (Hidden by default)
        self.bill_details = QLabel("")
        layout.addWidget(self.bill_details)

        self.setLayout(layout)
        self.load_data()

    def save_bill(self):
        name = self.customer_name.text()
        phone = self.customer_phone.text()
        email = self.customer_email.text()
        items = self.item_details.toPlainText()
        amount = self.total_amount.text()

        if not name or not amount:
            return  # Don't save if required fields are empty

        db = Database()
        customer_id = db.add_customer(name, phone, email)
        db.add_bill(customer_id, items, amount)

        self.customer_name.clear()
        self.customer_phone.clear()
        self.customer_email.clear()
        self.item_details.clear()
        self.total_amount.clear()

        self.load_data()

    def load_data(self):
        """Loads the bills list with format: Bill ID - Customer Name - Amount"""
        self.bill_list.clear()
        db = Database()

        bills = db.fetch_bills_with_customer()
        for bill in bills:
            self.bill_list.addItem(f"Bill {bill[0]} - {bill[1]} - ₹{bill[2]}")

    def show_bill_details(self, item):
        """Displays full bill details when a bill is clicked."""
        bill_id = int(item.text().split(" ")[1])  # Extract bill ID
        db = Database()
        self.bill_details.setText(self.get_bill_details(bill_id, db))

    def get_bill_details(self, bill_id, db):
        """Fetches full bill details and returns formatted string."""
        db.cursor.execute("""
            SELECT b.id, c.name, c.phone, c.email, b.item_details, b.total_amount, b.bill_date
            FROM bills b
            JOIN customers c ON b.customer_id = c.id
            WHERE b.id = %s
        """, (bill_id,))
        bill = db.cursor.fetchone()

        if bill:
            return (f"Bill ID: {bill[0]}\n"
                    f"Customer: {bill[1]}\n"
                    f"Phone: {bill[2]}\n"
                    f"Email: {bill[3]}\n"
                    f"Items: {bill[4]}\n"
                    f"Total Amount: ₹{bill[5]}\n"
                    f"Date: {bill[6]}")
        else:
            return "No details found."

if __name__ == "__main__":
    app = QApplication([])
    window = BillingUI()
    window.show()
    app.exec()
