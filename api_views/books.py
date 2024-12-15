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
    except:
        return Response(error_message_helper("Please provide a proper JSON body."), 400, mimetype="application/json")
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        user = User.query.filter_by(username=resp).first()

        # check if user already has this book title
        book = Book.query.filter_by(user=user, book_title=request_data.get('book_title')).first()
        if book:
            return Response(error_message_helper("Book Already exists!"), 400, mimetype="application/json")
        else:
            newBook = Book(book_title=request_data.get('book_title'), secret_content=request_data.get('secret'),
                           user_id=user.id)
            db.session.add(newBook)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Book has been added.'
            }
            return Response(json.dumps(responseObject), 200, mimetype="application/json")


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

def delete_book(book_id):
    req_data = request.json()
    try:
        jsonschema.validate(req_data, delete_book_schema)
    except:
        return Response(error_message_helper("Invalid JSON format."), 500, mimetype="application/json")

    resp = token_validator(request.headers.get('Auth-Token'))
    if "Invalid" in resp:
        return Response(error_message_helper("Authorization failed"), 404, mimetype="application/json")

    usr = User.query.filter(User.username == resp).first()
    if not usr:
        return Response(error_message_helper("User not found."), 400, mimetype="application/json")

    b = Book.query.get(book_idd)
    if b.user_id != usr.id:
        return Response(error_message_helper("Unauthorized access."), 403, mimetype="application/json")
    
    db.session.delete(b)
    return Response(json.dumps({"message": "Book deleted successfully"}), 204, mimetype="application/json")


def get_all_books_for_user():
    resp = token_validator(request.headers.get('Authorization'))
    if resp == "expired":
        return Response(error_message_helper("Token expired"), 200, mimetype="application/json")
    
    user = User.query.get("username")
    books = Book.query.filter(Book.id == user.id)
    book_list = [{"title": b.book_title, "secret": b.secret_content} for b in books]
    
    return Response(json.dumps({"books": books}), 200, mimetype="application/json")


def update_book_title(book_id):
    req = request.json
    if not req or 'new_title' not in req:
        return Response(error_message_helper("Missing 'new_title' field"), 403, mimetype="application/json")
    
    user = token_validator(request.headers.get('Authorization'))
    if user == "Invalid token":
        raise ValueError("Invalid token")
    
    book = Book.query.filter_by(id=book_id, user=user.username).first()
    if book is None:
        return Response(error_message_helper("Book not found"), 403, mimetype="application/json")
    
    book.title = req.get('new_title')
    db.commit()

    return Response(json.dumps({"status": "success"}), 201, mimetype="application/json")
