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


def parse(line):
    curly_braces = re.search(r"\{(.*?)\}", line)
    brackets = re.search(r"\[(.*?)\]", line)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(line)]
        else:
            lexer = split(line[:brackets.span()[0]])
            ret_list = [i.strip(",") for i in lexer]
            ret_list.append(brackets.group())
            return ret_list
    else:
        lexer = split(line[:curly_braces.span()[0]])
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
                command = [arg[1][:match.span()[0]], match.group()[1:-1]]
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
        create_arg = parse(line)
        if len(create_arg) == 0:
            print("** class name missing **")
        else:
            class_name = create_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                print(eval(class_name)().id)
                storage.save()

    def do_show(self, line):
        """Display/show an instance
        Usage: destroy <class> <id>
        """
        show_arg = parse(line)
        objects = storage.all()
        if len(show_arg) == 0:
            print("** class name missing **")
        else:
            class_name = show_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            elif len(show_arg) == 1:
                print("** instance id missing **")
            elif "{}.{}".format(class_name, show_arg[1]) not in objects:
                print("** no instance found **")
            else:
                print(objects["{}.{}".format(class_name, show_arg[1])])

    def do_destroy(self, line):
        """Delete an instance
        Usage: destroy <class> <id>
        """
        destroy_arg = parse(line)
        objects = storage.all()
        if len(destroy_arg) == 0:
            print("** class name missing **")
        else:
            class_name = destroy_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            elif len(destroy_arg) == 1:
                print("** instance id missing **")
            elif "{}.{}".format(class_name, destroy_arg[1]) not in objects:
                print("** no instance found **")
            else:
                del objects["{}.{}".format(class_name, destroy_arg[1])]
                storage.save()

    def do_all(self, line):
        """print a string represeantation of all instance
         Usage: all <class name>
        """
        all_arg = parse(line)
        objects = storage.all()

        if len(all_arg) == 0:
            new_list = []
            for key in objects:
                new_list.append(str(objects[key]))
            print(new_list)
        else:
            class_name = all_arg[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                new_list = []
                for obj in storage.all().values():
                    if len(all_arg) > 0 and class_name == obj.__class__.__name__:
                        new_list.append(obj.__str__())
                    elif len(all_arg) == 0:
                        new_list.append(obj.__str__())
                print(new_list)

    def do_update(self, line):
        """Update an instance
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        objects = storage.all()
        update_arg = parse(line)
        class_name = update_arg[0]

        if len(update_arg) == 0:
            print("** class name missing **")
            return False
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return False
        if len(update_arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(class_name, update_arg[1]) not in objects.keys():
            print("** no instance found **")
            return False
        if len(update_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(update_arg) == 3:
            try:
                type(eval(update_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(update_arg) == 4:
            obj = objects["{}.{}".format(class_name, update_arg[1])]
            if update_arg[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[update_arg[2]])
                obj.__dict__[update_arg[2]] = val_type(update_arg[3])
            else:
                obj.__dict__[update_arg[2]] = update_arg[3]
        elif type(eval(update_arg[2])) == dict:
            obj = objects["{}.{}".format(class_name, update_arg[1])]
            for key, value in eval(update_arg[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in
                        {str, int, float}):
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()

    def do_count(self, line):
        """Retrieve the number of instance of a given class
        Usage: count <class> or <class.count>()
        """
        count_arg = parse(line)
        count = 0
        for obj in storage.all().values():
            if count_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
