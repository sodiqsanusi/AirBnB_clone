#!/usr/bin/python3
"""Entry point for the command interpreter."""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class - Command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "Ade$ "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def default(self, arg):
        """
        Default method to handle <class name>.count(), <class name>.show(<id>),
        <class name>.destroy(<id>), and
        <class name>.update(<id>, <dictionary representation>)
        """
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel, saves it (to the JSON file)
        and prints the id.
        Usage: create <class_name>
        """
        argl = parse(arg)
        if not argl:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            instance = eval(argl[0])()
            print(instance.id)
            storage.save()

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the
        class name and id.
        Usage: show <class_name> <id>
        """
        argl = parse(arg)
        obj_dict = storage.all()
        if len(argl) < 2:
            print(
                "** class name missing **"
                if not argl
                else "** instance id missing **"
            )
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(argl[0], argl[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Usage: destroy <class_name> <id>
        """
        argl = parse(arg)
        obj_dict = storage.all()
        if len(argl) < 2:
            print(
                "** class name missing **"
                if not argl
                else "** instance id missing **"
            )
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(argl[0], argl[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not
        on the class name.
        Usage: all [class_name]
        """
        argl = parse(arg)
        if argl and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = [
                str(obj)
                for obj in storage.all().values()
                if not argl or obj.__class__.__name__ == argl[0]
            ]
            print(obj_list)

    def do_count(self, arg):
        """
        Retrieve the number of instances of a given class.
        Usage: count <class> or <class>.count()
        """
        argl = parse(arg)
        count = sum(
            1
            for obj in storage.all().values()
            if obj.__class__.__name__ == argl[0]
        )
        print(count)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Usage: update <class_name> <id> <attribute name> "<attribute value>"
        """
        argl = parse(arg)
        obj_dict = storage.all()

        if len(argl) < 2:
            print(
                "** class name missing **"
                if not argl
                else "** instance id missing **"
            )
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(argl) < 3:
            print("** attribute name missing **")
            return False
        if len(argl) < 4 and type(eval(argl[2])) != dict:
            print("** value missing **")
            return False

        obj = obj_dict["{}.{}".format(argl[0], argl[1])]
        if len(argl) == 4:
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys()
                        and type(obj.__class__.__dict__[k])
                        in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
