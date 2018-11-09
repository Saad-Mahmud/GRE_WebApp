import abc


from App_Main.Backend.App import db

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "{}: $ {}".format(self.name, self.price)

class MenuIterator:
    def __init__(self, items):
        self.indx = 0
        self.items = items

    def has_next(self):
        return False if self.indx >= len(self.items) else True

    def next(self):
        item = self.items[self.indx]
        self.indx += 1
        return item

    def remove(self):
        return self.items.pop()

class Menu:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def iterator(self):
        return MenuIterator(self.items)
    #
    # def retArr(self):
    #     return self.items

class Iteration:
    def IteratingCountry(self):
        collection = db['country']
        arr = []
        cursor = collection.find({})
        menu = Menu()
        for i in cursor:
            menu.add(i['country_name'])


        #print("Displaying Menu:")
        iterator = menu.iterator()

        while iterator.has_next():
            item = iterator.next()
            arr.append(item)
            #print(item)

        return arr


#
# class Iteration:
#     collection = db['country']
#     cursor = collection.find({})
#     menu = Menu()
#     for i in cursor:
#         menu.add(i['country_name'])