from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
'''
All authors have a name.
No two authors have the same name.
Author phone numbers are exactly ten digits.
All posts have a title.
Post content is at least 250 characters long.
Post summary is a maximum of 250 characters.
Post category is either Fiction or Non-Fiction.
'''


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())



#All authors have a name.
#No two authors have the same name.

    @validates('name',)
    def validate_name(self, key, name):
        if not name:
            raise ValueError('No author name provided')
        elif Author.query.filter(Author.name == name).first():
            raise ValueError('Name already in use')
        return name
    
    @validates('phone_number',)
    def validate_phone(self, key, number):
        if len(number) != 10:
            raise ValueError('Author phone numbers must be exactly 10 digits long')
        return number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Post content is at least 250 characters long.
# Post summary is a maximum of 250 characters.
# Post category is either Fiction or Non-Fiction.

    @validates('content')
    def validates_content(self, key, content):
        if len(content) <= 250:
            raise ValueError('Content is too short. Must be at least 250 characters long')
        return content
    
    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError('Summary is too long. Must be less than 250 characters.')
        return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Incorrect category')
        return category
    
    @validates('title')
    def validates_title(self, key, title):
        #if title does not contain any words in the list of click bait words, raise error
        #google: python check to see if list of words are in string
        required_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in required_words):
            raise ValueError("Make title more clickbait-y")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    
