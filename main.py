import inquirer
import curses
import menu as menu

def main():
	curses.wrapper(menu.MyApp)   

if __name__== "__main__":
	main()
