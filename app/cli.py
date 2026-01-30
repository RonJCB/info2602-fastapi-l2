import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

cli = typer.Typer()

@cli.command()
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        bob = User('bob', 'bob@mail.com', 'bobpass') # Create a new user (in memory)
        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)
        print("Database Initialized")


#Exercise 1
#Create a cli command that
#allows you to find a user using a 
#partial match of their email OR username.
@cli.command()
def findUserPartial(username:str, email :str):
    with get_all_users as db:
        user = db.exec(select(User).where(User.username == username)).first()
        email = db.exec(select(User).where(User.email == email)).first()
        if not user or email:
            print(f"{user} or {email} not found in DB!")
            return
        print("User found: {user} with email {email}")
    
@cli.command()
#command searches the created database in memory
#by referencing the name field
def get_user(username:str):
    # The code for task 5.1 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f'{username} not found!')
            return
        print(user)

@cli.command()
def get_all_users():
    # The code for task 5.2 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        all_users = db.exec(select(User)).all()
        if not all_users:
            print("No users found in database")
        else:
            #remember .all() object
            for user in all_users:
                print(user)


@cli.command()
def change_email(username: str, new_email:str):
    # The code for task 6 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        #get first username that matchs
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f"{username} not found! Unable to update email")
            return
        user.email = new_email #update object
        db.add(user)#reference chances to database
        db.commit()
        print(f"Updated{user.username} email to {user.email}")


@cli.command()
#safely add objects to the datbase
#ensures transcations are safely discarded if username or email is taken
def create_user(username: str, email:str, password: str):
    # The code for task 7 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        newuser = User(username,email,password)#call our userobject we created
        try:#try adding an object to the db
            db.add(newuser)
            db.commit()
        except IntegrityError as e:
            db.rollback()#undoes the add and commit object
            print(f"{username} or {email} already taken!")
        else:
            print(newuser)
@cli.command()
def delete_user(username: str):
    # The code for task 8 goes here. Once implemented, remove the line below that says "pass"
    #with get_session() as db:
     with get_session() as db:
         user = db.exec(select(User).where(User.username == username)).first()
         if not user:
             print(f"{username} not found! Unable to delete user")
             return
         db.delete(user)
         db.commit()#flush pending changes
         print(f"{username} deleted") 


if __name__ == "__main__":
    cli()