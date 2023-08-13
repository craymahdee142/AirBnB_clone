#!/usr/bin/python3
"""Defines Hbnb command line interpreter"""
import cmd
import shlex
import models
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity


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
        print("*** Unknown syntax: {}".format(line))

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
                print("** value missing **")
            else:
                key_find = class_name + '.' + update_arg[1]
                obj = objects.get(key_find, None)

                if not obj:
                    print("** no instance found **")
                    return

                setattr(obj, update_arg[2], update_arg[3].strip('"'))
                models.storage.save()

    def check_class_name(self, name=""):
        """check if stdin user typed class name and id"""
        if len(name) == 0:
            print("** class name missing **")
            return False
        else:
            return True

    def check_class_id(self, name=""):
        """Check lass id"""
        if len(name.split(" ")) == 1:
            print("** instance id missing **")
        else:
            return True

    def found_class_name(self, name=""):
        """Find the name of class"""
        if self.check_class_name(name):
            args = shlex.split(name)
            if class_name in self.valid_classes:
                if self.check_class_name_id(name):
                    key = args[0] + '.' + args[1]
                    return key
                else:
                    print("** class doesn't exist **")
                    return None


if __name__ == "__main__":
    HBNBCommand().cmdloop()
