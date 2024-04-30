#!/usr/bin/env python3
# This file universityConsole, which is a command-line console for managing universities.

import cmd
from app import db
from app import app
from app.models import University

class UniversityConsole(cmd.Cmd):
    """
    Class representing a command-line console for managing universities.
    """

    prompt = '(University Console) '

    def do_add(self, line):
        """
        Method for adding a new university to the database.
        
        Arguments:
        line -- a string containing the university details separated by
        spaces (name, location, website, status)
        e.g. add "University of Example" "Example City" "example.com" "open"
        """
        
        parts = line.split('" "')
        if len(parts) != 4:
            print("Invalid input. Expected format: \"name\" \"location\" \"website\" \"status\"")
            return
        name, location, website, status = parts
        name = name.strip('"')
        location = location.strip('"')
        website = website.strip('"')
        status = status.strip('"')
        with app.app_context():
            university = University(
                name=name,
                location=location,
                website=website,
                status=status
                )
            db.session.add(university)
            db.session.commit()
        print(f'Added university: {name}')

    def do_update(self, line):
        """
        Method for updating a university in the database.
        
        Arguments:
        line -- a string containing the university details separated by 
        spaces (id, name, location, website, status)
        e.g. update "1" "University of Example" "Example City" "example.com" "open"
        """
        
        parts = line.split('" "')
        if len(parts) != 5:
            print("Invalid input. Expected format: id \"name\" \"location\" \"website\" \"status\"")
            return
        id, name, location, website, status = parts
        id = id.strip('"')
        name = name.strip('"')
        location = location.strip('"')
        website = website.strip('"')
        status = status.strip('"')
        with app.app_context():
            university = University.query.filter_by(id=id).first()
            if university is None:
                print(f'University with id {id} not found')
                return
            university.name = name
            university.location = location
            university.website = website
            university.status = status
            db.session.commit()
        print(f'Updated university: {name}')
    
    def do_delete(self, line):
        """
        Method for deleting a university from the database.
        
        Arguments:
        line -- a string containing the id of the university to delete
        e.g. delete 1
        """
        
        id = line.strip('"')
        with app.app_context():
            university = University.query.filter_by(id=id).first()
            if university is None:
                print(f'University with id {id} not found')
                return
            db.session.delete(university)
            db.session.commit()
        print(f'Deleted university with id {id}')

    def do_get(self, line):
        """
        Method for getting a university from the database.
        
        Arguments:
        line -- a string containing the id of the university to get
        e.g. get 1
        """
        
        id = line.strip('"')
        with app.app_context():
            university = University.query.filter_by(id=id).first()
            if university is None:
                print(f'University with id {id} not found')
                return
            print(f'{university.id}: {university.name} ({university.location}, {university.website}, {university.status})')

    def do_list(self, line):
        """
        Method for listing all universities in the database.
        Arguments: line - not used
        """
        
        with app.app_context():
            universities = University.query.all()
            for university in universities:
                print('{}: {} ({}, {}, {})'.format(
                    university.id,
                    university.name,
                    university.location,
                    university.website,
                    university.status
                    ))

    def do_quit(self, line):
        """
        Method for quitting the console
        Arguments: line - not used
        """
        
        return True

    def help(self):
        """
        Method for displaying general help information.
        """
        
        print("Available commands:")
        print("  add <name> <location> <website> <status> - Add a new university to the database")
        print("  list - List all universities in the database")
        print("  quit - Quit the console")

    def help_add(self):
        """
        Method for displaying help information for the 'add' command.
        """
        
        print("Usage: add <name> <location> <website> <status>")
        print("Add a new university to the database.")
        print("Arguments:")
        print("  name - Name of the university")
        print("  location - Location of the university")
        print("  website - Website of the university")
        print("  status - Status of the university")

if __name__ == '__main__':
    UniversityConsole().cmdloop()