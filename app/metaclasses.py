import dis


# Метакласс для проверки соответствия сервера:
from pprint import pprint


class ServerMaker(type):
    def __init__(cls, clsname, bases, clsdict):

        methods = []
        methods_2 = []
        attrs = []
        for func in clsdict:

            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)

        if 'connect' in methods:
            raise TypeError('connect method in client socket')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('it is not tcp')
        # Обязательно вызываем конструктор предка:
        super().__init__(clsname, bases, clsdict)



class ClientMaker(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':

                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError(command.__str__(), 'command in server')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)
