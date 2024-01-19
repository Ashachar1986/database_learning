from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#------------ Start SQL part ----------------

app.config.update( #Setting the configurations for the DB connection:

    SECRET_KEY='Hadar225', #This is the password we set when we installed Postgres and is used to access the DB
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Hadar225@localhost/catalog_db', #This is the info on how the code can access the DB. Templage: <database>://<user_id>:<password>@<server>/<database_name>
    SQLALCHEMY_TRACK_MODIFICATIONS=False #Optional.

)

db = SQLAlchemy(app) #This creates an instance of the SQLAlchemy class with our flask app class passed to it and is used to do SQL actions
                     #This has to be done after updating app.config.update() otherwise we will get an error that SQLALCHEMY_DATABASE_URI is not set.

#Tables

class Publication(db.Model): #This is going to be our bean class. By passing it the db.Model, it can inherit the necessary properties and methods from teh SQL Alchemy class
    __tablename__ = 'publication' #This is the actual name of the table as we created in Postgrasql

    id = db.Column(db.Integer, primary_key=True) #First class attribute/table column. It is of type integer and is the primary key)
    name = db.Column(db.String(80), nullable=False) #Second class attribute/table column. It is of type string with max of 80 chars and cannot be null

    def __init__(self, id, name): #The constructor method that is used to when an instance of the class is created.
        self.id = id
        self.name = name

    def __repr__(self): #The 'toString' method which retuns a string with the instance info.
        return 'Publication instance: The id is {} and the name is {}'.format(self.id,self.name)

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(500),nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #Relationship column (Foreign Key)
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, format, image, num_pages, pub_id): #If no id is defined in the init method, python flask creates one automatically
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

with app.app_context(): #This code makes sure the below method is ran within the context of the project and is a must to run it.
    db.create_all() #This method creates all the table defined by our bean objects unless they already exist. If that is the case, this is skipped.


#CRUD: Create

def create_single(data_bean): #This is a create funtion that inserts one data object to the database. The function takes one data object as argument
    with app.app_context(): #To work we must run inside the app context
        db.session.add(data_bean) #This code takes the data object and adds it as a row in the database.
        db.session.commit() #This code commits the insertation of the data object and if not run, the object will not be written permenently to the database.

def create_multiple(data_bean_list): #This is a create funtion that inserts multiple data objects to the database. The function takes a list of data objects as argument
    with app.app_context(): #To work we must run inside the app context
        db.session.add_all(data_bean_list) #This code takes the data object list and adds it as rows in the database.
        db.session.commit() #This code commits the insertation of the data objects and if not run, the objects will not be written permenently to the database.


# Publication instances
stimatski = Publication(104,"Stimatski") #This creats an instance of the publication class
star = Publication(105,"Star") #This creats an instance of the publication class
haifa = Publication(106,"Haifa board") #This creats an instance of the publication class

#Book instances
robin_hood = Book("The Merry Adventures of Robin Hood","Howard Pyle",4.3,"Hard-Cover","Images\Robin hood img.jpg",192,100)
peter_pan = Book("Peter Pan","J.M Barrie",4.7,"Hard-Cover","Images\Peter Pan.jpg",201,101)
harry_potter = Book("Harry Potter and the Philosopher's Stone","J.K Rowling",2.7,"Hard-Cover","Images\Harry_Potter_and_the_Philosopher's_Stone_Book_Cover.jpg",223,104)
harry_potter2 = Book("Harry Potter and the Chambers of Secrets","J.K Rowling",4.8,"Hard-Cover","Images\Harry_Potter_and_the_Chamber_of_Secrets.jpg",251,104)

#Calling the create functions
# create_single(stimatski) This runs the single create function above which sends our instance to the function and gets it added as a row to the database
# create_multiple([star,haifa]) This runs the mutliple create function above which sends a list of instances to the fucction and gets them added as rows to the database
# create_multiple([robin_hood,peter_pan,harry_potter])
# create_single(harry_potter2)

#CRUD: Read

with app.app_context():
    print(Book.query.all()) #This query method returns all instances of the called class from the database (all rows) as a list and displays their __repr__ method
    all_books = Book.query.all() #we can also save the list into a variable
    print(Book.query.first()) #This query method only returns the first row in the database.

    print(Book.query.filter_by(author='J.K Rowling').all()) #The filter_by method takes 1 argument which is the column name equals a specific value, such as in this
                                                            #case where the author column is equal to J.K Rowling and then goes over all of the rows and brings back
                                                            #only the __repr__ result of the rows where the specified column (author in this case) is equal to the
                                                            #value specified (J.K Rowling in this case.
                                                            #### We have to add the .all() at the end or it wouldn't work. That is because the .all() tells the code
                                                            #### to run through all the rows for the query
    print(Book.query.filter_by(author='J.K Rowling').first()) #The .first() method works the same way as the .all() method, but once it finds the first row that fits
                                                              #the filter it returns it and stops the query, so you only get the first instance found.
    print(Book.query.get_or_404(2)) #The .get() method returns the row whose primary key number is entered in it. So in this caes, it will return the row with primary key 2.
                             #If we enter a primary key we don't have we will get a 404 error

    print(Book.query.limit(2).all()) #The .limit() method takes a number as arguments and returns the first amount of rows as per the number. In this case, it will
                                     #return the first 2 rows.
                                     #We still have to add the .all() afterwards or it will not work.

    print(Book.query.order_by(Book.title).all()) #The order_by() method takes a name of a column/class attribute as an argument and returns the information from the
                                                 #database ordered alphabetically by that column values. For instance, in the case, we get all the data in the book
                                                 #table ordered alphabetically by the title column.

    print(Book.query.filter_by(author='J.K Rowling').order_by(Book.title).all()) #We can also chain methods to get more specific results. In this case we first
                                                                                 #filter the result set by the author so we only get back rows where the author is
                                                                                 #J.K Rowling and then order it by the book title.

    book1 = Book.query.first() #IMPORTANT NOTE: When querying data from the DB, we get back the entire object back so we can always get the info from any of the
    print(book1.num_pages)                      #columns. For instance, in the case, we set book1 to get first book data from teh book table so we can use the
                                                #class.attribute notation to get the relevant value, such as getting the number of pages.

    book_list = Book.query.all() #When we call the .all() we get a list of all the tables, so in order to get to the specific instance's data, we need to specify
    print(book_list[0].num_pages) #the list's index and then use the attribute name.

    for book in book_list: #Just like with any list, we can iterate over its items using a for in loop and then use an if statment.
        if book.title == "The Merry Adventures of Robin Hood":
            print(book.num_pages)

    stimatski = Publication.query.filter_by(name='Stimatski').first() #We can use the primary key - foreign key relationship we set up when creating the tables
    print(Book.query.filter_by(pub_id =stimatski.id).all()) #to query information from one table using the foreign key in another table. We do this by first getting
                                                            #the primary key from the first table and then querying the second table with a filter using the value
                                                            #we got. In this case, we first got the stimatski instance from the publication table and then did a
                                                            #query for the book table with a filter using the pub_id (which is the foregin key linked to the
                                                            #primary key in the publication table) that is equal to stimatski's id. What this does is go over the
                                                            #whole book data and only returns objects where the pub_id is 104, which is stimatski's primary key.

    print("filter",Book.query.filter(Book.avg_rating > 3).all()) #The .filter(), which is different than .filter_by(), takes class.attribute as a parameter and allows
                                                                 #to run more advance quries than the .filter_by such as bigger or smaller than, or AND/OR.

    def get_full_book_list():
        return Book.query.all()

#CRUD: Updating

    with app.app_context(): #To update a record in the db we need to follow 3 steps:
        peter_pan_book = Book.query.filter_by(title='Peter Pan').first() #1: Get an instance of the row we want to update into a variable
        peter_pan_book.format = 'AudioBook' #Use the instance.attribute method to change the value we want in the instance.
        db.session.commit() #run the commit command (just like when adding a new row to the table) so that the new value will replace the old on in the table.

#CRUD: Deleting

    #1st method
    with app.app_context(): #To delete a record from the DB we need to follow 3 steps:
        if 3 == 4: #Using this so that the code wouldn't run again since I already deleted this record.
            harry_potter_book2 = Book.query.get_or_404(5) #1: Get an instance of the row we want to update into a variable
            db.session.delete(harry_potter_book2) #Use the db.session.delete() method and pass it the instance of the data we want to delete
            db.session.commit() #run the commit command (just like when adding a new row to the table) so that the value will be deleted from the table in the db.

    #2nd method
    with app.app_context():
        if 3==4:
            Book.query.filter_by(pub_id = 104).delete()
            db.session.commit()


    #Method #1 is quicker if we already have an instance of the object we want to delete and option 2 is quicker if we don't have an instance ready as it both
    #gets the record from the db and delets it in one line of code.

    #Also, take note that the first method can only delete one record at a time while the second method can delete multiple rows at a time.

    #IMPORTANT NOTE: we can't delete records in a parent table (tables whose primary key is a foregin key in a diffrent table) while there are still records linking
                     #linking to it in the child table (the table that has the parent's primary key as a foregin key in it). To delete such records we first must
                     #delete every record in the child table that is linked via the keys to the parent table. For instance, to delete a a publication record in the
                     #publication table, we first must delete all records in the book table who have that publisher's id as the pub_id foregin key.

#------------ End SQL part ----------------

@app.route('/')
def landing_page():
    return '<h1>This is the landing page</h1>'

@app.route('/books')
def display_book_list():
    book_list = get_full_book_list()
    return render_template('books.html',books = book_list)

if __name__ == '__main__':
    app.run()
