import click
from models import Book, Order, Customer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create an SQLite engine and session
engine = create_engine('sqlite:///bookstore.db')
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def main():
    """Bookstore Application CLI"""
    pass

@main.command()
@click.option('--title', prompt='Enter book title', help='Title of the book')
@click.option('--author', prompt='Enter author name', help='Author of the book')
@click.option('--genre', prompt='Enter genre', help='Genre of the book')
@click.option('--price', prompt='Enter price', type=int, help='Price of the book')
@click.option('--stock', prompt='Enter stock quantity', type=int, help='Stock quantity of the book')
def add_book(title, author, genre, price, stock):
    """Add a new book to the bookstore."""
    book = Book(titles=title, author=author, genre=genre, price=price, stock=stock)
    session.add(book)
    session.commit()
    click.echo(f"Book '{title}' added successfully.")

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
            click.echo(f"Title: {book.titles}, Author: {book.author}, Genre: {book.genre}, Price: {book.price}, Stock: {book.stock}")

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

    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        click.echo(f"Book with ID {book_id} does not exist.")
        return

    if book.stock < quantity:
        click.echo(f"Sorry, there is not enough stock available for '{book.titles}'")
        return

    order = Order(customer_id=customer_record.id, book_id=book.id, quantity=quantity)
    session.add(order)
    book.stock -= quantity  # Reduce stock
    session.commit()
    click.echo(f"Order placed successfully for '{book.titles}' by {customer}.")

if __name__ == "__main__":
    main()
