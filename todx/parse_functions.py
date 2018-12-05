from . import fabric
from . import searcher
from . import settings as stg
from .yesnoquery import query_yes_no

def parse_modifier(newtodo, arg):
    """
    Parse a sepecial modifier argument
    Current mod:
        +   add
    """
    if arg[0] == '+':
        newtodo.add_tag(arg[1:])
    # elif arg[1] == '':


def parse_add(twrap, args):
    """
    Parse the add command
     - If no arguments prints help for add
     - If 1 argument creates new todo with argument as content
     - If more arguments joins arguments into content and seperates modifiers
    """

    if len(args) == 1:
        print("Please provide at least one argument: content tags[optional]  status[optional]")
    
    elif len(args) == 2:
        fabric.add_todo(twrap, args[1])
        print("Added todo + ", args[1])
    
    else:
        newtodo = fabric.Todo()
        for arg in args[1:]:
            if fabric.check_modifier(arg) is False:
                newtodo.content += arg + ' '
            else:
                parse_modifier(newtodo, arg)
        twrap.tlist.append(newtodo)
        print('Added todo: ', newtodo)


def parse_mark(twrap, args):
    """
    Parse mark command
    """
    if len(args) == 1:
        if len(twrap) > 0:
            fabric.index_view(twrap)
            print()
            index = int(input("Which todo you want to mark: "))
            if index < len(twrap):
                twrap.tlist[index].status = input("What is your new status: ")
            else:
                print('Too large an Index, You have.')
        else:
            print("No todo list found")


def parse_view(twrap, args):
    """
    Parse view command
     - If no other arguments are passed view every todo
     - if an argument is passed view todos tagged as the argument
    """
    if len(args) == 1:
        fabric.view_list(twrap)
        return

    if args[1][0] == '+':
        args[1] = args[1][1:]

    index_list = searcher.find_index_tag(args[1], twrap.tlist)

    if len(index_list) == 0:
        print("No todos with tag " + stg.tag_decorator(args[1]) + " found!")
        return
    
    print(stg.tag_decorator(args[1]))
    for index in index_list[1:]:
        print(twrap.tlist[index].without_tags())


def parse_task(twrap, args):
    """
    Parse task command
     - If no other arguments are passed view every undone todo
     - if an argument is passed view undone todos tagged as the argument
    """
    if len(args) == 1:
        fabric.view_list(twrap, only_left=True)
        return

    if args[1][0] == '+':
        args[1] = args[1][1:]

    index_list = searcher.find_index_tag(args[1], twrap.tlist)
    
    if len(index_list) == 0:
        print("No todos with tag " + stg.tag_decorator(args[1]) + " found!")
        return
    
    print(stg.tag_decorator(args[1]))
    for index in index_list[1:]:
        if twrap.tlist[index].status not in stg.done_markers:
            print(twrap.tlist[index].without_tags())


def parse_del(twrap, args):
    """
    Parse del command
    """
    if len(args) == 1:
        if len(twrap) > 0:
            fabric.index_view(twrap)
            print()
            index = int(input("Which todo you want to delete: "))
            if index < len(twrap):
                if query_yes_no('Are you sure buddy?') is True:
                    del twrap.tlist[index]
            else:
                print('Too large an Index, You have.')
        else:
            print("No todo list found")
