#!/usr/bin/python3
"""Defines Hbnb command line interpreter"""
import cmd
from shlex import split
import models
import re
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            ret_list = [i.strip(",") for i in lexer]
            ret_list.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        ret_list = [i.strip(",") for i in lexer]
        ret_list.append(curly_braces.group())
        return ret_list


class HBNBCommand(cmd.Cmd):
    """Defines HBnB Command line interpreter

    Attributes:
        prompt (str): custom command prompt
    """
    prompt = "(Hbnb) "
    valid_classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line"""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            arg = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg[1])
            if match is not None:
                command = [arg[1][match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program"""
        print("")
        return True

    def do_create(self, line):
        """create new class instance and print id
        Usage: create <class>
        """
        create_arg = line.split()
        if len(create_arg) == 0:
            print("** class name missing **")
        else:
            class_name = create_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                new_creation = eval(class_name + "()")
                models.storage.save()
                print(new_creation.id)

    def do_show(self, line):
        """Display/show an instance
        Usage: destroy <class> <id>
        """
        show_arg = line.split()
        if len(show_arg) == 0:
            print("** class name missing **")
        else:
            class_name = show_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            elif len(show_arg) == 1:
                print("** instance id missing **")
            else:
                obj = models.storage.all()
                key_value = class_name + '.' + show_arg[1]
                if key_value in obj:
                    print(obj[key_value])
                else:
                    print("** no instance found **")

    def do_destroy(self, line):
        """Delete an instance
        Usage: destroy <class> <id>
        """
        destroy_arg = line.split()
        objects = models.storage.all()
        if len(destroy_arg) == 0:
            print("** class name missing **")
        else:
            class_name = destroy_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            elif len(destroy_arg) == 1:
                print("** instance id missing **")
            else:
                key_find = class_name + '.' + destroy_arg[1]
                if key_find in objects.keys():
                    objects.pop(key_find, None)
                    models.storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, line):
        """print a string represeantation of all instance
         Usage: all <class name>
        """
        all_arg = line.split()
        objects = models.storage.all()

        if len(all_arg) == 0:
            new_list = [obj.__str__() for obj in objects.values()]
            print(new_list)
        else:
            class_name = all_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                new_list = [obj.__str__() for obj in objects.values()
                            if obj.__class__.__name__ == class_name]
                print(new_list)

    def do_update(self, line):
        """Update an instance
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        objects = models.storage.all()
        update_arg = line.split(" ")

        if len(update_arg) == 0:
            print("** class name missing **")
        else:
            class_name = update_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            elif len(update_arg) == 1:
                print("** instance id missing **")
            elif len(update_arg) == 2:
                print("** attribute name missing **")
            elif len(update_arg) == 3:
               #    try:
               #    type(eval(update_arg[2])) != dict
               #    except NameError:"""
                print("** value missing **")
            else:
                key_find = class_name + '.' + update_arg[1]
                obj = objects.get(key_find, None)
                if not obj:
                    print("** no instance found **")

                setattr(obj, update_arg[2], update_arg[3].strip('"'))
                models.storage.save()


    def do_count(self, line):
        """Retrieve the number of instance of a given class
        Usage: count <class> or <class.count>()
        """
        count_arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if count_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
