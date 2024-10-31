import tkinter as tk
import random
import time
from tkinter import messagebox
from tkinter import filedialog
from datetime import time, date, datetime


ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (
    UP,
    DOWN,
    LEFT,
    RIGHT,
    f"{UP}-{LEFT}",
    f"{UP}-{RIGHT}",
    f"{DOWN}-{LEFT}",
    f"{DOWN}-{RIGHT}",
)
WALL_VERTICAL = "|"
WALL_HORIZONTAL = "-"
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
INVALID = "That ain't a valid action buddy."
TASK_ONE = 1
TASK_TWO = 2


class BoardModel:
    """
    this is BoardModel class
    to display the game with strings.
    """

    def __init__(self, grid_size, num_pokemon):
        self.grid_size = grid_size
        self.num_pokemon = num_pokemon
        self.game = UNEXPOSED * grid_size**2
        self.pokemon_locations = self.generate_pokemons(grid_size, num_pokemon)

    def get_game(self):
        """(str) Returns the game string."""
        return self.game

    def get_pokemon_locations(self):
        """(str) Returns the pokemon locations."""
        return self.pokemon_locations

    def get_num_attempted_catches(self):
        """(str) Returns the num catched."""
        return self.num_attempted_catches

    def get_num_pokemon(self):
        """(str) Returns the number of pokemon."""
        return self.num_pokemon

    def check_loss(self):
        """select (bool): if the game is over"""
        for location in self.pokemon_locations:
            if self.game[location] != UNEXPOSED:
                return True
        return False

    def generate_pokemons(self, grid_size, number_of_pokemons):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = grid_size**2
        pokemon_locations = ()

        for _ in range(number_of_pokemons):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count)

            while index in pokemon_locations:
                index = random.randint(0, cell_count)

            pokemon_locations += (index,)
        print(pokemon_locations)
        return pokemon_locations

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * grid_size + y

    def replace_character_at_index(self, game, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        return game[:index] + character + game[index + 1 :]

    def flag_cell(self, game, index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.

        Parameters:
            game (str): The game string.
            index (int): The index in the game string where a flag is placed.
        Returns
            (str): The updated game string.
        """
        if game[index] == FLAG:
            game = self.replace_character_at_index(game, index, UNEXPOSED)

        elif game[index] == UNEXPOSED:
            game = self.replace_character_at_index(game, index, FLAG)

        return game

    def index_in_direction(self, index, grid_size, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
          | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        col = index % grid_size
        row = index // grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < grid_size and 0 <= row < grid_size):
            return None
        return self.position_to_index((row, col), grid_size)

    def neighbour_directions(self, index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    def number_at_cell(self, game, pokemon_locations, grid_size, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if game[index] != UNEXPOSED:
            return int(game[index])

        number = 0
        for neighbour in self.neighbour_directions(index, grid_size):
            if neighbour in pokemon_locations:
                number += 1

        return number

    def check_win(self, game, pokemon_locations):
        """Checking if the player has won the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

        Returns:
            (bool): True if the player has won the game, false if not.

        """
        return UNEXPOSED not in game and game.count(FLAG) == len(pokemon_locations)

    def reveal_cells(self, game, grid_size, pokemon_locations, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        game = self.replace_character_at_index(game, index, str(number))
        clear = self.big_fun_search(game, grid_size, pokemon_locations, index)
        for i in clear:
            if game[i] != FLAG:
                number = self.number_at_cell(game, pokemon_locations, grid_size, i)
                game = self.replace_character_at_index(game, i, str(number))

        return game

    def big_fun_search(self, game, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if game[index] == FLAG:
            return queue

        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if game[neighbour] != FLAG:
                    number = self.number_at_cell(
                        game, pokemon_locations, grid_size, neighbour
                    )
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible


class PokemonGame:
    """
    this is PokemonGame class
    it is a controller for the whole game which can display strings with a intuitive way for users.
    """

    def __init__(self, master, grid_size=10, num_pokemon=15, task=TASK_ONE):
        """define what are these attributes and display the board for the game. This controller class will communicate with other classes"""
        self._master = master
        self._master.title("Pokemon: Got 2 Find Them All!")
        self._pokemonGame = BoardModel(grid_size, num_pokemon)
        self._label = tk.Label(
            self._master,
            text="Pokemon: Got 2 Find Them All!",
            bg="#ff8080",
            fg="white",
            font="helvetica 18",
        )
        self._label.pack(fill=tk.X)
        self._grid_size = grid_size
        if task == TASK_ONE:
            self._board_view = BoardView(master, grid_size)
            self._board_view.draw_board(self._pokemonGame.get_game())
            self._board_view.pack()
        else:
            self._board_view = ImageBoardView(master, self._grid_size)
            self._board_view.draw_board(self._pokemonGame.get_game())
            self._board_view.pack()
            self._status_bar = StatusBar(master)
            self._status_bar.pack()
        # bind left and right click
        self._board_view.bind("<Button-1>", self.handle_left_click)
        self._board_view.bind("<Button-3>", self.handle_right_click)

        # menu bar
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save game", command=self.save_game)
        filemenu.add_command(label="Load game", command=self.load_game)
        filemenu.add_command(label="Restart game", command=self.restart)
        filemenu.add_command(label="New game", command=self.new_game)
        filemenu.add_command(label="Quit", command=self.quit)
        self._filename = None

    def save_game(self):
        """save this game as a file"""
        pass

    def load_game(self):
        """load the file and display it"""
        pass

    def restart(self):
        """restart the game with same pokemon locations and game string"""
        pass

    def new_game(self):
        """create a new game"""
        pass

    def quit(self):
        """ "quit this game"""
        if (
            messagebox.askyesno(title="Game over", message="Do you wish to quit")
            == True
        ):
            self._master.destroy()

    def handle_left_click(self, event):
        """some works for left click"""
        pixel = (event.x, event.y)
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position)
        self._pokemonGame.game = self._pokemonGame.reveal_cells(
            self._pokemonGame.game,
            self._grid_size,
            self._pokemonGame.pokemon_locations,
            index,
        )
        self._board_view.draw_board(self._pokemonGame.get_game())
        if self._pokemonGame.check_loss():
            for location in self._pokemonGame.pokemon_locations:
                self._pokemonGame.game = self._pokemonGame.replace_character_at_index(
                    self._pokemonGame.game, location, POKEMON
                )
                self._board_view.draw_board(self._pokemonGame.get_game())
            messagebox.showinfo(title=None, message="You lose")
            self._master.destroy()

    def handle_right_click(self, event):
        """some wotks for right click"""
        pixel = (event.x, event.y)
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position)
        print(index)
        if (
            self._pokemonGame.game[index] == UNEXPOSED
            or self._pokemonGame.game[index] == FLAG
        ):
            self._pokemonGame.game = self._pokemonGame.flag_cell(
                self._pokemonGame.game, index
            )
            self._board_view.draw_board(self._pokemonGame.get_game())

        if self._pokemonGame.check_win(
            self._pokemonGame.game, self._pokemonGame.pokemon_locations
        ):
            messagebox.showinfo(title=None, message="You win")
            self._master.destroy()

        if self._pokemonGame.game[index] == FLAG:
            pass

    def pixel_to_position(self, pixel):
        """transfer the pixel to position"""
        row = pixel[0] // 60
        col = pixel[1] // 60
        position = (row, col)
        return position

    def position_to_index(self, position):
        """transfer the position to index"""
        index = position[1] * 10 + position[0]
        return index


class BoardView(tk.Canvas):
    """
    this is BoardView class
    display basic board for task 1.
    """

    def __init__(self, master, grid_size=10, board_width=600, *args, **kwargs):
        """define what are these attributes and display the board for the games."""
        super().__init__(master)
        self.grid_size = grid_size
        self.board_width = board_width
        self.config(width=board_width, height=board_width)

    def draw_board(self, board):
        """use rectangle to draw the whole task 1 board"""
        print("2")
        for index in range(len(board)):
            position = self.index_to_position(index)
            pixel = self.position_to_pixel(position)
            if board[index] == UNEXPOSED:
                self.create_rectangle(
                    pixel[0], pixel[1], pixel[0] + 60, pixel[1] + 60, fill="dark green"
                )

            elif board[index] == FLAG:
                self.create_rectangle(
                    pixel[0], pixel[1], pixel[0] + 60, pixel[1] + 60, fill="red"
                )

            elif board[index] == POKEMON:
                self.create_rectangle(
                    pixel[0], pixel[1], pixel[0] + 60, pixel[1] + 60, fill="yellow"
                )

            else:
                self.create_rectangle(
                    pixel[0], pixel[1], pixel[0] + 60, pixel[1] + 60, fill="light green"
                )
                self.create_text(pixel[0] + 30, pixel[1] + 30, text=board[index])

    def index_to_position(self, index):
        """transfer the index to position"""
        row = index % 10
        col = index // 10
        position = (row, col)
        return position

    def position_to_pixel(self, position):
        """ "transfer the position to pixel"""
        pixel = (position[0] * 60, position[1] * 60)
        return pixel


class StatusBar(tk.Frame, BoardModel):
    """ "
    this is statusbar class
    which shows a statusbar under the board.
    """

    def __init__(self, master, **kw):
        """define what are these attributes and display the board for the games."""
        super().__init__(master, **kw)
        self._master = master
        self._clock_image = tk.PhotoImage(file="images/clock.gif")
        self._pokeball = tk.PhotoImage(file="images/full_pokeball.gif")
        self._frame1 = tk.Frame(self._master, bg="white")
        self._frame1.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self._frame2 = tk.Frame(self._master, bg="white")
        self._frame2.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self._frame3 = tk.Frame(self._master, bg="white")
        self._frame3.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        tk.Label(self._frame1, image=self._pokeball, bg="white").pack(
            side=tk.LEFT, padx=(50, 0), pady=20
        )
        self._label1 = tk.Label(
            self._frame1, text="0 attemped catches", bg="white", font="helvetica 10"
        )
        self._label1.pack(side=tk.TOP, pady=(35, 5))
        self._label2 = tk.Label(
            self._frame1, text="15 pokeballs left", bg="white", font="helvetica 10"
        )
        self._label2.pack(side=tk.TOP, pady=(5, 20))
        tk.Label(self._frame2, image=self._clock_image, bg="white").pack(side=tk.LEFT)
        self._label3 = tk.Label(
            self._frame2, text="Time elapsed", bg="white", font="helvetica 10"
        )
        self._label3.pack(side=tk.TOP, pady=(30, 5))
        self._label4 = tk.Label(
            self._frame2, text="0m 0s", bg="white", font="helvetica 10"
        )
        self._label4.pack(side=tk.TOP, pady=(5, 20))
        tk.Button(
            self._frame3,
            text="New game",
            command=self.newgame,
            bg="white",
            font="helvetica 10",
        ).pack(side=tk.TOP, pady=(30, 5))
        tk.Button(
            self._frame3,
            text="Restart game",
            command=self.restart,
            bg="white",
            font="helvetica 10",
        ).pack(side=tk.TOP, pady=(5, 20))

    def newgame(self):
        """create a new board with different pokemon locations"""
        pass

    def restart(self):
        """restart the same game"""
        self._board_view.draw_board(self._pokemonGame.get_game())

    def timer(self):
        """a timer for statusbar"""
        self.after(1000, self.timer)

    def count(self, num_attempted_catches, num_pokemon):
        """count the number of pokemonball"""
        pass


class ImageBoardView(BoardView):
    """ "
    this is iamgeboardview class
    which shows a new board filled with images not rectangles.
    """

    def __init__(self, master, grid_size=10, board_width=600):
        """define what are these attributes and display the board for the games."""
        super().__init__(master, grid_size, board_width)
        self._tall_grass = tk.PhotoImage(file="images/unrevealed.gif")
        self._pokemon_ball = tk.PhotoImage(file="images/pokeball.gif")
        self._zero = tk.PhotoImage(file="images/zero_adjacent.gif")
        self._one = tk.PhotoImage(file="images/one_adjacent.gif")
        self._two = tk.PhotoImage(file="images/two_adjacent.gif")
        self._three = tk.PhotoImage(file="images/three_adjacent.gif")
        self._four = tk.PhotoImage(file="images/four_adjacent.gif")
        self._five = tk.PhotoImage(file="images/five_adjacent.gif")
        self._six = tk.PhotoImage(file="images/six_adjacent.gif")
        self._seven = tk.PhotoImage(file="images/seven_adjacent.gif")
        self._eight = tk.PhotoImage(file="images/eight_adjacent.gif")
        pokemon_profile = {
            1: "images/pokemon_sprites/pikachu.gif",
            2: "images/pokemon_sprites/charizard.gif",
            3: "images/pokemon_sprites/cyndaquil.gif",
            4: "images/pokemon_sprites/psyduck.gif",
            5: "images/pokemon_sprites/togepi.gif",
            6: "images/pokemon_sprites/umbreon.gif",
        }
        self._pokemon1 = tk.PhotoImage(file="images/pokemon_sprites/pikachu.gif")
        self._pokemon2 = tk.PhotoImage(file="images/pokemon_sprites/charizard.gif")
        self._pokemon3 = tk.PhotoImage(file="images/pokemon_sprites/cyndaquil.gif")
        self._pokemon4 = tk.PhotoImage(file="images/pokemon_sprites/psyduck.gif")
        self._pokemon5 = tk.PhotoImage(file="images/pokemon_sprites/togepi.gif")
        self._pokemon6 = tk.PhotoImage(file="images/pokemon_sprites/umbreon.gif")

    def draw_board(self, board):
        """ "draw out a new image board"""
        for index in range(len(board)):
            position = self.index_to_position(index)
            pixel = self.position_to_pixel(position)
            if board[index] == UNEXPOSED:
                self.create_image(
                    pixel[0], pixel[1], anchor="nw", image=self._tall_grass
                )

            elif board[index] == FLAG:
                self.create_image(
                    pixel[0], pixel[1], anchor="nw", image=self._pokemon_ball
                )

            elif board[index] == POKEMON:
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._pokemon1)

            elif board[index] == "0":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._zero)

            elif board[index] == "1":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._one)

            elif board[index] == "2":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._two)

            elif board[index] == "3":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._three)

            elif board[index] == "4":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._four)

            elif board[index] == "5":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._five)

            elif board[index] == "6":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._six)

            elif board[index] == "7":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._seven)

            elif board[index] == "8":
                self.create_image(pixel[0], pixel[1], anchor="nw", image=self._eight)

            else:
                # self.create_rectangle()
                # self.create_text(text=board[index])
                self.create_rectangle(
                    pixel[0], pixel[1], pixel[0] + 60, pixel[1] + 60, fill="light green"
                )
                self.create_text(pixel[0] + 30, pixel[1] + 30, text=board[index])


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonGame(root, task=TASK_TWO)
    root.mainloop()
