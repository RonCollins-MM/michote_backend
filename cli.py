#!/usr/bin/python3

"""This module contains the definition of the command line interpreter (cli)
for michote.

The main purpose of the cli is to provide a shell-like interface for
object manipulation useful for development and debugging.
"""

import cmd

from models import storage
from models.base_model import BaseModel
from models.customer import Customer
from models.booked_trip import BookedTrip
from models.company import Company
from models.vehicle import Vehicle
from models.admin import Admin
from models.price import Price
from models.destination import Destination

class MichoteCommand(cmd.Cmd):
    """Class definition for the command intepreter.

    Inherits from the inbuilt ``cmd`` module. The inbuilt ``cmd`` module
    contains the necessary tools (inherited attributes) to setup a custom
    line-oriented command intepreter.
    """

    prompt = '(michote) '

    __classes = {
        'BaseModel': BaseModel, 'Customer': Customer,
        'BookedTrip': BookedTrip, 'Company': Company,
        'Vehicle': Vehicle, 'Admin': Admin,
        'Price': Price, 'Destination': Destination
    }


    # --------------- Elementary Functions -------------------------- #

    def emptyline(self):
        """Method called when an emptyline is entered.

        Does nothing.
        """
        pass

    def help_help(self):
        """Method called when ``help`` command is entered.

        Prints the useage of the help command.
        """
        print('Use this command to find out more information about other' +
              'commands.')
        self.__usage('help')

    def do_quit(self, arg):
        """Method called when ``quit`` command is entered.

        Exits the command interpreter.
        """
        print('\nbye...')
        return True

    def help_quit(self):
        """Prints info on ``quit`` command to user."""
        print('Use this command to exit the command line interpreter.')
        print('You may alternatively enter an `EOF` character.')
        self.__usage('quit')

    def do_EOF(self, arg):
        """Method called when EOF character is entered.

        Exits the command interpreter.
        """
        print('\n\nbye...')
        return True

    def help_EOF(self):
        """Print info on ``EOF`` command to user"""
        print('Use this command to exit the command line interpreter.')
        print('You may alternatively type the `quit` command.')
        self.__usage('EOF')

    def __avail_classes(self):
        """Prints the valid classes that can be used with commands"""
        print('The following classes are available to use: ')
            for key, value in MichoteCommand.__classes:
                print(f'\t{MichoteCommand.__classes[key]}')


    def __usage(self, command):
        """Prints the correct usage for each command to the user"""
        if command == 'help':
            print('usage:\n\thelp <command>')
        elif command == 'quit':
            print('usage:\n\tquit\n(command takes no arguments)')
        elif command == 'EOF':
            print('usage:\n\t<EOF character>\nRefer to your operating' +
                  'system specifications for how to enter EOF character')
        elif command == 'create':
            print('usage:\n\tcreate <class_name>')
        elif command == 'show':
            print('usage:\n\tshow <class_name> <object_id>')
        elif command == 'destroy':
            print('usage:\n\tdestroy <class_name> <object_id>')

    # ------------- Core Functions ---------------------------------- #

    def do_create(self, args):
        """Method called when ``create`` command is entered.

        Will create a new instance of the specified class.
        If no arguments are passed or if the arguments passed do not correspond
        to attributes of the class specified, an error message is printed.
        If object is created successfully, the id of the object is printed to
        the commandline.
        """
        if not args:
            print('** class name missing **\n')
            self.__usage('create')
            return
        if args not in MichoteCommand.__classes:
            print('** Class doesn\'t exist **\n')
            print('The following classes are available to use: ')
            self.__avail_classes()
            return
        new_instance = MichoteCommand.__classes[args]()
        storage.save()
        print(new_instance.id)

    def do_show(self, args):
        """Method called when ``show`` command is entered.

        Prints string representation of an instance based on class name and id.
        The following scenarios will trigger an error message: class name
        missing, class doesn't exist, id missing, instance not found.
        """
        # Get class name and id
        args_tuple = args.partition(' ')
        class_name = args_tuple[0]
        object_id = args_tuple[2]

        # Remove trailing arguments if any
        if object_id and ' ' in object_id:
            object_id = object_id.partition(' ')[0]

        # Make sure class name and object id are valid
        if not class_name:
            print('** class name missing **')
            self.__usage('show')
            return
        if class_name not in MichoteCommand.__classes:
            print('** class doesn\'t exist **')
            self.__avail_classes()
            return
        if not object_id:
            print('** object id missing **')
            return

        # print the object
        try:
            print(storage._FileStorage__objects[f'{class_name}.{object_id}'])
        except KeyError:
            print('** Object with that ID does not exists **')

    def do_destroy(self, args):
        """Deletes an object based on its class name and ID."""
        # get class name and id
        args_tuple = args.partition(' ')
        class_name = args_tuple[0]
        object_id = args_tuple[2]

        # Remove trailing arguments if any
        if object_id and ' ' in object_id:
            object_id = object_id.partition(' ')[0]

        # Make sure class name and object id are valid
        if not class_name:
            print('** class name missing **')
            self.__usage('destroy')
            return
        if class_name not in MichoteCommand.__classes:
            print('** class doesn\'t exist **')
            self.__avail_classes()
            return
        if not object_id:
            print('** object id missing **')
            return

        # Delete the object
        try:
            del (storage.all()[f'{class_name}.{object_id}'])
            storage.save()
        except KeyError:
            print('** Object with that ID does not exist **')

    def do_all(self, args):
        """Prints the string representation of all instances in storage"""
        objs_as_string = []

        if args:
            args = args.split(' ')[0] # ignore any other arguments if any
            if args not in MichoteCommand.__classes:
                print('** class doesn\'t exist **')
                self.__avail_classes()
                return
            for k, v in _FileStorage__objects.items():
                if k.split('.')[0] == args:
                    objs_as_string.append(str(v))
        else:
            for k, v in _FileStorage__objects.items():
                objs_as_string.append(str(v))

        print(objs_as_string)



if __name__ == '__main__':
    michote_intro = f'Michote, Starehe yako.\n\nWelcome to michote, an online' \
    ' ticket booking service.\nYou are using the command line' \
    ' interpreter, best used for debugging and dev work.' \
    '\nType "help" for a list of commands.'

    MichoteCommand().cmdloop(intro=michote_intro)
