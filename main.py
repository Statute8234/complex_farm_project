import random
from ursina import *

def update():
    # update text
    money_text.text = 'money ${:.2f}'.format(money)
    food_text.text = 'food: {}'.format(food)
    objects_text.text = 'objects: {}'.format(objects)
    eggs_text.text = 'eggs: {}'.format(eggs)
    meat_text.text = 'meat: {}'.format(meat)

app = Ursina()
# window
window.fullscreen = True
window.fps_counter.enabled = False
window.cog_button.enabled = False

# bord
Bord = Entity(model = 'quad',scale = (15,1),color = color.black,y = 4)
money = 100
money_text = Text(text = '',y = 0.47,x = -0.85)
food = 0
food_text = Text(text = '',y = 0.47,x = -0.65)
objects = 0
objects_text = Text(text = '',y = 0.47,x = -0.48)
eggs = 0
eggs_text = Text(text = '',y = 0.47,x = -0.28)
meat = 0
meat_text = Text(text = '',y = 0.47,x = -0.11)

# Shop products icons
shop_inv = []
class Shop_products(Button):
    def __init__(self, position=(0, 0, 0),cost = 0.00,text = ''):
        super().__init__()
        # make the buttons
        self.parent = menu
        self.position = position
        self.scale = 0.1
        self.model = 'quad'
        self.cost = cost
        self.text = text + '\n${:.2f}'.format(cost)
        self.text_origin = (0, 0, -1)
        self.text_color = color.brown
        self.color = color.random_color()
        self.highlight_color = self.color
        self.tooltip = Tooltip(text = text + '\n${:.2f}'.format(cost))

    # activate the buttons
    def input(self, key):
        global money, food, objects,eggs,meat,storage_used
        if self.hovered:
            if key == 'left mouse down':
                # if you can afford it and have storage
                if money >= self.cost and storage_used < max_storage:
                    money -= self.cost
                    if 'food' in self.text:
                        food += 50
                        storage_list.append('food')
                    elif 'objects' in self.text:
                        objects += 1
                        storage_list.append('objects')
                    elif 'eggs' in self.text:
                        eggs += 12
                        storage_list.append('egg')
                    elif 'meat' in self.text:
                        meat += 1
                        storage_list.append('meat')
                    else:
                        money += self.cost
                    destroy(self)

# shop
class Shop(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__()
        # make the shop
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'quad'
        self.highlight_color = color.lime
        self.color = color.red
        self.text = 'Shop'
        self.text_origin = (0,0,-0.5)
        self.text_color = color.black

    def input(self, key):
        global shop_inv
        if self.hovered:
            if key == 'left mouse down':
                # shop menu
                T1 = Text(text = 'Shop',color = color.black,y = 0.4,scale = 3,x = -0.1,parent = menu)
                menu.color = color.white

                # food
                for x in range(7):
                    shop_products = Shop_products(position=(0.44 - x / 7, 0.2), cost=round(random.uniform(0.01, 99), 2),
                                                  text='food')
                    shop_products.text_origin = (-0.3, 0)
                    shop_inv.append(shop_products)
                    shop_products.icon = 'bag'
                # objects
                for x in range(7):
                    shop_products = Shop_products(position=(0.44 - x / 7, 0), cost=round(random.uniform(0.01, 99), 2),
                                                  text='objects')
                    shop_inv.append(shop_products)
                    shop_products.icon = 'orb'
                # eggs
                for x in range(7):
                    shop_products = Shop_products(position=(0.44 - x / 7, -0.2),
                                                  cost=round(random.uniform(0.01, 99), 2), text='eggs')
                    shop_products.text_origin = (-0.2, 0)
                    shop_inv.append(shop_products)
                    shop_products.icon = 'eggs.png'
                # meat
                for x in range(7):
                    shop_products = Shop_products(position=(0.44 - x / 7, -0.4),
                                                  cost=round(random.uniform(0.01, 99), 2), text='meat')
                    shop_products.text_origin = (-0.2, 0)
                    shop_inv.append(shop_products)
                    shop_products.icon = 'meat.png'

                # exit button
                def Remove():
                    global shop_inv
                    for x in range(len(shop_inv)):
                        for entity in shop_inv:
                            shop_inv.remove(entity)
                            destroy(entity)
                    menu.color = color.clear
                    destroy(T1)
                    destroy(exit_shop)

                exit_shop = Button(model='circle', parent=menu, color=color.red, scale=0.1,text = 'exit',y = 0.4,x = 0.4)
                exit_shop.on_click = Remove

# storage
storage_used = 0
max_storage = 50
storage_list = []
class Storage(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'quad'
        self.highlight_color = color.lime
        self.color = color.orange
        self.text = 'storge\n({}/{})'.format(storage_used,max_storage)
        self.text_color = color.black

    def update(self):
        global storage_used,storage_list,minute,food, objects,eggs,meat
        storage_used = len(storage_list)
        self.text = 'storge\n({}/{})'.format(storage_used,max_storage)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                menu.color = color.white
                T1 = Text(text = 'Storage',color = color.black,y = 0.4,scale = 3,x = -0.15,parent = menu)

                # what is in storage
                T2 = Text(text = 'left click to activate | right click to sell',color = color.dark_gray,y = 0.3,scale = 1,x = -0.25,parent = menu)

                food_held = Button(model='quad', parent=menu, scale=0.15, color=color.green, x=-0.3,text='food: {}'.format(food))
                objects_held = Button(model='quad', parent=menu, scale=0.15, color=color.brown, x=-0.1,text='objects: {}'.format(objects))
                eggs_held = Button(model='quad', parent=menu, scale=0.15, color=color.gold, x= 0.1, text='eggs: {}'.format(eggs))
                meat_held = Button(model='quad', parent=menu, scale=0.15, color=color.red, x= 0.3, text='meat: {}'.format(meat))
                # exit
                def Remove():
                    menu.color = color.clear
                    destroy(T1)
                    destroy(T2)
                    destroy(exit_shop)
                    destroy(food_held)
                    destroy(objects_held)
                    destroy(eggs_held)
                    destroy(meat_held)

                exit_shop = Button(model='circle', parent=menu, color=color.red, scale=0.1,text = 'exit',y = 0.4,x = 0.4)
                exit_shop.on_click = Remove

# egg holder
amount = 0
max_amount = 50
class Incubator(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'quad'
        self.highlight_color = color.lime
        self.color = color.yellow
        self.text = 'incubator\n({}/{})'.format(amount,max_amount)
        self.text_color = color.black

    def update(self):
        global amount,max_amount
        self.text = 'incubator\n({}/{})'.format(amount,max_amount)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                menu.color = color.white
                T1 = Text(text = 'Incubator',color = color.black,y = 0.4,scale = 3,x = -0.15,parent = menu)

                # exit
                def Remove():
                    menu.color = color.clear
                    destroy(T1)
                    destroy(exit_shop)

                exit_shop = Button(model='circle', parent=menu, color=color.red, scale=0.1,text = 'exit',y = 0.4,x = 0.4)
                exit_shop.on_click = Remove

# body
menu = Entity(model = 'quad',parent = camera.ui,color = color.clear)
storage = Storage(position = (6,1))
incubator = Incubator(position = (6,-0.5))
shop = Shop(position = (6,2.5))

if __name__ == '__main__':
    app.run()
