import random
import numpy as np
import curses
from curses.textpad import rectangle


# Define tiles ["image", movement cost, elevation, cover, heat_modifier]

PLAIN = [".", 1, 0, 0, 0]
HILL = ["^", 2, 2, 2, 0]
WOODS = ["#", 2, 0, 1, 0]
WATER = ["W", 2, 0, 1, -3]
CURSOR = ['+']
PLAYER_MECH = ["@"]
ENEMY_MECH = ['&']

# Set Colours

WHITE = 0
RED = 1
GREEN = 2
BLUE = 3
YELLOW = 4

dirkeys = {
	curses.KEY_LEFT: 'a', curses.KEY_RIGHT: 'd',
	curses.KEY_UP: 'w', curses.KEY_DOWN: 's'}
}

OBJECT_SYMBOL = {2: CURSOR, 1: PLAYER_MECH, 3: ENEMY_MECH}

game_objects = []

class GameObject(object):

	def __init__(self, name, objecttype=CURSOR, x=0, y=0, z=0):
		self.name = name
		self.objecttype = objecttype
		self.x = x
		self.y = y
		self.z = z

		game_objects.append(self)

class Mech(object):

	def __init__(self, name, move, maneuverability, armour,
		shortrange, mediumrange, longrange, sensors, silhouette, heat_sinks):
		self.name = name
		self.move = move
		self.maneuverability = maneuverability
		self.armour = armour
		self.shortrange = shortrange
		self.mediumrange = mediumrange
		self.longrange = longrange
		self.sensors = sensors
		self.silhouette = silhouette
		self.heat_sinks = heat_sinks

	def display(self):
		print("Mech Name: {}".format(self.name))
		print("Move: {}".format(self.move))
		print("Maneuverability: {}".format(self.maneuverability))
		print("Armour: {}".format(self.armour))
		print("Short: {}".format(self.shortrange))
		print("Medium: {}".format(self.mediumrange))
		print("Long: {}".format(self.longrange))
		print("Sensors: {}".format(self.sensors))
		print("Silhouette: {}".format(self.silhouette))
		print("Heat Sinks: {}".format(self.heat_sinks))


class Pilot(object):

	def __init__(self, name, pilot_skill, gunnery_skill):
		self.name = name
		self.pilot_skill = pilot_skill
		self.gunnery_skill = gunnery_skill

	def display(self):
		print("Pilot Name: {}".format(self.name))
		print("Piloting Skill: {}".format(self.pilot_skill))
		print("Gunnery Skill: {}".format(self.gunnery_skill))


class Unit(GameObject):

	def __init__(self, name, mech, pilot):
		GameObject.__init__(self, name, objecttype=PLAYER_MECH, x=0, y=0, z=0)
		self.mech = mech
		self.pilot = pilot
		self.piloting = mech.maneuverability + pilot.pilot_skill
		self.targetting = mech.sensors + pilot.gunnery_skill

	def display(self):
		print("Name: {}".format(self.name))
		print("Pilot: {}".format(self.pilot.name))
		print("Mech: {}".format(self.mech.name))
		print("Piloting: {}".format(self.piloting))
		print("Targetting: {}".format(self.targetting))


class Map(object):

	def __init__(self):
		self.terrain_grid = []
		self.object_grid = []
		self.length = 8
		self.width = 8

	def generate_terrain(self, terrain_list=[PLAIN]):

		for i in range(self.length):
			newlist = []
			for t in range(self.width):
				newlist.append([i,t, random.choice(terrain_list)[0]])
			self.terrain_grid.append(newlist)

		self.terrain_grid = np.asarray(self.terrain_grid)

	def plot_game_objects(self):

		self.object_grid = []

		for i in range(self.length):
			newlist = []
			for t in range(self.width):
				newlist.append([0])
			self.object_grid.append(newlist)

		self.object_grid = np.asarray(self.object_grid)

		for game_object in game_objects:
			if game_object.objecttype == PLAYER_MECH:
				self.object_grid[game_object.x, game_object.y] = 1
			elif game_object.objecttype == CURSOR:
				self.object_grid[game_object.x, game_object.y] = 2
			else:
				self.object_grid[game_object.x, game_object.y] = 3

	def display(self):
		self.view = ""
		for terrain_row, object_row in zip(self.terrain_grid, self.object_grid):
			row_string = ""
			for terrain_column, object_column in zip(terrain_row, object_row):
				if object_column:
					row_string += str(OBJECT_SYMBOL[object_column[0]][0])
				else:
					row_string += terrain_column[2][0]
			self.view += row_string + "\n"

		print(self.view)
		

class Game(object):

	def __init__(self, enemies=1, terrain="plains"):
		self.terrain = terrain
		self.enemies = enemies
		self.game_state = True

	def run_in_curses(stdscr):

		scrheight, scrwidth = stdscr.getmaxyx()

		if (scrheight < 24 or scrwidth < 80):
			raise RuntimeError("80x24 or larger terminal required")

		curses.mousemask(
			curses.BUTTON1_CLICKED | curses.BUTTON1_DOUBLE_CLICKED)
		stdscr.leaveok(0)

		if curses.has_colors():
			curses.init_pair(
				RED, curses.COLOR_RED, curses.COLOR_BLACK)
			curses.init_pair(
				GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
			curses.init_pair(
				BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
			curses.init_pair(
				YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)

		while not finished:
			active_screen.render()
		key = stdscr.getch()
		active_screen.handle_key(key)

	def draw_game_map(window):



	def next_coords(x, y, direction):
		if direction == 'n':
			return x, y - 1
		elif direction == 's':
			return x, y + 1
		elif direction == 'e':
			return x + 1, y
		elif direction ==  'w':
			return x - 1, y
		else:
			raise ValueError("Invalid compass direction " + str(direction))



if __name__ == "__main__":

	cursor = GameObject(name="cursor",x=3,y=3)

	firstmech = Mech("Battlemaster", 3, 0, 24, 5, 7, 5, 3, 2)
	firstmech.display()

	print("")

	firstpilot = Pilot("Carter", 3, 4)
	firstpilot.display()

	print("")

	unit1 = Unit("Banshee", firstmech, firstpilot)
	unit1.display()

	print("")

	game_map = Map()
	game_map.generate_terrain()

	active_game = Game()

	while active_game.game_state:
		game_map.plot_game_objects()
		game_map.display()
		user_input = input("Enter a command (W, A, S, D or Q to quit: ")

		if user_input =="w":
			unit1.x -= 1
		elif user_input =="a":
			unit1.y -= 1
		elif user_input =="s":
			unit1.x += 1
		elif user_input =="d":
			unit1.y += 1
		elif user_input =="q":
			active_game.game_state = False
			print("Game Over")
		else:
			pass

		if unit1.x < 0:
			unit1.x = 0
		if unit1.y < 0:
			unit1.y = 0
		if unit1.x > game_map.length:
			unit1.x = game_map.length
		if unit1.y > game_map.width:
			unit1.y = game_map.width
