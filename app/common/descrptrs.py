# 3. Реализовать дескриптор для класса серверного сокета, а в нем — проверку номера порта.
# Это должно быть целое число (>=0).
# Значение порта по умолчанию равняется 7777.
# Дескриптор надо создать в отдельном классе.
# Его экземпляр добавить в пределах класса серверного сокета.
# Номер порта передается в экземпляр дескриптора при запуске сервера.
class Port_num_check:

    def __init__(self, port_num):
        self.port_num = port_num

    def __get__(self, instance, owner):
        return instance.__dict__[self.port_num]

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Port number should be greater than or equal 0")
        instance.__dict__[self.port_num] = value
