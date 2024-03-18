#!/usr/bin/python3
""" Define the console module """
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """ Defines HBNBCommand class """

    classes = {"BaseModel": BaseModel, "User": User, 'Amenity': Amenity,
               'City': City, 'State': State, 'Place': Place,
               'Review': Review}

    prompt = "(hbnb) "

    def emptyline(self):
        """ called when an empty line is entered in response to the prompt """
        pass

    def do_EOF(self, line):
        """EOF command to exit the program (Ctrl + D)"""

        return True

    def postloop(self):
        """Hook method executed once when the cmdloop() method
            is about to return
        """
        if not sys.stdin.isatty():
            print()

    def do_quit(self, s):
        """Quit command to exit the program"""
        return True

    @staticmethod
    def is_int(n):
        """ checks if integer"""
        try:
            int(n)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def do_create(self, arg):
        """Usage: create <class>
        Creates a new instance of the given class and prints its id """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        else:
            cls = type(self).classes.get(args[0])
            if cls is not None:
                kwargs = {}
                for p in args[1:]:
                    k, v = p.split("=")
                    if v.startswith('"') and v.endswith('"'):
                        if ' ' in v:
                            continue
                        v = v[1:-1]
                        ln = len(v)
                        i = v.find('"')
                        while (i != -1):
                            if v[i - 1] != '\\':
                                break
                            if (i + 1) < ln:
                                i = v.find('"', i + 1)
                        if i != -1:
                            continue
                        v = v.replace('_', ' ')
                        kwargs[k] = v
                    elif type(self).is_int(v):
                        kwargs[k] = int(v)
                    elif type(self).is_float(v):
                        kwargs[k] = float(v)
                    else:
                        continue
                obj = cls(**kwargs)
                obj.save()
                print(obj.id)
            else:
                print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""

        ln = len(arg.split())
        my_list = []
        if ln == 0:
            obj_dict = storage.all().values()
            my_list = [str(v) for v in obj_dict]
            print(my_list)
        elif ln == 1:
            cls = type(self).classes.get(arg)
            if cls is not None:
                obj_dict = storage.all(cls).values()
                my_list = [str(v) for v in obj_dict]
                print(my_list)
            else:
                print("** class doesn't exist **")

    def validate(self, arg):
        """Validates class and id existence"""

        args = arg.split()
        ln = len(args)

        if ln == 0:
            print("** class name missing **")
        elif ln == 1:
            cls = type(self).classes.get(arg)
            if cls is None:
                print("** class doesn't exist **")

            print("** instance id missing **")
        elif ln >= 2:
            cls = type(self).classes.get(args[0])
            if cls is None:
                print("** class doesn't exist **")
            else:
                obj_dict = storage.all().values()
                for obj in obj_dict:
                    if isinstance(obj, cls) and obj.id == args[1]:
                        return obj
                print("** no instance found **")
        return False

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        obj = self.validate(arg)
        if obj:
            print(str(obj))

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        obj = self.validate(args)
        obj_dict = storage.all()
        for k, v in obj_dict.items():
            if v is obj:
                del obj_dict[k]
                storage.save()
                break

    def do_update(self, args):
        """Updates an instance based on the class name and id
        Usage: update <class name> <id> <attribute name> "<attribute value>"""

        obj = self.validate(args)
        args_list = args.split(maxsplit=3)
        ln = len(args_list)
        if ln == 2:
            print("** attribute name missing **")
        elif ln == 3:
            print("** value missing **")
        elif ln >= 4 and obj:
            try:
                attr_type = type(getattr(obj, args_list[2]))
                if attr_type is str and args_list[3].startswith('"'):
                    ls = args_list[3].split('"')
                    setattr(obj, args_list[2], attr_type(ls[1]))
                else:
                    ls = args_list[3].split()
                    setattr(obj, args_list[2], attr_type(ls[0]))
            except (AttributeError):
                v = args_list[3]
                try:
                    ls = v.split()
                    v = int(ls[0])
                except (TypeError, ValueError):
                    try:
                        v = float(ls[0])
                    except (TypeError, ValueError):
                        if v.startswith('"'):
                            ls = v.split('"')
                            v = ls[1]
                        else:
                            ls = v.split()
                            v = ls[0]
                finally:
                    setattr(obj, args_list[2], v)
            finally:
                storage.save()

    def count(self, arg):
        """Retrieves the number of instances of a class"""

        cls = type(self).classes.get(arg)
        if cls is not None:
            obj_dict = storage.all().values()
            c = 0
            for v in obj_dict:
                if type(v) is cls:
                    c += 1
            return c
        else:
            print("** class doesn't exist **")

    def update_from_dict(self, args):
        """Update an instance based on his ID with a dictionary"""

        obj = self.validate(args)
        args_list = args.split(maxsplit=2)
        my_dict = eval(args_list[2])
        if len(my_dict) == 0:
            print("** attribute name missing **")
            print("** value missing **")
        else:
            for k, v in my_dict.items():
                setattr(obj, k, v)
                storage.save()

    def default(self, line):
        """Handles unrecognized methods"""

        funcs = {"all": self.do_all, "count": self.count, "show": self.do_show,
                 "destroy": self.do_destroy, "update": self.do_update}

        ls = line.split('.', maxsplit=1)
        cls = ls[0]
        ls2 = ls[1].split('(')
        do = ls2[0]
        args = ls2[1].split(')')

        if args[0] != '':
            my_ls = args[0].split(',', maxsplit=1)
            if len(my_ls) == 2:
                if isinstance(eval(my_ls[1]), dict):
                    arg = cls + " " + my_ls[0].strip('"') + " " + my_ls[1]
                    self.update_from_dict(arg)
                    return
            t_ls = args[0].replace(",", " ").split()
            if len(t_ls) >= 2:
                t_ls[0] = t_ls[0].strip('"')
                t_ls[1] = t_ls[1].strip('"')
                args[0] = ' '.join(t_ls)
                arg = cls + " " + args[0]
            else:
                arg = cls + " " + t_ls[0].strip('"')
        else:
            arg = cls

        for k, v in funcs.items():
            if k == do:
                if do == "count":
                    c = v(arg)
                    print(c)
                else:
                    v(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
