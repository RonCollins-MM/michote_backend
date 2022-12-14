#!/usr/bin/python3

"""This module contains the definition of the command line interpreter (cli)
for michote.

The main purpose of the cli is to provide a shell-like interface for
object manipulation useful for development and debugging.
"""

import cmd
import json

from models import storage
from models.base_model import BaseModel
from models.customer import Customer
from models.booked_trips import BookedTrips
from models.company import Company
from models.vehicle import Vehicle
from models.admin import Admin
from models.prices import Prices
from models.destination import Destination

class MichoteCommand(cmd.Cmd):
    """Class definition for the command intepreter.

    Inherits from the inbuilt ``cmd`` module. The inbuilt ``cmd`` module
    contains the necessary tools (inherited attributes) to setup a custom
    line-oriented command intepreter.
    """

    prompt = '\n(michote) => '

    __classes = {
        'BaseModel': BaseModel, 'Customer': Customer,
        'BookedTrips': BookedTrips, 'Company': Company,
        'Vehicle': Vehicle, 'Admin': Admin,
        'Prices': Prices, 'Destination': Destination
    }

    __types = {
        'age': int, 'no_of_seats': int,
        'price_per_ticket': int, 'total_amount': int,
        'latitude': float, 'longitude': float
    }


    # --------------- Utility Functions -------------------------- #

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
              ' commands.')
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

    def help_show(self):
        """Print info on ``show`` command to user"""
        print('Use this command to print an object based on class name and ' +
              'object id')
        self.__usage('show')

    def help_create(self):
        """Print info on ``create`` command to user"""
        print('Use this command to create a new object of a class.')
        self.__usage('create')

    def help_destroy(self):
        """Print info on ``destroy`` command to user"""
        print('Use this command to delete an object based on class name and ' +
              'object id')
        self.__usage('destroy')

    def help_all(self):
        """Print info on ``all`` command to user"""
        print('Use this command to print an object based on class name and ' +
              'object id. ')
        self.__usage('all')

    def help_update(self):
        """Print info on ``update`` command to user"""
        print('Use this command to update an object based on class name and ' +
              'object id, with attribute name(s) and value(s)')
        self.__usage('update')

    def __avail_classes(self):
        """Prints the valid classes that can be used with commands"""
        print('The following classes are available to use: ')
        for key in MichoteCommand.__classes.keys():
            print(f'\t{MichoteCommand.__classes[key].__name__}')

    def __usage(self, command):
        """Prints the correct usage for each command to the user"""
        print('')
        if command == 'help':
            print('usage:\n\thelp <command>')
        elif command == 'quit':
            print('usage:\n\tquit\n(command takes no arguments)')
        elif command == 'EOF':
            print('usage:\n\t<EOF character>\n\t(Ctrl+D for linux os)')
        elif command == 'create':
            print('usage:\n\tcreate <class_name>')
        elif command == 'show':
            print('usage:\n\tshow <class_name> <object_id>')
        elif command == 'destroy':
            print('usage:\n\tdestroy <class_name> <object_id>')
        elif command == 'update':
            print('usages:\n\t1. update <class_name> <object_id> <att_name>' +
                  ' <att_value>.\n\t2. update <class_name> <object_id>' +
                  ' {"<att_name>": "<att_value>", ...}')
        elif command == 'all':
            print('usage:\n\tall [<class_name>]\n\tClass name is optional')

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
            print(json.dumps(storage._FileStorage__objects[f'{class_name}.{object_id}'].to_dict(),
                            indent = 1))
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
            print(f'Object of ID {object_id} belonging to' +
                  f' {class_name} class deleted.')
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
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    objs_as_string.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                objs_as_string.append(str(v))

        print(json.dumps(objs_as_string, indent = 1))

    def do_update(self, args):
        """Method used to update an object."""
        class_name = object_id = att_name = att_value = kwargs = ''

        # First, extract the class name and check if its valid
        args = args.partition(' ')
        if args[0]:
            class_name = args[0]
        else:
            print('** class name missing **')
            self.__usage('update')
            return
        if class_name not in MichoteCommand.__classes:
            print('** That class name doesn\'t exist **')
            self.__avail_classes()
            return

        # Next extract object id and check if valid
        args = args[2].partition(' ')
        if args[0]:
            object_id = args[0]
        else:
            print('** instance id missing **')
            self.__usage('update')
            return

        # class name and object id extracted. Check if object exists
        if f'{class_name}.{object_id}' not in storage.all():
            print(f'** Object of class {class_name} and id {object_id}' +
                  'doesn\'t exist **')
            return

        # Now, check if attributes to be added have been passed as *args or
        # **kwargs
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            # if this line is reached, it is **kwargs.
            # Store all the key/values in a list
            kwargs = eval(args[2])
            args = []
            for key, value in kwargs.items():
                args.append(key)
                args.append(value)
        else:
            # if this line is reached, it is *args
            args = args[2]

            # First, obtain attribute name.
            # If it is quoted, slice string to get name
            if args and args[2] == '\"':
                end_quote = args.find('\"', 1)
                att_name = args[1:end_quote]
                args = args[end_quote + 1:]

            args = args.partition(' ')

            # if attribute name is not set by now, it wasn't quoted. It should
            # be in the 0th index of args
            if not att_name and args[0] != ' ':
                att_name = args[0]

            # By this point, we have attribute name. Let's extract attribute
            # value. Again, it may be quoted or not
            if args[2] and args[2][0] == '\"':
                att_value = args[2][1:args[2].find('\"', 1)]

            if not att_value and args[2]:
                att_value = args[2].partition(' ')[0]

            # Attribute name and value extracted by this point. Store in a list
            # just like in **kwargs case
            args = [att_name, att_value]

        # We have all attribute name(s) and value(s) in a list. Next step is to
        # load the object, update it then save it
        obj_to_update = storage.all()[f'{class_name}.{object_id}']

        for i, att_name in enumerate(args):
            if i % 2 == 0:
                att_value = args[i + 1]
                if not att_name:
                    print('** attribute name missing **')
                    self.__usage('update')
                    return
                if not att_value:
                    print('** attribute value missing **')
                    self.__usage('update')
                    return
                if att_name in MichoteCommand.__types:
                    att_value = MichoteCommand.__types[att_name](att_value)

                # update the object
                obj_to_update.__dict__.update({att_name: att_value})

        # save changes to file
        obj_to_update.save()
        print('Object Updated !')
        print(json.dumps(obj_to_update.to_dict(), indent = 1))



if __name__ == '__main__':
    michote_intro = f'Michote, Starehe yako.\n\nWelcome to michote, an online' \
    ' ticket booking service.\nYou are using the command line' \
    ' interpreter, best used for debugging and dev work.' \
    '\nType "help" for a list of commands.'

    MichoteCommand().cmdloop(intro=michote_intro)
