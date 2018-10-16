from flask_restplus import reqparse

# Add more arguments if needed
books_parser = reqparse.RequestParser()
books_parser.add_argument('owner_id', help='The user_id of the owner')
books_parser.add_argument('title', help='The title of the book')
books_parser.add_argument('author_id', help='The id of the author')
books_parser.add_argument('year_start', help='Find books that published after some year')
books_parser.add_argument('year_end', help='Find books that published before some year')
books_parser.add_argument('genre', help='The genre that the books belong to')
books_parser.add_argument('list_name', help='The list name that the books belong to')

users_parser = reqparse.RequestParser()
users_parser.add_argument('username')

notes_parser = reqparse.RequestParser()
notes_parser.add_argument('book_id')
notes_parser.add_argument('user_id')

loans_parser = reqparse.RequestParser()
loans_parser.add_argument('book_id')
loans_parser.add_argument('user_id')

lists_parser = reqparse.RequestParser()
lists_parser.add_argument('list_name')
