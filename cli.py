#!/usr/bin/python3

"""This module contains the definition of the command line interpreter (cli)
for michote.

The main purpose of the cli is to provide a shell-like interface for
object manipulation useful for development and debugging.
"""

import cmd

class MichoteCommand(cmd.Cmd):
    """Class definition for the command intepreter.

    Inherits from the inbuilt ``cmd`` module. The inbuilt ``cmd`` module
    contains the necessary tools (inherited attributes) to setup a custom
    line-oriented command intepreter.
    """

    prompt = '(michote) '

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
        print('useage: \n\thelp <command>')

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
        print('useage: \n\tquit')

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
        print('useage: \n\t <EOF character>')

    # ------------- Core Functions ---------------------------------- #


if __name__ == '__main__':
    michote_intro = f'Michote, Starehe yako.\n\nWelcome to michote, an online' \
    ' ticket booking service.\nYou are using the command line' \
    ' interpreter, best used for debugging and dev work.' \
    '\nType "help" for a list of commands.'

    MichoteCommand().cmdloop(intro=michote_intro)
