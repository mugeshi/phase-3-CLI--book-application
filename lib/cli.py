import click
from models import Book, Order, Customer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create an SQLite engine and session for database interaction
engine = create_engine('sqlite:///bookstore.db')
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def main():
    """Bookstore Application CLI"""
    pass

# Define a CLI command to add a new book to the bookstore
@main.command()
@click.option('--title', prompt='Enter book title', help='Title of the book')
@click.option('--author', prompt='Enter author name', help='Author of the book')
@click.option('--genre', prompt='Enter genre', help='Genre of the book')
@click.option('--price', prompt='Enter price', type=int, help='Price of the book')
@click.option('--stocks', prompt='Enter stock quantity', type=int, help='Stock quantity of the book')  # Updated option name to 'stocks'

def add_book(title, author, genre, price, stocks):  # Updated parameter name to 'stocks'
    """Add a new book to the bookstore."""
    book = Book(titles=title, author=author, genre=genre, price=price, stocks=stocks)  # Updated attribute name to 'stocks'
    session.add(book)
    session.commit()
    click.echo(f"Book '{title}' added successfully.")

@main.command()
@click.option('--name', prompt='Enter customer name', help='Name of the customer')
@click.option('--contact_info', prompt='Enter contact information', help='Contact information of the customer')
def add_customer(name, contact_info):
    """Add a new customer to the bookstore."""
    customer = Customer(name=name, contact_info=contact_info)
    session.add(customer)
    session.commit()
    click.echo(f"Customer '{name}' added successfully with contact info: {contact_info}.")

@main.command()
def list_books():
    """List all books in the bookstore."""
    books = session.query(Book).all()

    if not books:
        click.echo("No books available.")
    else:
        # Sort the books by title
        sorted_books = sorted(books, key=lambda x: x.titles)
        
        click.echo("List of available books (sorted by title):")
        for book in sorted_books:
            click.echo(f"Title: {book.titles}, Author: {book.author}, Genre: {book.genre}, Price: {book.price}, Stock: {book.stocks}")  # Updated attribute name to 'stocks'

# Defining a CLI command to place an order for a book
@main.command()
@click.option('--customer', prompt='Enter customer name', help='Name of the customer')
@click.option('--book_id', prompt='Enter book ID', type=int, help='ID of the book to order')
@click.option('--quantity', prompt='Enter quantity', type=int, help='Quantity to order')
def place_order(customer, book_id, quantity):
    """Place an order for a book."""
    customer_record = session.query(Customer).filter_by(name=customer).first()
    
    if not customer_record:
        customer_record = Customer(name=customer)
        session.add(customer_record)
        session.commit()

    # Check if the book exists
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        click.echo(f"Book with ID {book_id} does not exist.")
        return

    if book.stocks is not None and book.stocks < quantity:
        click.echo(f"Sorry, there is not enough stock available for '{book.titles}'")
        return

    order = Order(customer_id=customer_record.id, book_id=book.id, quantity=quantity)
    session.add(order)
    
  
    if book.stocks is not None:
        book.stocks -= quantity  # Reduce stock
        session.commit()
        click.echo(f"Order placed successfully for '{book.titles}' by {customer}.")
    else:
        click.echo(f"Order placed successfully for '{book.titles}' by {customer}. However, stock information is not available.")
        
@main.command()
def list_orders():
    """List all orders in the bookstore."""
    orders = session.query(Order).all()

    if not orders:
        click.echo("No orders available.")
    else:
        click.echo("List of orders:")
        for order in orders:
            click.echo(f"Order ID: {order.id}, Customer: {order.customer.name}, Book: {order.book.titles}, Quantity: {order.quantity}")

#Delete operation
@main.command()
@click.option('--book_id', prompt='Enter book ID to delete', type=int, help='ID of the book to delete')
def delete_book(book_id):
    """Delete a book from the bookstore."""
    book = session.query(Book).filter_by(id=book_id).first()
    
    if not book:
        click.echo(f"Book with ID {book_id} does not exist.")
        return

    # Confirm with the user before deleting
    confirmation = click.confirm(f"Are you sure you want to delete '{book.titles}' (ID: {book.id})?")
    
    if confirmation:
        session.delete(book)
        session.commit()
        click.echo(f"Book '{book.titles}' (ID: {book.id}) deleted successfully.")
    else:
        click.echo(f"Deletion of '{book.titles}' (ID: {book.id}) canceled.")
   

if __name__ == "__main__":
    main()
