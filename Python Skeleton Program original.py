import random as r


def sign(num):
	return -1 if num < 0 else 1
class GameOverException(Exception):
	def __init__(s, winLoss):
		s.winLoss = winLoss
		super().__init__()

class Exit(Exception):
	pass
class Position:  # Anything on the map will be a position
	def __init__(s, x, y, gridIdentifier=1) -> None:
		s._x = x
		s._y = y
		s._gID = gridIdentifier

	def __eq__(s, o) -> bool:
		return s._x == o.x and s._y == o.y

	def __add__(s, o) -> bool:
		return s._x + o.x and s._y + o.y

	def __le__(s, o) -> bool:
		return s._x <= o.x and s._y <= o.y

	def __lt__(s, o) -> bool:
		return s._x < o.x and s._y < o.y

	def __gt__(s, o) -> bool:
		return s._x > o.x and s._x > o.y

	def __ge__(s, o) -> bool:
		return s._x >= o.x and s._y >= o.y

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
	def __init__(s, pos, identifier):
		super(Item, s).__init__(pos[0], pos[1], identifier)


class Character(Position):
	possibleMoves = {"w" : Position(0, -1),
					 "a" : Position(1, 0),
					 "s" : Position(0, 1),
					 "d" : Position(-1, 0),
					}
	def __init__(s, pos):
		super(Character, s).__init__(pos[0], pos[1], "*")
		s._collectedItems = []
	@property
	def collectedItems(s):
		return s._collectedItems
	
	def MakeMove(s, grid):
		while True:
			print("Press Control C at anytime to Exit to Menu")
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
	def TakeTurn(s, grid):
		s.MakeMove(grid)
		for pos in grid:
			if isinstance(pos, Item):
				if pos == s:
					s._collectedItems.append(pos)
class Enemy(Position):
	positionIdentifiers = {True  : "!",
						   False : " ",	
						  }
	defaultSleepCounter = 4
	def __init__(s, pos, isAwake=False, sleepCounter = -1):
		super(Enemy, s).__init__(pos[0], pos[1])
		s._awake = isAwake
		s._sleepCounter = sleepCounter
		s._gID = Enemy.positionIdentifiers[s._awake]

	@property
	def awake(s):
		return s._awake

	@awake.setter
	def awake(s, isAwake):
		s._awake = isAwake
		s.gID = Enemy.positionIdentifiers[s._awake]

	def toggleAwake(s):
		s._awake = not s._awake
	@property
	def sleepCounter(s):
		return s._sleepCounter
	@sleepCounter.setter
	def sleepCounter(s, count):
		s._sleepCounter = count


	def TakeTurn(s, player):
		s._sleepCounter -= 1
		if s._sleepCounter == 0:
			s.toggleAwake()
		if s._awake:
			if s == player:
				raise GameOverException(0)
			s.MakeMove(player)
			if s == player:
				raise GameOverException(0)
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
	def __init__(s, pos):
		Item.__init__(s, pos)
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

	def __iter__(s):
		s.iC = 0
		return s
	def __next__(s):
		if s.iC < len(s._gridState):
			output = s._gridState[s.iC]
			s.iC += 1 
			return output
		else:
			raise StopIteration
	def __repr__(s) -> str:
		dividerLine = "-" * (s._posMax.x * 2 + 1)
		output = [dividerLine]
		for y in range(s._posMax.y):
			line = "|"
			for x in range(s._posMax.x):
				try:
					positionIdentifier = s._gridState[s._gridState.index(Position(x, y))].gID
				except ValueError:
					positionIdentifier = Grid.blankSpace
				line += f"{positionIdentifier}|"
			output.append(line)
			output.append(dividerLine)
		outputSTR = "\n".join(output)
		return outputSTR

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
		return s._posMin < position <= s._posMax
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
	ySize = 6

	def Start(s, setPosition = False):
		print(f"Set Positions: {setPosition}")
		s.Cave = Grid(Game.xSize, Game.ySize)
		if setPosition:
			s.Player = Character((0, 0))
			s.Monster = Enemy((5, 5))
			s.items = [Item((3, 3), "F"), Item((6, 2), "T"), Item((8, 8), "P")]
		else:
			s.Player = Character(s.Cave.GenerateRandomPosition(False).pos)
			s.Monster = Enemy(s.Cave.GenerateRandomPosition().pos, sleepCounter = 2)
			itemIdentifiers = ["F", "T", "P"]
			r.shuffle(itemIdentifiers)
			s.items = [Item(s.Cave.GenerateRandomPosition().pos, itemIdentifiers.pop(0)) for _ in range(r.randint(1, len(itemIdentifiers)))]
		s.Cave.AddPositionsToGrid(s.Player, s.Monster, s.items)
		s.Play()
		r.seed()

	def Play(s):
		try:
			while True:
				print(s.Cave)
				s.Player.TakeTurn(s.Cave)
				if len(s.Player.collectedItems) == len(s.items):
					raise GameOverException(1)
				s.Monster.TakeTurn(s.Player)
		except GameOverException as winLoss:
			if bool(winLoss.winLoss):
				print("You won, congrats")
			else:
				print("Skill issue")
		except KeyboardInterrupt:
			pass
	def Exit(s, *args):
		print("You have chosen to exit")
		raise Exit
	def __init__(s):
		options = {"0" : ("Play", s.Start, False),
				   "1" : ("Play (Set Positions)", s.Start, True),
				   "9" : ("Exit", s.Exit, "")}
		while True:
			print("Welcome to the Game, would you like to play")
			print("\n".join([f"{x} : {options[x][0]}" for x in options]))
			userInput = input("Input: ")
			if userInput in options:
				options[userInput][1](options[userInput][2])
			else:
				print("Invalid Input")
		

if __name__ == "__main__":
	try:
		while True:
			Game()
	except Exit:
		pass