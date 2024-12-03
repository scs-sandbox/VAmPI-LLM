import jsonschema

from api_views.users import token_validator
from config import db
from api_views.json_schemas import *
from flask import jsonify, Response, request, json
from models.user_model import User
from models.books_model import Book
from app import vuln


def error_message_helper(msg):
    return '{ "status": "fail", "message": "' + msg + '"}'


def get_all_books():
    return_value = jsonify({'Books': Book.get_all_books()})
    return return_value


def add_new_book():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, add_book_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")
    
    auth_header = request.headers.get('Authorization')
    resp = token_validator(auth_header)
    
    if "expired" in resp:
        return Response(error_message_helper("Token expired. Please log in again."), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper("Invalid token. Please log in again."), 401, mimetype="application/json")
    
    user = User.query.filter_by(username=resp).first()
    if not user:
        return Response(error_message_helper("User not found."), 404, mimetype="application/json")

    # Check if the user already has this book title
    existing_book = Book.query.filter_by(user=user, book_title=request_data.get('book_title')).first()
    if existing_book:
        return Response(error_message_helper("Book already exists!"), 400, mimetype="application/json")
    
    # Add the new book
    try:
        new_book = Book(
            book_title=request_data.get('book_title'),
            secret_content=request_data.get('secret'),
            user_id=user.id
        )
        db.session.add(new_book)
        db.session.commit()
        responseObject = {
            'status': 'success',
            'message': 'Book has been added.'
        }
        return Response(json.dumps(responseObject), 201, mimetype="application/json")
    except Exception as e:
        db.session.rollback()
        return Response(error_message_helper("An error occurred while adding the book."), 500, mimetype="application/json")
        

def get_by_title(book_title):
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        if vuln:  # Broken Object Level Authorization
            book = Book.query.filter_by(book_title=str(book_title)).first()
            if book:
                responseObject = {
                    'book_title': book.book_title,
                    'secret': book.secret_content,
                    'owner': book.user.username
                }
                return Response(json.dumps(responseObject), 200, mimetype="application/json")
            else:
                return Response(error_message_helper("Book not found!"), 404, mimetype="application/json")
        else:
            user = User.query.filter_by(username=resp).first()
            book = Book.query.filter_by(user=user, book_title=str(book_title)).first()
            if book:
                responseObject = {
                    'book_title': book.book_title,
                    'secret': book.secret_content,
                    'owner': book.user.username
                }
                return Response(json.dumps(responseObject), 200, mimetype="application/json")
            else:
                return Response(error_message_helper("Book not found!"), 404, mimetype="application/json")
