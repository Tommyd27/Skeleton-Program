import random

def sign(num):
  return -1 if num < 0 else 1
class Position:#Anything on the map will be a position
  def __init__(s, x, y) -> None:
    s._x = x
    s._y = y
  def __eq__(s, o) -> bool:
    return s._x == o.x and s._y == o.y
  def __add__(s, o) -> bool:
    return s._x + o.x and s._y + o.y
  def __lt__(s, o) -> bool:
    return s._x < o.x and s._y < o.y
  def __gt__(s, o) -> bool:
    return s._x > o.x and s._y > o.y

  @property
  def x(s):
    return s._x
  @x.setter
  def x(s, x):
    s._x = x
  @property
  def y(s):
    return s._y
  @y.setter
  def y(s, y):
    s._y = y
  @property
  def pos(s):
    return s._x, s._y
  @pos.setter
  def pos(s, x, y):
    s._x = x
    s._y = y

class Item(Position):
  def __init__(s, x, y):
    super(Item, s).__init__(x, y)       

class Character(Position):
  def __init__(s, x = 0, y = 0):             
    super(Position, s).__init__(x, y)    

  def MakeMove(self, Direction):
    direction = direction.lower()
    if Direction == 'n':
      self._y += 1 
    elif Direction == 's':
      self._y -= 1            
    elif Direction == 'w':
      self._x -=  1 
    elif Direction == 'e':
      self._x +=  1

class Enemy(Position):
  def __init__(s, x = 0, y = 0, isAwake = False):             
    super(Position, s).__init__(x, y)
    s._awake = isAwake
  @property
  def awake(s):
    return s._awake
  @awake.setter
  def awake(s, isAwake):
    s._awake = isAwake

  def MakeMove(s, Player):
    if random.randint(0, 1) == 0 and Player.y - s._y != 0:
      s._y = 1 * sign
    else:
      pass

class Trap(Item):
  def __init__(self):
    Item.__init__(self)
    self.Triggered = False

  def GetTriggered(self):
    return self.Triggered

  def ToggleTrap(self):
    self.Triggered = not self.Triggered

class Grid:
  def __init__(self, NS, WE):
    self.NSDistance = NS
    self.WEDistance = WE
    self.CavernState = []
    for Count1 in range(self.NSDistance + 1):
      BlankRow = []
      for Count2 in range(self.WEDistance + 1):
        BlankRow.append(' ')
      self.CavernState.append(BlankRow)

  def Display(self, MonsterAwake):
    print(" ------------- ")
    for Count1 in range(self.NSDistance + 1):
      for Count2 in range(self.WEDistance + 1):
        if (self.CavernState[Count1][Count2] == ' ') or  (self.CavernState[Count1][Count2] == '*') or ((self.CavernState[Count1][Count2] == 'M') and MonsterAwake):
          print('|' + self.CavernState[Count1][Count2], end='')
        else:
          print('| ', end='')
      print('|')
      print(" ------------- ")
    print()     

  def PlaceItem(self, Position, Item):
    self.CavernState[Position.y][Position.x] = Item

  def IsCellEmpty(self, Position):
    if Position.x < 0 or Position.x > Game.WE:
      print("Error")
    if Position.y < 0 or Position.y > Game.NS:
      print("Error")
    if self.CavernState[Position.y][Position.x] == ' ':
      return True
    else:
      return False

  def Reset(self):
    for Count1 in range(self.NSDistance + 1):
      for Count2 in range(self.WEDistance + 1):
        self.CavernState[Count1][Count2] = ' '

class Game:
  NS = 4       
  WE = 6

  def __init__(self, IsATrainingGame):
    self.Player = Character()
    self.Cavern = Grid(Game.NS, Game.WE)
    self.Monster = Enemy()
    self.Flask = Item()
    self.Trap1 = Trap()
    self.Trap2 = Trap()
    self.TrainingGame = IsATrainingGame
    random.seed()
    self.SetUpGame()
    self.Play()

  def Play(self):
    Eaten = False
    FlaskFound = False
    MoveDirection = ' '
    Position = Cell()
    self.Cavern.Display(self.Monster.GetAwake())
    while not Eaten and not FlaskFound and (MoveDirection != 'M'):
      ValidMove = False
      while not ValidMove:
        self.DisplayMoveOptions()
        MoveDirection = self.GetMove()
        ValidMove = self.CheckValidMove(MoveDirection)
      if MoveDirection != 'M':         
        self.Cavern.PlaceItem(self.Player.GetPosition(), ' ')
        self.Player.MakeMove(MoveDirection)
        self.Cavern.PlaceItem(self.Player.GetPosition(), '*')
        self.Cavern.Display(self.Monster.GetAwake())
        FlaskFound = self.Player.CheckIfSameCell(self.Flask.GetPosition())
        if FlaskFound:
          self.DisplayWonGameMessage()
        Eaten = self.Monster.CheckIfSameCell(self.Player.GetPosition())
        # This selection structure checks to see if the player has triggered one of the traps in the cavern
        if not self.Monster.GetAwake() and not FlaskFound and not Eaten and (self.Player.CheckIfSameCell(self.Trap1.GetPosition()) and not self.Trap1.GetTriggered() or self.Player.CheckIfSameCell(self.Trap2.GetPosition()) and not self.Trap2.GetTriggered()):
          self.Monster.ChangeSleepStatus()
          self.DisplayTrapMessage()
          self.Cavern.Display(self.Monster.GetAwake())
        if (self.Monster.GetAwake()) and not Eaten and not FlaskFound:
          Count = 0
          while Count != 2 and not Eaten:
            self.Cavern.PlaceItem(self.Monster.GetPosition(), ' ')
            Position = self.Monster.GetPosition()
            self.Monster.MakeMove(self.Player.GetPosition())
            self.Cavern.PlaceItem(self.Monster.GetPosition(), 'M')
            if self.Monster.CheckIfSameCell(self.Flask.GetPosition()):
              self.Flask.SetPosition(Position)
              self.Cavern.PlaceItem(Position, 'F')
            Eaten = self.Monster.CheckIfSameCell(self.Player.GetPosition())
            print()
            print('Press Enter key to continue')
            input()
            self.Cavern.Display(self.Monster.GetAwake())
            Count = Count + 1
      if Eaten:
        self.DisplayLostGameMessage()

  def DisplayMoveOptions(self):
    print()
    print("Enter N to move NORTH")
    print("Enter S to move SOUTH")
    print("Enter E to move EAST")
    print("Enter W to move WEST")
    print("Enter M to return to the Main Menu")
    print()

  def GetMove(self):
    Move = input()
    print()
    if Move != "": 
      return Move[0] 
    else:
      return ""
    
  def DisplayWonGameMessage(self):
    print("Well done!  You have found the flask containing the Styxian potion.")
    print("You have won the game of MONSTER!")
    print()    

  def DisplayTrapMessage(self):
    print("Oh no!  You have set off a trap.  Watch out, the monster is now awake!")
    print()

  def DisplayLostGameMessage(self):
    print("ARGHHHHHHH!  The monster has eaten you.  GAME OVER.")
    print("Maybe you will have better luck next time you play MONSTER!")
    print()

  def CheckValidMove(self, Direction):
    ValidMove = True
    if not(Direction in ['N', 'S', 'W', 'E', 'M']):
      ValidMove = False 
    return ValidMove

  def SetPositionOfItem(self, Item):
    Position = self.GetNewRandomPosition()
    while not self.Cavern.IsCellEmpty(Position):
      Position = self.GetNewRandomPosition()
    self.Cavern.PlaceItem(Position, Item)
    return Position

  def SetUpGame(self):
    Position = Cell()
    self.Cavern.Reset()
    if not self.TrainingGame:
      Position.x = 0
      Position.y = 0
      self.Player.SetPosition(Position)
      self.Cavern.PlaceItem(Position, '*')
      self.Trap1.SetPosition(self.SetPositionOfItem('T'))
      self.Trap2.SetPosition(self.SetPositionOfItem('T'))
      self.Monster.SetPosition(self.SetPositionOfItem('M'))
      self.Flask.SetPosition(self.SetPositionOfItem('F'))
    else:
      Position.x = 4
      Position.y = 2
      self.Player.SetPosition(Position)
      self.Cavern.PlaceItem(Position, '*')
      Position.x = 6
      Position.y = 2
      self.Trap1.SetPosition(Position)
      self.Cavern.PlaceItem(Position, 'T')
      Position.x = 4
      Position.y = 3
      self.Trap2.SetPosition(Position)
      self.Cavern.PlaceItem(Position, 'T')
      Position.x = 4
      Position.y = 0
      self.Monster.SetPosition(Position)
      self.Cavern.PlaceItem(Position, 'M')
      Position.x = 3
      Position.y = 1
      self.Flask.SetPosition(Position)
      self.Cavern.PlaceItem(Position, 'F')

  def GetNewRandomPosition(self):
    Position = Cell()
    while (Position.y == 0) and (Position.x == 0):
      Position.y = random.randint(0, Game.NS)
      Position.x = random.randint(0, Game.WE)
    return Position
  
def DisplayMenu():
  print("MAIN MENU")
  print()
  print("1.  Start new game")
  print("2.  Play training game")
  print("9.  Quit")
  print()
  print("Please enter your choice: ", end='')

def GetMainMenuChoice():
  Choice = int(input())
  print()
  return Choice

if __name__ == "__main__":
  Choice = 0
  while Choice != 9:
    DisplayMenu()
    Choice = GetMainMenuChoice()
    if Choice == 1:
      MyGame = Game(False)
    elif Choice == 2:
      MyGame = Game(True)
