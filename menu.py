import curses
from curses import panel
import dockerapi as dockerapi

class Menu(object):

	def __init__(self, items, stdscreen):
		self.window = stdscreen.subwin(0,0)
		self.window.keypad(1)
		self.panel = panel.new_panel(self.window)
		self.panel.hide()
		panel.update_panels()
		self.position = 0
		self.items = items
		self.items.append(('exit','exit'))

	def navigate(self, n):
		self.position += n
		if self.position < 0:
			self.position = 0
		elif self.position >= len(self.items):
			self.position = len(self.items)-1

	def display(self):
		self.panel.top()
		self.panel.show()
		self.window.clear()
		while True:
			self.window.refresh()
			curses.doupdate()
			for index, item in enumerate(self.items):
				if index == self.position:
					mode = curses.A_REVERSE
				else:
					mode = curses.A_NORMAL
				msg = '%d. %s' % (index, item[0])
				self.window.addstr(1+index, 1, msg, mode)
			key = self.window.getch()
			if key in [curses.KEY_ENTER, ord('\n')]:
				if self.position == len(self.items)-1:
					break
				else:
					if len(self.items[self.position]) == 3:
						self.items[self.position][1](self.items[self.position][2])
					else:
						self.items[self.position][1]()

			elif key == curses.KEY_UP:
				self.navigate(-1)
			elif key == curses.KEY_DOWN:
				self.navigate(1)
		self.window.clear()
		self.panel.hide()
		panel.update_panels()
		curses.doupdate()

class MyApp(object):

	def __init__(self, stdscreen):
		self.screen = stdscreen
		curses.curs_set(0)

		self.dockerApi = dockerapi.DockerAPI()
		
		repoMenuItems = []
		for image, tag in self.dockerApi.imageDict.items():
			repoMenuItems.append((image, self.createAndDisplay(self.dockerApi.imageDict[image])))

		repoMenu = Menu(repoMenuItems, self.screen)

		repoMenu.display()

	def createAndDisplay(self, subMenuItems):
		tagItems = []
		for item in subMenuItems:
			tagItems.append((item[0], self.dockerApi.runImage, item[1]))

		tagMenu = Menu(tagItems, self.screen)
		return tagMenu.display
