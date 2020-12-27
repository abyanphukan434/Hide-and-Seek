#
# Intro CS Group Project
# Beta-name : mail-bomber
# Group members: Koh Terai & Maverick Alzate
#

# module used for battle system
import random
import time
#modules for pygame
import pygame
from pygame.locals import *
from sys import exit


###############################################################################
############################---Player---Class---###############################
###############################################################################

class Player(object):
    def __init__(self, location, inventory, health_bar):
        self.location = location
        self.inventory = set([inventory])
        self.health_bar = health_bar
        self.current_health = self.health_bar
        self.exp_bar = 0
        self.exp_needed = 100
        self.level = 1
        self.dodge = False
        self.alive = True
        # Error Handler
        if not isinstance(location, Square):
            raise ValueError
        if not isinstance(health_bar, int):
            raise ValueError

    #EXP system implemented 
    def exp_gain(self, number):
        # number == amount of exp earned
        #remainder == ensures exp is not lost when player levels up
        remainder = 0
        #when exp gain does not result in level up
        if self.level == 1 and self.exp_bar < self.exp_needed:
            self.exp_bar += number
        elif self.level == 2 and self.exp_bar < self.exp_needed:
            self.exp_bar += number
        elif self.level == 3 and self.exp_bar < self.exp_needed:
            self.exp_bar += number
        #when exp gain results in level up
        if self.level == 1 and self.exp_bar >= 100:
            self.level += 1
            self.health_bar += 5
            self.current_health = self.health_bar 
            remainder = (self.exp_bar - 100)
            self.exp_bar = 0
            self.exp_bar += (number + remainder)
            self.exp_needed = 200
        elif self.level == 2 and self.exp_bar >= 200:
            self.level += 1
            self.health_bar += 5
            self.current_health = self.health_bar
            remainder = (self.exp_bar - 200)
            self.exp_bar = 0 
            self.exp_bar += (number + remainder)
            self.exp_needed = 300
        elif self.level == 3 and self.exp_bar >= 300:
            self.level += 1 
            self.health_bar += 5
            self.current_health = self.health_bar
            remainder = (self.exp_bar - 300)
            self.exp_bar = 0 
            self.exp_bar += (number + remainder)
            self.exp_needed = 'fullBar'
        if self.level == 4:
            pass

    def attack(self, enemy):
        # Method used in combat function in main script
        # enemy may be any enemy instance

        if not isinstance(enemy, Subenemy1) and not isinstance(enemy, Subenemy2) \
        and not isinstance(enemy, Subenemy3) and not isinstance(enemy, Subenemy4)\
        and not isinstance(enemy, Subenemy5):
            raise ValueError

        # dodge member of each character allows them to avoid a hit
        if enemy.dodge == True:
            #resets dodge value to avoid infinite dodge
            enemy.dodge = False

        # if-suites reflect perks of leveling up
        elif self.level == 1:
            hit = random.randint(0,100)
            if hit <= 33:
                enemy.current_health -= 1
                return 1

        elif self.level == 2:
            hit = random.randint(0,100)
            if hit <= 50:
                enemy.current_health -= 2
                return 2

        elif self.level == 3:
            hit = random.randint(0,100)
            if hit <= 67:
                enemy.current_health -= 3
                return 3

        elif self.level == 4:
            hit = random.randint(0,100)
            if hit <= 80:
                enemy.current_health -= 3
                return 3
        return 0

    # Dodging feature
    def dodging(self):
        # nomenclature variance to avoid 'boolean' TypeErrors
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 20:
            self.dodge = True
          
    # movement (checks for location before applying movement)
    def move_up(self):
        if isinstance(self.location.n(), Square):
            self.location = self.location.n()
        else:
            pass

    def move_right(self):
        if isinstance(self.location.e(), Square):
            self.location = self.location.e()
        else:
            pass

    def move_down(self):
        if isinstance(self.location.s(), Square):
            self.location = self.location.s()
        else:
            pass

    def move_left(self):
        if isinstance(self.location.w(), Square):
            self.location = self.location.w()
        else:
            pass

    # Picking up and dropping items
    def pick_up_item(self):
        # once respective House instance 'blows up', player 
        # can pick up next bomb in sequence

        if isinstance(self.location, House) and not self.location.intact\
        and len(self.location.secret_inventory) != 0:
            self.inventory.add(self.location.secret_inventory.pop())

        elif len(self.location.inventory) >= 1:
            self.inventory.add(self.location.inventory.pop())

        elif len(self.location.inventory) == 0:
            pass

    def drop_item(self):
        if isinstance(self.location, House) and len(self.inventory) != 0\
        and self.location.intact:
            dropped_item = self.inventory.pop()
            self.location.inventory.add(dropped_item)
            return 1
        else:
            return 0

    # Life_check method for ending battle sequences
    def life_check(self):
        if self.current_health > 0:
            return self.alive
        else:
            self.alive = False
            return self.alive

###############################################################################
#############################---Enemy---Classes---#############################
###############################################################################

class Enemy(object):
    def __init__(self, location, current_health, square_map):
        self.location = location
        self.current_health = current_health
        #tells us what the maximum health is
        self.maxHealth = current_health
        #health that changes when attacked
        self.current_health = current_health  
        self.dodge = False
        self.alive = True
        self.square_map = square_map


    # Life check method used to end battle sequences
    def life_check(self):
        if self.current_health > 0:
            return self.alive
        else:
            self.alive = False
            return self.alive

class Subenemy1(Enemy):
    def __init__(self, location, current_health, square_map):
        #passes arguments onto parent
        super(Subenemy1, self).__init__(location, current_health, square_map)

    # Determines how much exp the player gets from character
    def exp_gain(self, player):

        if player.level == 1:
            expgainValue = random.randint(20,40)
        elif player.level == 2:
            expgainValue = random.randint(20,30)
        elif player.level == 3:
            expgainValue = random.randint(10,20)
        elif player.level == 4:
            expgainValue = 0
        player.exp_gain(expgainValue)
        return expgainValue

    # Attack and Dodge suite
    def attack(self, player):
        if not isinstance(player, Player):
            raise ValueError
        if player.dodge:
            player.dodge = False
        hit = random.randint(0,100)
        if hit <= 10 and player.level == 1:
            player.current_health -= 1
            return -1

        elif hit <= 10 and player.level == 2:
            player.current_health -= 1
            return -1

        elif hit <= 10 and player.level == 3:
            player.current_health -= 1
            return -1
        #code for enemy unsuccessful attack
        else:
            return -100

    def dodging(self):
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 20:
            self.dodge = True

    # Movement suite
    def move(self):
        if self.location == self.square_map[12] or \
        self.location == self.square_map[13]:
            self.location = self.location.n()

        elif self.location == self.square_map[14] or \
        self.location == self.square_map[24]:
            self.location = self.location.e()

        elif self.location == self.square_map[33] or \
        self.location == self.square_map[34]:
            self.location = self.location.s()

        elif self.location == self.square_map[32] or \
        self.location == self.square_map[22]:
            self.location = self.location.w()

class Subenemy2(Enemy):
    def __init__(self, location, current_health, square_map):
        super(Subenemy2, self).__init__(location, current_health, square_map)

    # Customized EXP determiner
    def exp_gain(self, player):
        if player.level == 1:
            expgainValue = random.randint(35,50)
        elif player.level == 2:
            expgainValue = random.randint(30,40)
        elif player.level == 3:
            expgainValue = random.randint(20,30)
        elif player.level == 4:
            expgainValue = 0
        player.exp_gain(expgainValue)
        return expgainValue

    # Attack and Dodge Suite
    def attack(self, player):
        if not isinstance(player, Player):
            raise ValueError

        if player.dodge:
            player.dodge = False

        hit = random.randint(0,100)
        if hit <= 15 and player.level == 1:
            player.current_health -= 2
            return -2

        if hit <= 15 and player.level == 2:
            player.current_health -= 2
            return -2

        if hit <= 15 and player.level == 3:
            player.current_health -= 1
            return -2
        #code for enemy unsuccessful attack
        else:
            return -100

    def dodging(self):
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 30:
            self.dodge = True

    # Movement suite
    def move(self):
        if self.location == self.square_map[93] or \
        self.location == self.square_map[94]:
            self.location = self.location.n()

        elif self.location == self.square_map[73] or \
        self.location == self.square_map[83]:
            self.location = self.location.e()

        elif self.location == self.square_map[75] or \
        self.location == self.square_map[74]:
            self.location = self.location.s()

        elif self.location == self.square_map[85] or \
        self.location == self.square_map[95]:
            self.location = self.location.w()

class Subenemy3(Enemy):
    def __init__(self, location, current_health, square_map):
        super(Subenemy3, self).__init__(location, current_health, square_map)
    # EXP suite
    def exp_gain(self, player):           
        if player.level == 1:
            expgainValue = random.randint(40,60)                         
        elif player.level == 2:
            expgainValue = random.randint(30,40)
        elif player.level == 3:
            expgainValue = random.randint(20,30)
        elif player.level == 4:
            expgainValue = 0
        player.exp_gain(expgainValue)
        return expgainValue

    # Attack and Dodge Suite
    def attack(self, player):
        if not isinstance(player, Player):
            raise ValueError

        if player.dodge:
            player.dodge = False

        hit = random.randint(0,100)


        if hit <= 20 and player.level == 1:
            player.current_health -= 3
            return -3

        if hit <= 20 and player.level == 2:
            player.current_health -= 3
            return -3

        if hit <= 20 and player.level == 3:
            player.current_health -= 2
            return -2
        #code for enemy unsuccessful attack
        else:
            return -100

    def dodging(self):
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 40:
            self.dodge = True
        else:
            pass

    # Movement Suite
    def move(self):
        if self.location == self.square_map[56] or \
        self.location == self.square_map[57] or \
        self.location == self.square_map[58]:
            self.location = self.location.n()

        elif self.location == self.square_map[26] or\
        self.location == self.square_map[36] or \
        self.location == self.square_map[46]:
            self.location = self.location.e()

        elif self.location == self.square_map[29] or\
        self.location == self.square_map[28] or \
        self.location == self.square_map[27]:
            self.location = self.location.s()

        elif self.location == self.square_map[59] or \
        self.location == self.square_map[49] or \
        self.location == self.square_map[39]:
            self.location = self.location.w()

class Subenemy4(Enemy):
    def __init__(self, location, current_health, square_map):
        super(Subenemy4, self).__init__(location, current_health, square_map)

    # EXP suite
    def exp_gain(self, player):
        if player.level == 1:
            expgainValue = random.randint(50,70)
        elif player.level == 2:
            expgainValue = random.randint(40,60)
        elif player.level == 3:
            expgainValue = random.randint(30,50)
        elif player.level == 4:
            expgainValue = 0
        player.exp_gain(expgainValue)
        return expgainValue

    # Attack and Dodge suite
    def attack(self, player):
        if not isinstance(player, Player):
            raise ValueError

        if player.dodge:
            player.dodge = False

        hit = random.randint(0,100)

        if hit <= 25 and player.level == 1:
            player.current_health -= 4
            return -4

        if hit <= 25 and player.level == 2:
            player.current_health -= 4
            return -4

        if hit <= 25 and player.level == 3:
            player.current_health -= 3
            return -3
        #code for enemy unsuccessful attack
        else:
            return -100

    def dodging(self):
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 50:
            self.dodge = True

    # Movement suite
    def move(self):
        if self.location == self.square_map[50] \
        or self.location == self.square_map[51]:
            self.location = self.location.n()

        elif self.location == self.square_map[52] \
        or self.location == self.square_map[62]:
            self.location = self.location.e()

        elif self.location == self.square_map[72] \
        or self.location == self.square_map[71]:
            self.location = self.location.s()

        elif self.location == self.square_map[60] \
        or self.location == self.square_map[70]:
            self.location = self.location.w()

class Subenemy5(Enemy):
    def __init__(self, location, current_health, square_map):
        super(Subenemy5, self).__init__(location, current_health, square_map)
        self.movement_type = random.randint(0,1)
    # EXP suite
    def exp_gain(self, player):
        if player.level == 1:
            expgainValue = random.randint(80,100)

        elif player.level == 2:
            expgainValue = random.randint(70,90)

        elif player.level == 3:
            expgainValue = random.randint(60,80)

        elif player.level == 4:
            expgainValue = 0
        player.exp_gain(expgainValue)
        return expgainValue

    # This enemy can blow up Player_house instance, which causes the game to end
    def blow_up(self):
        if isinstance(self.location, Player_house):
            self.location.blow_up()

    # Attack and Movement suite
    def attack(self, player):
        if not isinstance(player, Player):
            raise ValueError

        if player.dodge:
            player.dodge = False

        hit = random.randint(0,100)
        
        if hit <= 30 and player.level == 1:
            player.current_health -= 5
            return -5

        if hit <= 30 and player.level == 2:
            player.current_health -= 5
            return -5

        if hit <= 30 and player.level == 3:
            player.current_health -= 4
            return -4
        #code for enemy unsuccessful attack
        else:
            return -100

    def dodging(self):
        dummy_dodge = random.randint(0,100)
        if dummy_dodge <= 70:
            self.dodge = True

    # Movement Suite    
    def move(self):
        #Destruction of House 4 starts this movement
        if not self.square_map[61].intact: 
            if self.movement_type == 0:
                left_count = 0
                down_count = 0
                if left_count < 2 and self.location.w():
                    self.location = self.location.w()
                    left_count += 1
                else:
                    if down_count < 3 and self.location.s():
                        self.location = self.location.s()
                        down_count += 1
                    else:
                        left_count = 0
                        down_count = 0
        
            else:
                left_count = 0
                down_count = 0
                if down_count < 2 and self.location.s():
                    self.location = self.location.s()
                    down_count += 1
                else:
                    if left_count < 3 and self.location.w():
                        self.location = self.location.w()
                        left_count += 1
                    else:
                        left_count = 0
                        down_count = 0

###############################################################################
##############################---images/Bomb----###############################
###############################################################################

class Bomb(object):
    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        if self.number == other.number:
            return True
        elif self.number != other.number or not isinstance(other, Bomb):
            return False

###############################################################################
############################---Map---Class---##################################
###############################################################################

class Square(object):
    def __init__(self, house_number):
        self._n = None
        self._e = None
        self._s = None
        self._w = None
        self.inventory = set([])
        self.house_number = house_number
        #for GUI topleftCorner x-cordinates of where square will belong
        self.xLocation = None
        #topleftCorner y-cordinates of where square will belong
        self.yLocation = None


    def set_n(self, node):
        if not isinstance(node, Square) and node is not None:
            raise ValueError   
        if node is None:
            self._n = node
        elif node == self._n:
            pass    
        elif self._n is not None:
            (self._n).set_s(None)
            self._n = None
            self._n = node
            (node).set_s(self)
        elif isinstance(node, Square):
            self._n = node
            node.set_s(self)

    def set_e(self, node):
        if not isinstance(node, Square) and node is not None:
            raise ValueError
        if node is None:
            self._e = node
        elif node == self._e:
            pass 
        elif self._e is not None:
            (self._e).set_w(None)
            self._e = None
            self._e = node
            (node).set_w(self)
        elif isinstance(node, Square):
            self._e = node
            node.set_w(self)

    def set_s(self, node):
        if not isinstance(node, Square) and node is not None:
            raise ValueError
        if node is None:
            self._s = node
        elif node == self._s:
            pass
        elif self._s is not None:
            (self._s).set_n(None)
            self._s = None
            self._s = node
            (node).set_n(self)
        elif isinstance(node, Square):
            self._s = node
            node.set_n(self)

    def set_w(self, node):
        if not isinstance(node, Square) and node is not None:
            raise ValueError
        if node is None:
            self._w = node
        elif node == self._w:
            pass
        elif self._w is not None:
            (self._w).set_e(None)
            self._w = None
            self._w = node
            (node).set_e(self)
        elif isinstance(node, Square):
            self._w = node
            node.set_e(self)

    def n(self):
        if isinstance(self._n, Square):
            return self._n
        else:
            return None

    def s(self):
        if isinstance(self._s, Square):
            return self._s
        else:
            return None

    def e(self):
        if isinstance(self._e, Square):
            return self._e
        else:
            return None

    def w(self):
        if isinstance(self._w, Square):
            return self._w
        else:
            return None

class House(Square):
    def __init__(self, number, bomb, house_number):
        super(House, self).__init__(house_number)
        #makes sure that bomb and number are both Bomb instances
        if not isinstance(bomb, Bomb):
            raise ValueError
        if not isinstance(number, Bomb):
            raise ValueError
        #checks whether house is not blown or not
        self.intact = True
        #later use for when player drops bomb
        self.inventory = set([])
        #hidden bombs, only appear when a house is blown up
        self.secret_inventory = set([bomb])
        self.number = number
        #for GUI topleftCorner x-cordinates of where square will belong
        self.xLocation = None
        #topleftCorner y-cordinates of where square will belong
        self.yLocation = None


    def blow_up(self):
        poppedItem = self.inventory.pop()
        if poppedItem == self.number:
            self.intact = False
        else: 
            self.inventory.add(poppedItem)

class Player_house(Square):
    def __init__(self, house_number):
        super(Player_house, self).__init__(house_number)
        self.intact = True

    # Method changes intact member 
    # (This is one of many sufficient conditons for ending game)
    def blow_up(self):
        self.intact = False

class Boss_house(House):
    def __init__(self, number, house_number):
        #cant inheret __init__ since doesnt have 'bomb' argument
        if not isinstance(number, Bomb):
            raise ValueError
        self._n = None
        self._e = None
        self._s = None
        self._w = None
        self.intact = True
        self.inventory = set([])
        self.number = number
        self.house_number = house_number
        #for GUI topleftCorner x-cordinates of where square will belong
        self.xLocation = None
        #topleftCorner y-cordinates of where square will belong
        self.yLocation = None

###############################################################################
####################---Instantiation---Facilitators---#########################
###############################################################################

# Creates five bombs each labled with a different number.
def bomb_instantiator():
    # count used to label bombs appropriately
    count = 0
    # easy access to bombs later
    bomb_list = {}
    for bomb in xrange(0,5):
        #instantiation
        bomb_list[count] = Bomb(count)
        count += 1

    return bomb_list

# Creates 100 squares (for map)
def square_instantiator():
    # Creates 100 squares (for map)
    square_map = {}
    bomb_list = bomb_instantiator()
    count = 0
    for x in xrange(100):
        square_map[count] = Square(count)
        count += 1
    ###assigns X, Y cordinates for GUI implementation###
    #Setting cordinates for first background tile
    xCordinate = 75
    yCordinate = 525
    gridCount = 0
    #iterates 10 times since there are 10 collumns  
    for x in xrange(10):
        #assigns x cordinates and y cordinates according to position
        for y in xrange(10):
            square_map[gridCount].xLocation = xCordinate
            square_map[gridCount].yLocation = yCordinate
            gridCount += 1
            #tiles are 50*50px in dimension so cumilates 50px
            yCordinate -= 50
        #yCordinate resets back to bottom most position
        yCordinate = 525
        xCordinate += 50


    # Certain squares will be re-assigned as houses
    #x and y locations must be transfered to the new instances
    #House - 1
    tempInst = square_map[0]
    square_map[0] = Player_house(0)
    square_map[0].xLocation = tempInst.xLocation
    square_map[0].yLocation = tempInst.yLocation
    #House - 1
    tempInst = square_map[23]
    square_map[23] = House(bomb_list[0], bomb_list[1], 23)
    square_map[23].xLocation = tempInst.xLocation
    square_map[23].yLocation = tempInst.yLocation
    #House - 2
    tempInst = square_map[47]
    square_map[47] = House(bomb_list[1] , bomb_list[2], 84)
    square_map[47].xLocation = tempInst.xLocation
    square_map[47].yLocation = tempInst.yLocation
    #House - 3
    tempInst = square_map[61]
    square_map[61] = House(bomb_list[2], bomb_list[3], 47)
    square_map[61].xLocation = tempInst.xLocation
    square_map[61].yLocation = tempInst.yLocation
    #House - 4
    tempInst = square_map[84]
    square_map[84] = House(bomb_list[3], bomb_list[4], 61)
    square_map[84].xLocation = tempInst.xLocation
    square_map[84].yLocation = tempInst.yLocation
    #Boss House
    tempInst = square_map[99]
    square_map[99] = Boss_house(bomb_list[4], 99)
    square_map[99].xLocation = tempInst.xLocation
    square_map[99].yLocation = tempInst.yLocation

    return square_map, bomb_list

# Connects the squares into coherent map:
################################
# 9 19 29 39 49 59 69 79 89 99 # 
# 8 17 27 37 47 57 67 77 87 97 # 
# 7 17 27 37 47 57 67 77 87 97 #
# 6 16 26 36 46 56 66 76 86 96 #
# 5 15 25 35 45 55 65 75 85 95 #
# 4 14 24 34 44 54 64 74 84 94 #
# 3 13 23 33 43 53 63 73 83 93 #
# 2 12 22 32 42 52 62 72 82 92 #
# 1 11 21 31 41 51 61 71 81 91 #
# 0 10 20 30 40 50 60 70 80 90 #
################################

def square_connector():
    # squares needed to connect them
    square_map, bomb_list = square_instantiator()

    count = 0

    # connects first column (from left) only vertically
    for square in xrange(0, 100):
        if count <= 8: 
            square_map[count].set_n(square_map[count + 1])
            count += 1
            
        # connects last node to its left-neighbor
        elif count == 99:
            square_map[count].set_w(square_map[count - 10])
        
        # top-most square in first row will be connected later
        elif count == 9:
            count += 1
            
        # connects bottom-most row horizontally
        elif count > 9 and (count % 10) == 0: 
            square_map[count].set_w(square_map[count - 10])
            square_map[count].set_n(square_map[count + 1])
            count += 1
            
        # connects top-most row to its left-neighbor
        elif (str(count).count('9') is 1 and count < 90):
            square_map[count].set_w(square_map[count - 10])
            count += 1
            
        # connects every other node vertically and horizontally
        elif count > 9:
            square_map[count].set_w(square_map[count - 10])
            square_map[count].set_n(square_map[count + 1])
            count += 1
            
    # connected map
    return square_map, bomb_list

###############################################################################
######################---The---Actual---Instantiatons---#######################
###############################################################################

# Everything instantiated here 

def the_instantiator():
    square_map, bomb_list = square_connector()

    player = Player(square_map[0], bomb_list[0], 50)

    enemy_list = []
    # first kind of enemy
    enemy_list.append(Subenemy1(square_map[12], 3, square_map))
    enemy_list.append(Subenemy1(square_map[32], 3, square_map))
    enemy_list.append(Subenemy1(square_map[24], 3, square_map))
    # second kind of enemy
    enemy_list.append(Subenemy2(square_map[95], 4, square_map))
    enemy_list.append(Subenemy2(square_map[93], 4, square_map))
    enemy_list.append(Subenemy2(square_map[74], 4, square_map))
    # third kind of enemy
    enemy_list.append(Subenemy3(square_map[39], 5, square_map))
    enemy_list.append(Subenemy3(square_map[58], 5, square_map))
    enemy_list.append(Subenemy3(square_map[26], 5, square_map))
    enemy_list.append(Subenemy3(square_map[56], 5, square_map))
    # fourth kind of enemy
    enemy_list.append(Subenemy4(square_map[51], 6, square_map))
    enemy_list.append(Subenemy4(square_map[62], 6, square_map))
    enemy_list.append(Subenemy4(square_map[71], 6, square_map))
    # fifth kind of enemy
    enemy_list.append(Subenemy5(square_map[98], 7, square_map))
    enemy_list.append(Subenemy5(square_map[89], 7, square_map))
    enemy_list.append(Subenemy5(square_map[88], 7, square_map))

    return square_map, bomb_list, player, enemy_list
    
###############################################################################
############################---Main---Script---################################
###############################################################################

def game():
    #create all game instances at first
    square_map, bomb_list, player, enemy_list = the_instantiator()
    #pygame must be initialized
    pygame.init()
    #sends all instances to GUI Class - incharge of all rendering of graphics
    graphics = GUI(square_map, bomb_list, player, enemy_list)
    while True:
        #takes keyboard input and allows pygame to be quit
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        graphics.renderSuite()
        #game runs while boss/player houses are afloat and player is alive
        if square_map[99].intact and player.life_check() \
        and square_map[0].intact:
            #player turn occurs (takes input)
            player_turn(player, graphics)
            if square_map[99].intact == False:
                #if house 99 blows up, means player defeated boss (checks immediately after player drops)
                graphics.win()
            #checks if enemy location and player location are identical
            for enemy in enemy_list:
                #if player and enemy locations are identical, enters fight sequence
                if enemy.location == player.location and enemy.life_check():
                    fight(graphics, player, enemy)
                #if player dies, the dead graphics play to celebrate the player's death
                if not player.life_check():
                    graphics.dead()
                #if enemies reach the player house, intact changes, causing game to finish
                if isinstance(enemy.location, Player_house):
                    enemy.location.intact = False
            #pauses display for a moment to make graphics more sensible
            graphics.renderSuite()
            time.sleep(0.1)
            #moves enemies once move/or fight sequence is over
            enemy_movement(enemy_list)
            #second repetition to make sure that if enemy lands on character, fight starts
            for enemy in enemy_list:
                #if player and enemy locations are identical, enters fight sequence
                if enemy.location == player.location and enemy.life_check():
                    fight(graphics, player, enemy)
                #if enemies reach the player house, intact changes, causing game to finish
                if isinstance(enemy.location, Player_house):
                    enemy.location.intact = False
        #player dies
        if not player.life_check():
            graphics.dead()
        #win game funct
        if not square_map[0].intact:
            graphics.dead()
        if not square_map[99].intact:
            graphics.win()

def player_turn(player, graphics):
    # Turn Handler
    turn_over = False
    while turn_over is False:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player.move_up()
                    turn_over = True
                elif event.key == K_DOWN:
                    player.move_down()
                    turn_over = True
                elif event.key == K_LEFT:
                    player.move_left()
                    turn_over = True
                elif event.key == K_RIGHT:
                    player.move_right()
                    turn_over = True
                elif event.key == K_p:
                    player.pick_up_item()
                    #update the screen to show immediate response
                    graphics.renderSuite()

                elif event.key == K_d:
                    drop = player.drop_item()
                    #makes sure that the inventory GUI gets updates when bomb is dropped
                    graphics.playerInventory()
                    pygame.display.update()
                    if drop == 1:
                        player.location.blow_up()
                        #update graphics
                        graphics.renderSuite()
                        turn_over = True
                    else:
                        pass
            if event.type == QUIT:
                exit()

def enemy_movement(enemy_list):
    #move every live enemy
    for enemy in enemy_list:
        if enemy.life_check():
            enemy.move()

def fight(graphics, player, enemy):
    #Fight Suite
    #changes GUI to fight sequence
    graphics.fightSequence()
    graphics.playerHealthBar(player.current_health, player.health_bar)
    graphics.enemyHealthBar(enemy.current_health, enemy.maxHealth)
    pygame.display.update()
    while player.life_check() and enemy.life_check():
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        #Player turn first
        #recieves how much damage is given and sends it to the GUI console function
        damage = fight_player(player, enemy)
        graphics.fightsequenceConsole(damage)
        graphics.playerHealthBar(player.current_health, player.health_bar)
        pygame.display.update()
        #Enemy turn second
        time.sleep(0.2)
        damage = fight_enemy(player, enemy)
        graphics.fightsequenceConsole(damage)
        graphics.enemyHealthBar(enemy.current_health, enemy.maxHealth)
        pygame.display.update()
    #clears the attack sequence console once the attacking is done.
    if player.life_check():
        expValue = enemy.exp_gain(player)
        graphics.battleWon(expValue)

    else:
        return 'You lost and thus died. gg'
    #resets the sequence text to blank for next battle
    graphics.sequenceText = []

def fight_player(player, enemy):
    playerInput = False
    while playerInput == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                x,y = event.pos
                #coordinates for the big red attack button
                if x >= 110 and x<= 310 and y>= 430 and y<= 630:
                    damage = player.attack(enemy)
                    playerInput = True
                    return damage
                #coordinates for the big blue dodge button
                if x >= 340 and x<= 540 and y>= 430 and y<= 630:
                    player.dodging()
                    playerInput = True
                    return 100

def fight_enemy(player, enemy):
    command = random.randint(0,5)
    if command == 0:
        enemy.dodging()
        return -101
    else:
        damage = enemy.attack(player)
        return damage


###############################################################################
##########################--------GUI--------##################################
###############################################################################

class GUI(object):
    def __init__(self, square_map, bomb_list, player, enemy_list):
        #initiallizing for pygame
        self.screen = pygame.display.set_mode((650,700),0,32)
        pygame.display.set_caption("Hide and Seak")
        self.font = pygame.font.SysFont("gillsans",16)
        self.fightFont = pygame.font.SysFont("gillsans",18)
        #defining arguments passed into object
        self.square_map = square_map
        self.bomb_list = bomb_list
        self.player = player
        self.enemy_list = enemy_list
        #load images from folder into usable vars
        self.blueTile = pygame.image.load('images/blockBlue.png')
        self.skyTile = pygame.image.load('images/blockSky.png')
        self.house1 = pygame.image.load('images/House-1.png').convert_alpha()
        self.house2 = pygame.image.load('images/House-2.png').convert_alpha()
        self.house3 = pygame.image.load('images/House-3.png').convert_alpha()
        self.house4 = pygame.image.load('images/House-4.png').convert_alpha()
        self.fireImage = pygame.image.load('images/fire.png').convert_alpha()
        self.bossTile = pygame.image.load('images/House-Boss.png').convert_alpha()
        self.startTile = pygame.image.load('images/House-Start.png').convert_alpha()
        self.playerImage = pygame.image.load('images/character.png').convert_alpha()
        self.bomb1 = pygame.image.load('images/Bomb-1.png').convert_alpha()
        self.bomb2 = pygame.image.load('images/Bomb-2.png').convert_alpha()
        self.bomb3 = pygame.image.load('images/Bomb-3.png').convert_alpha()
        self.bomb4 = pygame.image.load('images/Bomb-4.png').convert_alpha()
        self.bombBoss = pygame.image.load('images/Bomb-Boss.png').convert_alpha()
        self.enemyImage = pygame.image.load('images/enemy.png').convert_alpha()
        self.instructions = pygame.image.load('images/instructions.png').convert_alpha()
        self.houseArray = [self.house1, self.house2, self.house3, self.house4]
        self.bombArray = [self.bomb1, self.bomb2, self.bomb3, self.bomb4, self.bombBoss]

        #forEnemySequence
        self.stickFigureBig = pygame.image.load('images/stickFigureBig.png').convert_alpha()
        self.enemyBig = pygame.image.load('images/enemyBig.png').convert_alpha()
        self.dodgeButton = pygame.image.load('images/Dodge.png').convert_alpha()
        self.attackButton = pygame.image.load('images/Attack.png').convert_alpha()
        self.attackSequenceBar = pygame.image.load('images/AttackSequenceBar.png').convert_alpha()
        self.victoryStamp = pygame.image.load('images/VictoryStamp.png').convert_alpha()
        self.sequenceText = []

        #deadSequence
        self.paik = pygame.image.load('images/PaikFace.png').convert_alpha()
        self.crown = pygame.image.load('images/crown.png').convert_alpha()
        self.endNigh = pygame.image.load('images/endNigh.png').convert_alpha()

        #winSequence
        self.foot = pygame.image.load('images/Foot.png').convert_alpha()
        self.endingScreen = pygame.image.load('images/EndNighHappy.png').convert_alpha()

    def renderSuite(self):
        self.renderBackground()
        self.printPlayer()
        self.printEnemy()
        self.mapHealthBar()
        self.mapExperienceBar()
        self.playerInventory()
        #readjust for instruction
        self.screen.set_clip((0,0), (650, 700))
        self.screen.blit(self.instructions, (0, 0))
        pygame.display.update()

    def renderBackground(self):
        self.screen.set_clip((0,0), (650, 700))
        self.screen.fill((255,255,255))
        #governs the color of the tile
        alternator = 0
        #looks after the value of alternator%2
        alternatorMod = 0
        #helps change colors of houses
        houseCount = 0
        #since every row, tile order must shift by one, %2 results must shift
        for square in self.square_map:
            if alternator == 10:
                alternator = 0
                if alternatorMod == 0:
                    alternatorMod = 1
                elif alternatorMod == 1:
                    alternatorMod = 0
            #the actual laying down of tiles.
            if alternator%2 == alternatorMod:
                self.screen.blit(self.skyTile, (self.square_map[square].xLocation, self.square_map[square].yLocation))
                alternator += 1
            else:
                self.screen.blit(self.blueTile, (self.square_map[square].xLocation, self.square_map[square].yLocation))
                alternator += 1
            #lays down additional graphics according to instance (is it a house? boss house?)
            #if the instance is a Player_house....
            if isinstance(self.square_map[square], Player_house):
                if self.square_map[square].intact == True:
                    self.screen.blit(self.startTile, (self.square_map[square].xLocation, self.square_map[square].yLocation))
            #if the instance is a Boss_house....
            elif isinstance(self.square_map[square], Boss_house):
                if self.square_map[square].intact == True:
                    self.screen.blit(self.bossTile, (self.square_map[square].xLocation, self.square_map[square].yLocation))
            #if the instance is a House....
            elif isinstance(self.square_map[square], House):
                #Since we want to display different colored houses for each unique instance
                self.screen.blit(self.houseArray[houseCount], (self.square_map[square].xLocation, self.square_map[square].yLocation))
                if self.square_map[square].intact == False:
                    #also blit an image of a fire on top of the house
                    self.screen.blit(self.fireImage, (self.square_map[square].xLocation, self.square_map[square].yLocation))
                    #if the blown up house reveals an item, will display a bomb on top of the house as well
                    for item in self.square_map[square].secret_inventory:
                        #remember bomb numbers and bomb image numbers all corespond
                        bombNumber = item.number
                        #readjust x,y coordinates to center bomb since squares are 50x50 but bombs are 30x30px
                        self.screen.blit(self.bombArray[bombNumber], ((self.square_map[square].xLocation)+10, (self.square_map[square].yLocation)+20))
                #also print bombs if player drops on wrong house
                for item in self.square_map[square].inventory:
                    bombNumber = item.number
                    self.screen.blit(self.bombArray[bombNumber], ((self.square_map[square].xLocation)+10, (self.square_map[square].yLocation)+20))
                #houseCount should cumilate even if house array is blownup, and not blitted
                houseCount += 1


    def mapHealthBar(self):
        #self.player.health_bar refers to MAX HEALTH, self.player.current_health refers to player's current health
        #to adjust bar at constant 200px
        multplicationNeeded = 200/float(self.player.health_bar)
        #((R,G,B),(x-location,y-location,y-width,x-height))
        #this one is for background black bar
        self.screen.fill((0,0,0),(125,590,self.player.health_bar*multplicationNeeded,25))
        #this one is for forground red bar
        self.screen.fill((255,0,0),(125,590,self.player.current_health*multplicationNeeded,25))
        #text diplay on top of the exp bar
        healthStat = self.font.render(str('(' + str(self.player.current_health)+'/'+str(self.player.health_bar) + ')'),1,(255,255,255))
        healthLabel = self.font.render(str('Health: '),1,(0,0,0))
        #text requires a blit, w/ location info
        self.screen.blit(healthStat,(180,590))
        self.screen.blit(healthLabel,(75,590))

    def mapExperienceBar(self):
        #self.player.exp_bar is MAX exp needed, self.player.exp_bar is CURRENT exp
        #special display for level 4
        if self.player.exp_needed == str('fullBar'):
            self.screen.fill((54,255,255),(125,620,200,25))
            experience = self.font.render(str('Level' + str(self.player.level) + ' (Max Level!)'),1,(0,0,0))
            expLabel = self.font.render(str('Exp:'),1,(0,0,0))
        else:
            #to adjust bar at constant 200px
            multplicationNeeded = float(200)/float(self.player.exp_needed)
            #((R,G,B),(x-location,y-location,y-width,x-height))
            #this one is for background black bar
            self.screen.fill((190,190,190),(125,620,self.player.exp_needed*multplicationNeeded,25))
            #this one is for forground red bar
            self.screen.fill((54,255,255),(125,620,self.player.exp_bar*multplicationNeeded,25))
            #text diplay on top of the exp bar
            experience = self.font.render(str('Level' + str(self.player.level) + ' (' + str(self.player.exp_bar)+'/'+str(self.player.exp_needed) + ')'),1,(0,0,0))
            expLabel = self.font.render(str('Exp:'),1,(0,0,0))
        #text requires a blit, w/ location info
        self.screen.blit(experience,(165,620))
        self.screen.blit(expLabel,(75,620))

    def printPlayer(self):
        self.screen.set_clip((0,0), (650, 700))
        self.screen.blit(self.playerImage, (self.player.location.xLocation, self.player.location.yLocation))

    def printEnemy(self):
        self.screen.set_clip((0,0), (650, 700))
        for enemy in self.enemy_list:
            #only print the enemies if they are still alive
            if enemy.life_check():
                self.screen.blit(self.enemyImage, (enemy.location.xLocation, enemy.location.yLocation))

    def playerInventory(self):
        #specifies part of the screen that will be updated ((x,y cordinates),(width,height))
        self.screen.set_clip((0,650), (300, 35))
        self.screen.fill((255,255,255))        
        #initial x position for the first bomb
        x = 145
        for bomb in self.player.inventory:
            bombNumber = bomb.number
            self.screen.blit(self.bombArray[bombNumber], (x, 650))
            #staggars bomb position since they are 35x35 each
            x += 35
        self.screen.blit(self.font.render(str('Inventory: '), True, (0,0,0)),(75,650))

    def fightSequence(self):
        self.screen.set_clip((0,0), (650, 700))
        self.screen.fill((255,255,255))
        self.screen.blit(self.stickFigureBig, (25, 70))
        self.screen.blit(self.enemyBig, (325, 70))
        #attackButton dimensions are 200x200   
        self.screen.blit(self.attackButton, (110, 430))
        #dodgeButton dimensions are 200x200   
        self.screen.blit(self.dodgeButton, (340, 430))
        self.screen.blit(self.attackSequenceBar, (0, 0))

    def playerHealthBar(self, playerCurrentHealth, playerMaxHealth):
        self.screen.set_clip((0,0),(650,700))
        ######RENDERS HEALTH BAR######
        #since maxHealth values vary by oponent, adjust for 200 PX wide
        multplicationNeeded = 200/float(playerMaxHealth)
        #((R,G,B),(x-location,y-location,y-width,x-height))
        #this one is for background black bar
        self.screen.fill((0,0,0),(75,390,playerMaxHealth*multplicationNeeded,25))
        #this one is for forground red bar
        self.screen.fill((255,0,0),(75,390,playerCurrentHealth*multplicationNeeded,25))
        #text diplay on top of the exp bar
        experience = self.font.render(str(str(playerCurrentHealth)+'/'+str(playerMaxHealth)),1,(255,255,255))
        #text requires a blit, w/ location info
        self.screen.blit(experience,(154,392))

    def enemyHealthBar(self, enemyCurrentHealth, enemyMaxHealth):
        self.screen.set_clip((0,0),(650,700))
        ######RENDERS ENEMY HEALTH BAR######
        #same notation as the playerHealthBar, shifted 200px to the right
        #since maxHealth values vary by oponent, adjust for 200 PX wide
        multplicationNeeded = float(float(200)/float(enemyMaxHealth))
        self.screen.fill((0,0,0),(375,390,enemyMaxHealth*multplicationNeeded,25))
        #this one is for forground red bar
        self.screen.fill((255,0,0),(375,390,enemyCurrentHealth*multplicationNeeded,25))
        #text diplay on top of the exp bar
        experience = self.font.render(str(str(enemyCurrentHealth)+'/'+str(enemyMaxHealth)),1,(255,255,255))
        #text requires a blit, w/ location info
        self.screen.blit(experience,(454,392))

    def fightsequenceConsole(self, damage):
        #height = fontsize* number of rows you want to display
        self.screen.set_clip((0,630), (700, 18*3))
        self.screen.fill((255,255,255))
        y = 630
        #if the given damage is 0, means player missed
        if damage == 0:
            self.sequenceText.append(str('You MISSED!'))
        #damage -100 is code for enemy missed attack
        elif damage == -100:
            self.sequenceText.append(str('Enemy MISSED!'))
        #damage -101 is code for enemy dodge
        elif damage == -101:
            self.sequenceText.append(str('Enemy DODGED YOUR ATTACK!'))
        elif damage == 100:
            self.sequenceText.append(str('You are ready to DODGE!!'))            

        #if the given damage is positive, means player successfully attacked enemy
        elif damage > 0:
        #if the given damage is negative, means enemy attacked
            self.sequenceText.append(str('You hit the enemy '+str(damage) +' damage.'))
        elif damage < 0:
            damage = damage + (-(damage*2))
            self.sequenceText.append(str('The enemy attacked you '+str(damage) +' damage.'))
        #iterates though text to print one message at a time
        for text in reversed(self.sequenceText):
            self.screen.blit(self.fightFont.render(str(text), True, (0,0,0)),(200,y))
            #shifts y value of printed message by font height so that messages stagger
            y += 18

    def battleWon(self, expAmt):
        #create a new surface w/ alpha channels
        transparentRect = pygame.Surface((650,700), pygame.SRCALPHA)
        #give it some color w/ 4th value as alpha channel (currently 50% opcaity)
        transparentRect.fill((150,100,100,240))
        self.screen.blit(transparentRect, (0,0))
        #blit the victory stamp! victory stamp is 650x600px
        self.screen.blit(self.victoryStamp, (0,50))
        self.screen.blit(self.fightFont.render(str('Congratulations!!! '), True, (255,255,255)),(220,562))
        self.screen.blit(self.fightFont.render(str('You have gained ' + str(expAmt) + ' exp'), True, (255,255,255)),(200,590))
        self.screen.blit(self.fightFont.render(str('CLICK TO CONTINUE'), True, (255,255,255)),(210,630))
        pygame.display.update()
        mouseClicked = False
        while mouseClicked == False:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mouseClicked = True

    def dead(self):
        self.screen.set_clip((0,0), (650, 700))
        transparentRect = pygame.Surface((650,700), pygame.SRCALPHA)
        for x in xrange(230):
                transparentRect.fill((125,0,0,x))
                self.screen.blit(transparentRect, (0,0))
                pygame.display.update()
        self.screen.fill((125,0,0))
        x = 600
        while x != 0:
            self.screen.fill((125,0,0))
            self.screen.blit(self.paik,(x,0))
            pygame.display.update()
            x -= 1
        y = -300
        while y!= 0:
            self.screen.fill((125,0,0))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,y))
            y += 30
            pygame.display.update()
        for x in xrange(3):
            self.screen.fill((125,0,0))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            self.screen.blit(self.endNigh,(0,0))
            pygame.display.update()
            time.sleep(1)
            self.screen.fill((125,0,0))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            time.sleep(1)
            pygame.display.update()
        while True:
            self.screen.fill((125,0,0))
            self.screen.fill((125,0,0))
            self.screen.blit(self.endNigh,(0,0))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            self.screen.blit(self.fightFont.render(str('CLICK TO EXIT'), True, (0,0,0)),(210,630))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    exit(3)

    def win(self):
        self.screen.set_clip((0,0), (650, 700))
        transparentRect = pygame.Surface((650,700), pygame.SRCALPHA)
        for x in xrange(200):
                transparentRect.fill((255,255,255,x))
                self.screen.blit(transparentRect, (0,0))
                pygame.display.update()
        self.screen.fill((255,255,255))
        x = 600
        while x != 0:
            self.screen.fill((255,255,255))
            self.screen.blit(self.paik,(x,0))
            pygame.display.update()
            x -= 1
        y = -300
        while y!= 0:
            self.screen.fill((255,255,255))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,y))
            y += 30
            pygame.display.update()
        for x in xrange(3):
            self.screen.fill((255,255,255))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            self.screen.blit(self.endNigh,(0,0))
            pygame.display.update()
            time.sleep(1)
            self.screen.fill((255,255,255))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            time.sleep(1)
            pygame.display.update()
        y = -900
        while y!= 0:
            self.screen.fill((255,255,255))
            self.screen.blit(self.paik,(0,0))
            self.screen.blit(self.crown,(0,0))
            self.screen.blit(self.endNigh,(0,0))
            self.screen.blit(self.foot,(0,y))
            y += 30
            pygame.display.update()
        while True:
            self.screen.fill((255,255,255))
            self.screen.blit(self.foot,(0,0))
            self.screen.blit(self.endingScreen,(0,0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    exit(3)

####Image Credit####
#Professor Paik: http://www.news.cs.nyu.edu/sites/default/filesimages/group.preview.jpg
#Burger King Hat: http://s3.amazonaws.com/everystockphoto/fspid30/59/63/15/3/lightbox-burgerking-crown-5963153-o.jpg
#Dragon Ball Cloud: http://th08.deviantart.net/fs70/PRE/f/2010/024/6/6/images/Nube_Voladora_by_camarinox.png
#Foot: http://etc.usf.edu/clipart/63300/63322/63322_foot_lg.gif

game()