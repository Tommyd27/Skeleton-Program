import random as r


def sign(num):
	return -1 if num < 0 else 1


class Position:  # Anything on the map will be a position
	def __init__(s, x, y, gridIdentifier=1) -> None:
		s._x = x
		s._y = y
		s._gID = gridIdentifier

	def __eq__(s, o) -> bool:
		return s._x == o.x and s._y == o.y

	def __add__(s, o) -> bool:
		return s._x + o.x and s._y + o.y

	def __lt__(s, o) -> bool:
		return s._x < o.x and s._y < o.y

	def __gt__(s, o) -> bool:
		return s._x > o.x and s._y > o.y

	def __add__(s, o):
		return Position(s._x + o.x, s._y + o.y)

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
	def pos(s, nPos):
		s._x = nPos.x
		s._y = nPos.y

	@property
	def gID(s):
		return s._gID

	@gID.setter
	def gID(s, gridIdentifier):
		s._gID = gridIdentifier


class Item(Position):
	def __init__(s, x, y, identifier):
		super(Item, s).__init__(x, y, identifier)


class Character(Position):
	possibleMoves = {"w" : Position(1, 0),
					 "a" : Position(0, 1),
					 "s" : Position(-1, 0),
					 "d" : Position(0, -1),
					}
	def __init__(s, x=0, y=0):
		super(Position, s).__init__(x, y, "*")

	def MakeMove(s, grid):
		while True:
			userMoveInput = input("Where would you like to move (WASD): ").lower()
			try:
				move = Character.possibleMoves[userMoveInput]
				newPosition = s + move
				if grid.InGrid(newPosition):
					s.pos = newPosition
					break
			except KeyError:
				pass
			print("Sorry, that is not a valid move.")

class Enemy(Position):
	positionIdentifiers = {True  : "!",
						   False : " ",	
						  }
	def __init__(s, x=0, y=0, isAwake=False):
		super(Position, s).__init__(x, y)
		s._awake = isAwake
		s.gID = Enemy.positionIdentifiers[s._awake]

	@property
	def awake(s):
		return s._awake

	@awake.setter
	def awake(s, isAwake):
		s._awake = isAwake
		s.gID = Enemy.positionIdentifiers[s._awake]

	def MakeMove(s, Player: Character):
		# Calculate distances
		idealMove = [("x", Player.x - s._x), ("y", Player.y - s._y)]
		# Remove move away from player (because on same x or y)
		idealMove = [x for x in idealMove if x[1] != 0]
		try:
			move = r.choice(idealMove)
			if move[0] == "x":
				s._x = sign(move[1])
			else:
				s._y = sign(move[1])
		except IndexError:
			pass  # In same square as Character


class Trap(Item):
	def __init__(s):
		Item.__init__(s)
		s._triggered = False

	@property
	def triggered(s):
		return s._triggered

	def toggleTriggerd(s):
		s._triggered = not s._triggered


class Grid:
	blankSpace = " "
	def __init__(s, xSize, ySize):
		if xSize < 1 or ySize < 1:
			raise ValueError("Grid Size must be larger than 0")
		s._posMin = Position(0, 0)
		s._posMax = Position(xSize, ySize)
		s._gridState = []

	@property
	def posMax(s):
		return s._posMax

	@property
	def gridState(s):
		return s._gridState

	def __repr__(s) -> str:
		dividerLine = ["-" * (s._posMax.x * 2 + 1)]
		output = dividerLine
		for y in range(s._posMax):
			line = "|"
			for x in range(s._posMax.x):
				try:
					positionIdentifier = s._gridState[s._gridState.index(Position(x, y))].gID
				except ValueError:
					positionIdentifier = Grid.blankSpace
				line += f"{positionIdentifier}|"
			output.append(line)
		return output

	def AddPositionsToGrid(s, *args, unique = False):
		lists = [x for x in args if isinstance(x, list)]
		nonLists = [x for x in args if not isinstance(x, list)]

		allPositions = nonLists
		for sList in lists:
			allPositions  += sList

		for positionToAdd in allPositions:
			if unique and positionToAdd in s._gridState:
				raise ValueError("Item Already at that Location")
			s._gridState.append(positionToAdd)
	def InGrid(s, position):
		return s._posMin <= position <= s._posMax
	def GenerateRandomPosition(s, unique = True):
		x = r.randint(0, s._posMax.x - 1)
		y = r.randint(0, s._posMax.y - 1)
		nPos = Position(x, y)
		while unique and nPos in s._gridState:
			x = r.randint(0, s._posMax.x - 1)
			y = r.randint(0, s._posMax.y - 1)
			nPos = Position(x, y)
		return nPos

class Game:
	xSize = 10
	ySize = 10

	def __init__(s, setPosition = False):
		s.Cave = Grid()
		if setPosition:
			s.Player = Character(0, 0)
			s.Monster = Enemy(5, 5)
			s.items = [Item(3, 3, "F"), Item(6, 2, "T"), Item(8, 8, "P")]
		else:
			s.Player = Character(s.Cave.GenerateRandomPosition(False).pos)
			s.Monster = Character(s.Cave.GenerateRandomPosition().pos)
			itemIdentifiers = ["F", "T", "P"]
			r.shuffle(itemIdentifiers)
			s.items = [Item(s.Cave.GenerateRandomPosition().pos, itemIdentifiers.pop(0)) for _ in range(r.randint(1, len(itemIdentifiers)))]
		s.Cave.AddPositionsToGrid(s.Player, s.Monster, s.items)
		r.seed()

	def Play(self):
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
				FlaskFound = self.Player.CheckIfSameCell(
					self.Flask.GetPosition())
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
						Eaten = self.Monster.CheckIfSameCell(
							self.Player.GetPosition())
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
