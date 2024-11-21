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

def update_book(book_title):
    request_data = request.get_json()
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        user = User.query.filter_by(username=resp).first()
        book = Book.query.filter_by(user=user, book_title=str(book_title)).first()
        
        if book:
            # Update book fields if present in request
            if 'book_title' in request_data:
                book.book_title = request_data['book_title']
            if 'secret' in request_data:
                book.secret_content = request_data['secret']
            
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Book has been updated.'
            }
            return Response(json.dumps(responseObject), 200, mimetype="application/json")
        else:
            return Response(error_message_helper("Book not found!"), 404, mimetype="application/json")


def delete_book(book_title):
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        user = User.query.filter_by(username=resp).first()
        book = Book.query.filter_by(user=user, book_title=str(book_title)).first()
        
        if book:
            db.session.delete(book)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Book has been deleted.'
            }
            return Response(json.dumps(responseObject), 200, mimetype="application/json")
        else:
            return Response(error_message_helper("Book not found!"), 404, mimetype="application/json")


def get_books_by_user(username):
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        user = User.query.filter_by(username=username).first()
        if user:
            books = Book.query.filter_by(user=user).all()
            books_data = [{'book_title': book.book_title, 'secret': book.secret_content} for book in books]
            return Response(json.dumps({'books': books_data}), 200, mimetype="application/json")
        else:
            return Response(error_message_helper("User not found!"), 404, mimetype="application/json")


def search_books(query):
    resp = token_validator(request.headers.get('Authorization'))
    if "expired" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    elif "Invalid token" in resp:
        return Response(error_message_helper(resp), 401, mimetype="application/json")
    else:
        books = Book.query.filter(Book.book_title.ilike(f'%{query}%')).all()
        books_data = [{'book_title': book.book_title, 'secret': book.secret_content} for book in books]
        
        if books_data:
            return Response(json.dumps({'books': books_data}), 200, mimetype="application/json")
        else:
            return Response(error_message_helper("No books found matching the search query."), 404, mimetype="application/json")
