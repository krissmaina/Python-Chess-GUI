import tkinter
import os
from PIL import Image, ImageTk


class King:

    @staticmethod
    def get_adjacent_files(file: str) -> tuple:
        """Gets adjacent files, the left, current and right file, if there is any.
        Example:
            if 'a' is the argument, -> ('a', 'b').
            if 'c' is the argument, -> ('b', 'c','d').
            if 'h' is the argument, -> ('g', 'h') since there is no file to the right of h
            """
        if file == 'a':
            return file, chr(ord(file) + 1)
        elif file == 'h':
            return chr(ord(file) - 1), file
        else:
            return chr(ord(file) - 1), file, chr(ord(file) + 1)

    @staticmethod
    def get_adjacent_ranks(rank: int) -> tuple:
        """Gets adjacent ranks and also the current rank.
        Example:
            if rank == 1(at the edge) -> (1, 2).
            if rank == 4(somewhere in the middle) -> (3, 4, 5).
            if rank == 8(at the edge) -> (7, 8)
            """
        if rank == 1:
            return 1, 2
        elif rank == 8:
            return 7, 8
        else:
            return rank - 1, rank, rank + 1

    def __init__(self, color: str, image):
        self.name = 'king'
        self.color = color
        self.image = image
        self.piece_value = 0

        if self.color == 'white':
            self.starting_squares = ('e1',)
        elif self.color == 'black':
            self.starting_squares = ('e8',)

        self.moves = []
        self.current_square = None
        self.annotation = 'K'

    def generate_valid_moves(self) -> list:
        """
        Gets the square the King is currently in and generates the squares that it can move to.
        The king can move horizontally, diagonally, and vertically but only one square at a time.
        """
        file, rank = self.current_square[0], int(self.current_square[1])
        valid_files = self.get_adjacent_files(file)
        valid_ranks = self.get_adjacent_ranks(rank)

        valid_moves = [f'{letter}{num}' for letter in valid_files for num in valid_ranks]

        # remove the original square
        valid_moves.remove(self.current_square)

        return valid_moves


class Queen:

    def __init__(self, color: str, image):
        self.name = 'queen'
        self.color = color
        self.image = image
        self.piece_value = 9

        if self.color == 'white':
            self.starting_squares = ('d1',)
        elif self.color == 'black':
            self.starting_squares = ('d8',)

        self.moves = []
        self.current_square = None
        self.annotation = "Q"

    def generate_valid_moves(self) -> dict:
        """
        Returns a list of valid moves the Queen has.
        A Queen can move: vertically, horizontally and diagonally.
        Vertically it can move in the directions: N, S.
        Horizontally it can move in the directions: W, E.
        Diagonally it can move in the directions: NW, NE, SE, SW.

        This functions returns a dictionary where:
                key: direction (str) eg 'NE'
                value: [valid_moves] list of valid moves in the direction
        """
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        file, rank = self.current_square[0], int(self.current_square[1])
        files_left = files[:files.index(file)][::-1]
        files_right = files[files.index(file) + 1:]

        if rank == 8:
            ranks_up = []
            ranks_down = list(range(7, 0, -1))
        elif rank == 1:
            ranks_up = list(range(2, 9))
            ranks_down = []
        else:
            ranks_up = list(range(rank + 1, 9))
            ranks_down = list(range(rank - 1, 0, -1))

        ne = [f'{letter}{num}' for letter, num in zip(files_right, ranks_up)]
        e = [f'{letter}{rank}' for letter in files_right]
        se = [f'{letter}{num}' for letter, num in zip(files_right, ranks_down)]
        s = [f'{file}{num}' for num in ranks_down]
        sw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_down)]
        w = [f'{letter}{rank}' for letter in files_left]
        nw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_up)]
        n = [f'{file}{num}' for num in ranks_up]

        return {
            'NE': ne,
            'E': e,
            'SE': se,
            'S': s,
            'SW': sw,
            'W': w,
            'NW': nw,
            'N': n,
        }


class Rook:

    def __init__(self, color: str, image):
        self.name = 'rook'
        self.color = color
        self.image = image
        self.piece_value = 5

        if self.color == 'white':
            self.starting_squares = ('a1', 'h1')
        elif self.color == 'black':
            self.starting_squares = ('a8', 'h8')

        self.moves = []
        self.current_square = None
        self.annotation = "R"

    def generate_valid_moves(self) -> dict:
        """
        Returns the valid moves the rook has.
        A rook can move horizontally(W, E) or vertically(N, S).
        This function returns a dictionary containing:
            key: direction(eg N, S)
            value: valid_moves in that direction.
        """
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        file, rank = self.current_square[0], int(self.current_square[1])
        files_left = files[:files.index(file)][::-1]
        files_right = files[files.index(file) + 1:]

        if rank == 8:
            ranks_up = []
            ranks_down = list(range(7, 0, -1))
        elif rank == 1:
            ranks_up = list(range(2, 9))
            ranks_down = []
        else:
            ranks_up = list(range(rank + 1, 9))
            ranks_down = list(range(rank - 1, 0, -1))

        e = [f'{letter}{rank}' for letter in files_right]
        s = [f'{file}{num}' for num in ranks_down]
        w = [f'{letter}{rank}' for letter in files_left]
        n = [f'{file}{num}' for num in ranks_up]

        return {
            'N': n,
            'E': e,
            'W': w,
            'S': s,
        }


class Bishop:

    def __init__(self, color: str, image):
        self.name = 'bishop'
        self.color = color
        self.image = image
        self.piece_value = 3

        if self.color == 'white':
            self.starting_squares = ('c1', 'f1')
        elif self.color == 'black':
            self.starting_squares = ('c8', 'f8')

        self.moves = []
        self.current_square = None
        self.annotation = "B"

    def generate_valid_moves(self) -> dict:
        """
        Returns the valid moves the bishop has.
        A bishop can only move diagonally in NE, SE, SW and NW directions.
        This function returns a dictionary containing:
            key: direction(eg NE, SE)
            value: valid_moves in that direction.
        """
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        file, rank = self.current_square[0], int(self.current_square[1])
        files_left = files[:files.index(file)][::-1]
        files_right = files[files.index(file) + 1:]

        if rank == 8:
            ranks_up = []
            ranks_down = list(range(7, 0, -1))
        elif rank == 1:
            ranks_up = list(range(2, 9))
            ranks_down = []
        else:
            ranks_up = list(range(rank + 1, 9))
            ranks_down = list(range(rank - 1, 0, -1))

        ne = [f'{letter}{num}' for letter, num in zip(files_right, ranks_up)]
        se = [f'{letter}{num}' for letter, num in zip(files_right, ranks_down)]
        sw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_down)]
        nw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_up)]

        return {
            'NE': ne,
            'SE': se,
            'SW': sw,
            'NW': nw
        }


class Knight:

    def __init__(self, color: str, image):
        self.name = 'knight'
        self.color = color
        self.image = image
        self.piece_value = 3

        if self.color == 'white':
            self.starting_squares = ('b1', 'g1')
        elif self.color == 'black':
            self.starting_squares = ('b8', 'g8')

        self.moves = []
        self.current_square = None
        self.annotation = "N"

    def generate_valid_moves(self) -> list:
        """
        Returns the valid moves the knight has.
        A knight moves in an L shape.
        """
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        file, rank = self.current_square[0], int(self.current_square[1])

        left_file_1 = chr(ord(file) - 1) if chr(ord(file) - 1) in files else None
        left_file_2 = chr(ord(file) - 2) if chr(ord(file) - 2) in files else None
        right_file_1 = chr(ord(file) + 1) if chr(ord(file) + 1) in files else None
        right_file_2 = chr(ord(file) + 2) if chr(ord(file) + 2) in files else None

        up_rank_1 = rank + 1 if (rank + 1) in ranks else None
        up_rank_2 = rank + 2 if (rank + 2) in ranks else None
        down_rank_1 = rank - 1 if (rank - 1) in ranks else None
        down_rank_2 = rank - 2 if (rank - 2) in ranks else None

        lr1 = [f'{left_file_1}{num}' for num in (up_rank_2, down_rank_2) if num and left_file_1]
        lr2 = [f'{left_file_2}{num}' for num in (up_rank_1, down_rank_1) if num and left_file_2]
        rr1 = [f'{right_file_1}{num}' for num in (up_rank_2, down_rank_2) if num and right_file_1]
        rr2 = [f'{right_file_2}{num}' for num in (up_rank_1, down_rank_1) if num and right_file_2]

        return lr1 + lr2 + rr1 + rr2


class Pawn:

    def __init__(self, color: str, image):
        self.name = 'pawn'
        self.color = color
        self.image = image
        self.piece_value = 1

        if self.color == 'white':
            self.starting_squares = ('a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2')
        elif self.color == 'black':
            self.starting_squares = ('a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7')

        self.moves = []
        self.current_square = None
        self.annotation = ""

    def generate_valid_moves(self) -> list:
        """
        Returns the valid moves the pawn has.
        A pawn can only move forward one square at a time, except the first move where it can move
        two squares or one square.
        """
        file, rank = self.current_square[0], int(self.current_square[1])
        if self.color == 'white':
            ranks = [2, 3, 4, 5, 6, 7, 8]
            if self.moves:  # the pawn has already moved at least once
                valid_moves = [f'{file}{rank + 1}' if rank + 1 in ranks else None]
            else:  # the pawn has not moved
                valid_moves = [f'{file}{rank + 1}', f'{file}{rank + 2}']
        else:
            ranks = [7, 6, 5, 4, 3, 2, 1]
            if self.moves:
                valid_moves = [f'{file}{rank - 1}' if rank - 1 in ranks else None]
            else:
                valid_moves = [f'{file}{rank - 1}', f'{file}{rank - 2}']

        return valid_moves


class ChessBoard(tkinter.Canvas):
    """Class to represent a chess board with 64 squares and its pieces"""

    @staticmethod
    def get_image(image_path):
        """Returns an image object"""
        image = Image.open(image_path)

        return ImageTk.PhotoImage(image)  # .resize((self.square_length, self.square_length)))

    @staticmethod
    def get_piece(name: str, color: str, image):
        """Given the name, color and image, this function returns the appropriate Piece(King, Queen etc.) object"""
        if name == 'king':
            return King(color, image)
        elif name == 'queen':
            return Queen(color, image)
        elif name == 'rook':
            return Rook(color, image)
        elif name == 'bishop':
            return Bishop(color, image)
        elif name == 'knight':
            return Knight(color, image)
        elif name == 'pawn':
            return Pawn(color, image)

    @staticmethod
    def get_in_between_squares(k_square: str, p_square: str) -> list:
        """Generates the squares between the King and a piece including the piece square.

        This function works for pieces Queen, Rook and Bishop as long as any of the pieces is attacking
        the King.
        """
        king_file, king_rank = k_square[0], int(k_square[1])
        piece_file, piece_rank = p_square[0], int(p_square[1])

        # if the king_file and piece_file are the same
        if king_file == piece_file:
            if piece_rank > king_rank:
                squares = [f'{king_file}{rank}' for rank in range(king_rank + 1, piece_rank + 1)]
            else:
                squares = [f'{king_file}{rank}' for rank in range(king_rank - 1, piece_rank - 1, -1)]

        # if the ranks of the king and the piece are the same
        elif king_rank == piece_rank:
            if ord(piece_file) > ord(king_file):
                squares = [f'{chr(file)}{king_rank}' for file in range(ord(king_file) + 1, ord(piece_file) + 1)]
            else:
                squares = [f'{chr(file)}{king_rank}' for file in range(ord(king_file) - 1, ord(piece_file) - 1, -1)]

        # If the ranks and files are different
        else:
            if ord(king_file) > ord(piece_file):
                if king_rank > piece_rank:
                    squares = [f'{chr(file)}{rank}' for file, rank in
                               zip(range(ord(king_file) - 1, ord(piece_file) - 1, -1),
                                   range(king_rank - 1, piece_rank - 1, -1))]
                else:
                    squares = [f'{chr(file)}{rank}' for file, rank in
                               zip(range(ord(king_file) - 1, ord(piece_file) - 1, -1),
                                   range(king_rank + 1, piece_rank + 1))]
            else:
                if king_rank > piece_rank:
                    squares = [f'{chr(file)}{rank}' for file, rank in
                               zip(range(ord(king_file) + 1, ord(piece_file) + 1),
                                   range(king_rank - 1, piece_rank - 1, -1))]
                else:
                    squares = [f'{chr(file)}{rank}' for file, rank in
                               zip(range(ord(king_file) + 1, ord(piece_file) + 1),
                                   range(king_rank + 1, piece_rank + 1))]

        return squares

    def __init__(self, window, width, height, relief, **kwargs):
        super().__init__(master=window, width=width, height=height, relief=relief, highlightthickness=0, **kwargs)

        self.window = window

        self.width = width
        self.height = height
        self.square_length = int(self.width // 8)

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        self.white = 'silver'  # color representing the white square
        self.black = 'RoyalBlue4'  # color representing the black square

        self.white_piece_objects = self.get_piece_objects('white')
        self.black_piece_objects = self.get_piece_objects('black')

        self.current_white_pieces = {}  # key: image_id, value: white_piece
        self.current_black_pieces = {}  # key: image_id, value: black_piece

        pieces = ['queen', 'rook', 'bishop', 'knight']
        self.promotion_white_images = [(self.get_image(f"chess_pieces/{piece}_white.png"), f"{piece}_white")
                                       for piece in pieces]
        self.promotion_black_images = [(self.get_image(f"chess_pieces/{piece}_black.png"), f"{piece}_black")
                                       for piece in pieces]

        self.squares_dict = {}  # key: square name(e.g a4), value: square_id
        self.pieces = {}  # key: image_id, value: piece object
        self.originals = {}

        self.bind('<Button-1>', self.drag_start)
        self.bind('<B1-Motion>', self.drag_motion)
        self.bind('<ButtonRelease-1>', self.drag_release)
        self.bind('<Button-3>', self.draw_inscribed_ring)

        self.white_moves = []
        self.black_moves = []

        self.game_moves = []
        self.white_turn = True

        self.highlighting_circles = []
        self.clicked_piece = None

        self.checkmate = False
        self.won = None

        self.white_celebration = resize_image('images/white_celebration.jpeg', 400, 300)
        self.black_celebration = resize_image('images/black_celebration.jpeg', 400, 300)

    def grid(self, row, column, **kwargs):
        super().grid(row=row, column=column, **kwargs)
        self._draw_squares()
        self.place_pieces()

    def get_piece_objects(self, color: str) -> list:
        pieces = []
        for piece_path in os.listdir('chess_pieces'):
            name, piece_color = piece_path.rstrip('.png').split('_')
            image = self.get_image(f"chess_pieces/{piece_path}")

            if piece_color == color:
                if name == 'king':
                    pieces.append(King(piece_color, image))
                elif name == 'queen':
                    pieces.append(Queen(piece_color, image))
                elif name == 'rook':
                    pieces.append(Rook(piece_color, image))
                elif name == 'bishop':
                    pieces.append(Bishop(piece_color, image))
                elif name == 'knight':
                    pieces.append(Knight(piece_color, image))
                elif name == 'pawn':
                    pieces.append(Pawn(piece_color, image))

        return pieces

    def _draw_squares(self):
        """Draws the 64 squares with alternating white and dark squares"""
        start_white = True
        for i, num in zip(range(8), self.ranks):  # each rank
            for j, letter in zip(range(8), self.files):  # each file
                x0 = j * self.square_length
                y0 = i * self.square_length
                x1 = x0 + self.square_length
                y1 = y0 + self.square_length

                if start_white:
                    square = self.create_rectangle(x0, y0, x1, y1, fill=self.white, tags=f'{letter}{num}')
                    self.squares_dict[f'{letter}{num}'] = square
                else:
                    square = self.create_rectangle(x0, y0, x1, y1, fill=self.black, tags=f'{letter}{num}')
                    self.squares_dict[f'{letter}{num}'] = square

                start_white = not start_white
            start_white = not start_white

    def put_piece_image(self, image, square_id, tag):
        """Places a piece `image` to the center of the specified `square_id`"""
        x_center, y_center = self.get_centred_coordinates(square_id)

        # place the image
        image_id = self.create_image(x_center, y_center, image=image, tags=tag)
        return image_id

    def place_pieces(self):
        """Puts the chess pieces in their original starting squares.

        For each white or black piece.
            Extract the name, color and image of the piece.
            For each of the piece's starting squares.
                - Place the image of the piece to that starting square
                - Create a new piece object
                - Update the current_square attribute of the piece
                - Append the piece object to its current pieces list
                - Create a new item in the pieces attribute
            """
        # Placing the black pieces
        for black_piece in self.black_piece_objects:
            name, color, image = black_piece.name, black_piece.color, black_piece.image
            for square in black_piece.starting_squares:
                image_id = self.put_piece_image(black_piece.image, self.squares_dict[square],
                                                f'image_in_{self.squares_dict[square]}')
                black_object = self.get_piece(name, color, image)
                black_object.current_square = square

                self.current_black_pieces[image_id] = black_object
                self.pieces[image_id] = black_object

        # Placing the white pieces
        for white_piece in self.white_piece_objects:
            name, color, image = white_piece.name, white_piece.color, white_piece.image
            for square in white_piece.starting_squares:
                image_id = self.put_piece_image(white_piece.image, self.squares_dict[square],
                                                f'image_in_{self.squares_dict[square]}')
                white_object = self.get_piece(name, color, image)
                white_object.current_square = square

                self.current_white_pieces[image_id] = white_object
                self.pieces[image_id] = white_object

    def flip_board(self):
        """
        Flips the board.
        IN PROGRESS
        """
        pass

    def load_position(self):
        """
        Loads a chess position according to the FEN chess notation.
        IN PROGRESS
        """
        pass

    def place_image_on_square(self, image_id: int, square_name: str):
        """
        Places the image_id(image itself) to square_name.
        And updates the tag of the image_id
        """
        square_id = self.squares_dict[square_name]
        x_center, y_center = self.get_centred_coordinates(square_id)

        self.coords(image_id, x_center, y_center)
        self.itemconfig(image_id, tags=f'image_in_{square_id}')

    def new_game(self):
        """Starts a new game with pieces in their original squares.

        Deletes the current pieces in the canvas.
        Adds pieces to their original starting squares
        """
        # delete all the images
        for image_id in self.pieces:
            self.delete(image_id)
        self.pieces = {}
        self.current_black_pieces = {}
        self.current_white_pieces = {}

        self.white_turn = True
        self.white_moves = []
        self.black_moves = []
        self.checkmate = False

        # place the pieces in their starting squares
        self.place_pieces()

    def drag_start(self, event):
        """Function to call when a piece image is clicked"""
        # check to see if the game is over
        if self.checkmate:
            return

        item_clicked = self.find_withtag('current')

        # if no item was clicked, do nothing
        if not item_clicked:
            return

        item = item_clicked[0]  # retrieves the item ID

        # check to see if the item is an image, this avoids a square to be dragged
        # if the item is not of image type, do nothing
        if self.type(item) != 'image':
            self.delete_circles(self.highlighting_circles)
            self.highlighting_circles = []
            return

        # store the original co-ordinates of the image
        self.originals[item] = (event.x, event.y)

        # print the valid moves if there exists valid moves
        image_id = item
        print(f'image_id is: {image_id}')  # TODO delete after testing
        piece = self.pieces[image_id]
        valid_moves = self.generate_correct_piece_moves(piece)

        # check the color of the piece
        piece_color = self.pieces[image_id].color

        if self.white_turn:
            if piece_color == 'black':
                return
        else:  # black's turn
            if piece_color == 'white':
                return

        print(f'piece current square is {piece.current_square}')  # TODO delete this line
        if not valid_moves:
            return

        print(f"correct_moves are : {valid_moves}")  # TODO delete after testing
        if self.highlighting_circles:
            if self.clicked_piece == piece:
                self.delete_circles(self.highlighting_circles)
                self.highlighting_circles = []
            else:
                self.delete_circles(self.highlighting_circles)
                self.highlighting_circles = []
                self.highlight_squares(valid_moves)
        else:
            self.highlight_squares(valid_moves)

        self.clicked_piece = piece

    def drag_motion(self, event):
        """
        Function to call when a piece image is moved.
        1. Checks if an item was clicked.
            if not EXIT
        2. Check if the item is an image.
            if not EXIT
        3. Checks whose turn it is.
            If its white move, black cannot move and vice verser
        """

        if self.checkmate:
            return

        item_clicked = self.find_withtag('current')

        # if no item was clicked, do nothing
        if not item_clicked:
            return

        item = item_clicked[0]  # retrieves the item ID

        # check to see if the item is an image, this avoids a square to be dragged
        # if the item is not of image type, do nothing
        if self.type(item) != 'image':
            # self.delete_circles(self.highlighting_circles)
            # self.highlighting_circles = []
            return

        image_id = item
        piece = self.pieces[image_id]
        piece_color = piece.color

        if self.white_turn:
            if piece_color == 'black':
                return
        else:  # black's turn
            if piece_color == 'white':
                return

        # get the original x and y co-ordinates
        x_origin, y_origin = self.originals[image_id]

        # calculate the new x and y co-ordinates
        x = event.x - x_origin
        y = event.y - y_origin

        # move the item to the new position
        self.move(image_id, x, y)

        # update the original position of the item in the dictionary
        self.originals[image_id] = (event.x, event.y)

        # raise the item above others in the canvas
        self.tag_raise(image_id)

    def drag_release(self, event):
        """Places the image to the square where the cursor is released.

        1. Checks if there was an item that was clicked.
            if not exit
        2. If an item was clicked, verify that it is of image type.
            If not exit
        3. Gets the square_id where the image was dropped
            If the image was not dropped on a square of the board(dropped outside the board)
                - Place the image back to its original square
                - Exit
        4. Get the piece object and the piece valid moves.
            If the square the piece was released was not in its valid moves
                return the piece back to its original square
            Else the move is valid
                Get the current item that exists in that square
                    If current_item_id same as the image_id
                        return the image back to where it was
                        EXIT
                    Else
                        delete that item from the square
                call the `make_move` method
        """
        if self.checkmate:
            return

        item_clicked = self.find_withtag('current')

        # if no item was clicked, do nothing
        if not item_clicked:
            return

        item = item_clicked[0]  # retrieves the item ID

        # check to see if the item is an image, this avoids a square to be dragged
        # if the item is not of image type, do nothing
        if self.type(item) != 'image':
            # self.delete_circles(self.highlighting_circles)
            # self.highlighting_circles = []
            return

        image_id = item
        x, y = event.x, event.y
        square_id = None
        items_id = self.find_overlapping(x, y, x, y)
        print(f'items_id is {items_id}')
        for square in items_id:
            if self.type(square) == 'rectangle':
                square_id = square
                break

        # get the center original square_id of the image
        original_square_id = int(self.gettags(image_id)[0].split('_')[-1])
        x_original, y_original = self.get_centred_coordinates(original_square_id)

        # if the item was released somewhere not in the board, return it to its square
        if not square_id:
            self.coords(image_id, x_original, y_original)
            return

        piece = self.pieces[image_id]
        # piece_valid_moves = self.get_valid_piece_moves(piece)
        piece_valid_moves = self.generate_correct_piece_moves(piece)

        square_name = self.get_square_name(square_id)
        # piece_name = piece.name

        # if the piece is dropped on a square not in its valid moves, return the piece back to its original square
        if square_name not in piece_valid_moves:
            self.coords(image_id, x_original, y_original)
        else:  # the move is valid
            self.make_move(image_id, piece, square_name, square_id)

            # TODO delete after testing
            print(f"white moves: {self.white_moves}")
            print(f"Black moves: {self.black_moves}")

            print('\n\n')

    def make_move(self, image_id, piece, square_name, square_id):
        """
        Gets whose turn it is, the center co-ordinates of the square_id.

        Gets the current_item on that square
        If there exists an item:
            If the item == image_id:
                place the image to where it was originally
                Exit
            Else:
                remove the image_id from the pieces and current_pieces
                deletes that current_item

        If the piece == pawn:
            check whether en-passant is possible and act appropriately

        If the piece == king:
            If the king has not moved and castles is possible, play it

        Places the image_id(image) to the square_name(square).
        Updates the current_square attribute of the piece.
        Adds the square_name to the moves attribute of the piece.

        """
        if self.white_turn:
            turn = 'white'
            opponent = 'black'
            self.white_moves.append(f'{piece.annotation}{square_name}')
        else:
            turn = 'black'
            opponent = 'white'
            self.black_moves.append(f'{piece.annotation}{square_name}')

        # get the center co-ordinates of the square
        x_center, y_center = self.get_centred_coordinates(square_id)

        # get the current item that exists in the square_id
        current_item = self.find_withtag(f'image_in_{square_id}')

        if current_item:
            # if the current_item is the same as the item, the image is released to where it was originally
            if current_item[0] == image_id:
                self.coords(current_item[0], x_center, y_center)  # put the image where it was
                return
            else:
                self.update_current_pieces(turn, current_item[0])  # removes the image_id from current_pieces and pieces
                self.delete(current_item[0])  # delete the current_item

        # check whether an en-passant was played
        if piece.name == 'pawn':
            enpassant_square = self.get_enpassant_square_capture(piece, square_name)
            # if an enpassant move was played, delete the item that was captured
            if enpassant_square:
                print(f'An en-passant move was played on {enpassant_square}')  # TODO delete this line
                captured_square_id = self.squares_dict[enpassant_square]
                captured_piece_id = self.find_withtag(f'image_in_{captured_square_id}')
                self.update_current_pieces(turn, captured_piece_id[0])
                self.delete(captured_piece_id[0])

            file, rank = square_name[0], int(square_name[1])
            if self.white_turn:     # white's turn
                if rank == 8:
                    self.promotion_pawn('white', square_name)
            else:
                if rank == 1:
                    self.promotion_pawn('black', square_name)

        # check whether castles can be played
        if piece.name == 'king':
            if piece.color == 'white':
                king_rank = 1
            else:
                king_rank = 8
            if not piece.moves:
                if square_name == f'c{king_rank}':
                    self.castle(piece.color, 'long_castle')
                    self.delete_circles(self.highlighting_circles)
                    self.highlighting_circles = []
                    self.white_turn = not self.white_turn
                    return
                elif square_name == f'g{king_rank}':
                    self.castle(piece.color, 'short_castle')
                    self.delete_circles(self.highlighting_circles)
                    self.highlighting_circles = []
                    self.white_turn = not self.white_turn
                    return

        # place the image on the square
        self.place_image_on_square(image_id, square_name)

        # update the current square of the piece
        piece.current_square = square_name

        # add the square_name to the piece's moves attribute
        piece.moves.append(square_name)
        print(f"piece moves is: {piece.moves}")  # TODO delete this line after testing

        # check if the opponent's King is in checkmate
        if self.is_checkmate(opponent):
            print("Game Over")
            self.checkmate = True
            self.won = turn
            self.game_over('checkmate', turn)
        else:
            print(f"{opponent} King is not yet checkmated")

        # give the move to the other player
        self.white_turn = not self.white_turn

        self.delete_circles(self.highlighting_circles)
        self.highlighting_circles = []

    def draw_inscribed_ring(self, event):
        """
        Draws an inscribe ring inside a square.
        IN PROGRESS
        """

        pass

    def update_current_pieces(self, turn: str, image_id: int):
        """If a piece is captured -> the image_id of the piece is deleted.
        The image_id will be removed from the pieces attribute of the ChessBoard

        This function deletes the item from the respective current_pieces list.
        If turn == 'white':
            the image_id key will be deleted from current_black_pieces attribute
        Else (its blacks turn)
            the image_id key will be deleted from the current_white_pieces attribute
        """
        del self.pieces[image_id]
        if turn == 'white':
            del self.current_black_pieces[image_id]
        else:
            del self.current_white_pieces[image_id]

    def get_centred_coordinates(self, square_id: int) -> tuple:
        """
        Calculates the centre co-ordinates of the particular square
        :param square_id: unique id of the square
        :return: (x_center, y_center) the centre co-ordinates of the square
        """
        x0, y0, x1, y1 = self.coords(square_id)

        x_center = (x0 + x1) // 2
        y_center = (y0 + y1) // 2

        return x_center, y_center

    def get_square_name(self, square_id: int) -> str:
        """returns the name of a particular square given its square_id"""
        for square_name, value in self.squares_dict.items():
            if square_id == value:
                return square_name

    def highlight_squares(self, squares: list):
        """Given a list of square_name's, the squares are highlighted by a small circle."""
        for square in squares:
            square_id = self.squares_dict[square]
            x0_s, y0_s, x1_s, y1_s = self.coords(square_id)
            x0, y0, x1, y1, = x0_s + 40, y0_s + 40, x1_s - 40, y1_s - 40

            circle = self.create_oval(x0, y0, x1, y1, fill='azure4')
            self.highlighting_circles.append(circle)

    def highlight_king_check(self, king_square: str):
        """
        Highlights the square the King is in if the King is in check.
        IN PROGRESS.
        """
        king_square_id = self.squares_dict[king_square]
        # self.cre
        pass

    def delete_circles(self, circles: list):
        """
        Given a list of tkinter canvas circles, this functions deletes them.
        """
        if circles:
            for circle in circles:
                self.delete(circle)

    def get_king_object(self, color: str):
        """Gets the King object of a particular `color`"""
        if color == 'white':
            for white_piece in self.current_white_pieces.values():
                if white_piece.name == 'king':
                    return white_piece
        else:
            for black_piece in self.current_black_pieces.values():
                if black_piece.name == 'king':
                    return black_piece

    def get_valid_piece_moves(self, piece):
        """Checks the piece's possible moves, scans the board and returns the piece's valid moves.

        If piece is King:
            -`generate_valid_moves` method returns a list(possible moves)
            1. For each of the possible moves
                If that square contains a piece with the same color
                    don't include the move

        Elif piece is Knight:
            -`generate_valid_moves` method returns a list(possible moves).
            1. For each of the possible moves, check if there is a piece of the same color at that square.
            2. If there is a piece of the same color, delete that move(invalid move).

        Elif piece is Queen | Rook | Bishop:
            -`generate_valid_moves` method returns a dict(key(direction), value(list(possible moves in that direction)).

            1. For each direction's possible move:
                If that square contains a piece of the same color.
                    include the moves up to the previous square
                Elif the square contains an enemy piece(different color piece).
                    include the moves up to that square (enemy piece can be captured)

        Else (piece is Pawn):
            -`generate_valid_moves` method returns a list.

            1. For each possible move:
                If that square contains any piece(of any color).
                    delete that move
            2. Check the diagonal square to the left and right.
                If that square contains an enemy piece.
                    include the move
                Else
                    don't include that move
            3. If the pawn is on the 5th rank(white) or 4th rank(black):
                Check if there is an enemy pawn to the left or right.
                    If the enemy pawn has made one move
                        the pawn can move diagonally to that direction.
        """
        name = piece.name
        color = piece.color

        valid_moves = []
        if name == 'king':
            possible_moves = piece.generate_valid_moves()
            for move in possible_moves:
                # check to see if there exists a piece on that square
                square_id = self.squares_dict[move]
                item = self.find_withtag(f'image_in_{square_id}')

                if item:
                    image_id = item[0]
                    another_piece = self.pieces[image_id]

                    # check to see the color of the other piece
                    if another_piece.color == color:
                        continue
                valid_moves.append(move)

        elif name == 'knight':
            possible_moves = piece.generate_valid_moves()
            for move in possible_moves:
                # check to see if there exists a piece on that square
                square_id = self.squares_dict[move]
                item = self.find_withtag(f'image_in_{square_id}')

                if item:
                    image_id = item[0]
                    another_piece = self.pieces[image_id]

                    # check to see the color of the other piece
                    if another_piece.color == color:
                        continue

                valid_moves.append(move)
        elif name == 'queen' or name == 'rook' or name == 'bishop':
            possible_moves = piece.generate_valid_moves()
            for direction in possible_moves.values():
                if direction:
                    for move in direction:
                        # check to see a piece exists in that square
                        square_id = self.squares_dict[move]
                        item = self.find_withtag(f'image_in_{square_id}')

                        if item:
                            image_id = item[0]
                            another_piece = self.pieces[image_id]

                            # check to see the color of the other piece
                            if another_piece.color == color:
                                break
                            else:  # the other piece is of different color
                                valid_moves.append(move)
                                break
                        valid_moves.append(move)
        else:  # the piece is a pawn
            current_square = piece.current_square
            file, rank = current_square[0], int(current_square[1])

            possible_moves = piece.generate_valid_moves()
            for move in possible_moves:
                # check to see if there is any piece in that square
                square_id = self.squares_dict[move]
                item = self.find_withtag(f'image_in_{square_id}')

                if item:
                    continue
                valid_moves.append(move)

            if color == 'white':
                ranks = [3, 4, 5, 6, 7, 8]
                files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

                # check to the left or right diagonal

                left_file = chr(ord(file) - 1) if chr(ord(file) - 1) in files else None
                right_file = chr(ord(file) + 1) if chr(ord(file) + 1) in files else None

                l_diagonal = f'{left_file}{rank + 1}' if left_file and (rank + 1) in ranks else None
                r_diagonal = f'{right_file}{rank + 1}' if right_file and (rank + 1) in ranks else None

                if rank == 5:  # enforcing the en-passant rule

                    # check to see if there is an enemy pawn to the left or right
                    left = f'{left_file}{rank}' if left_file else None
                    right = f'{right_file}{rank}' if right_file else None

                    if left:
                        square_id = self.squares_dict[left]
                        item = self.find_withtag(f'image_in_{square_id}')

                        if item:
                            another_piece = self.pieces[item[0]]
                            if another_piece.color == 'black' and another_piece.name == 'pawn' \
                                    and len(another_piece.moves) == 1 and self.black_moves[-1] == left:
                                valid_moves.append(l_diagonal)

                    if right:
                        square_id = self.squares_dict[right]
                        item = self.find_withtag(f'image_in_{square_id}')

                        if item:
                            another_piece = self.pieces[item[0]]
                            if another_piece.color == 'black' and another_piece.name == 'pawn' \
                                    and len(another_piece.moves) == 1 and self.black_moves[-1] == right:
                                valid_moves.append(r_diagonal)

                # check if left and right diagonal have pieces(for capture) of opposite color
                if l_diagonal:
                    square_id = self.squares_dict[l_diagonal]
                    item = self.find_withtag(f'image_in_{square_id}')

                    if item:
                        another_piece = self.pieces[item[0]]
                        if another_piece.color == 'black':
                            valid_moves.append(l_diagonal)
                if r_diagonal:
                    square_id = self.squares_dict[r_diagonal]
                    item = self.find_withtag(f'image_in_{square_id}')

                    if item:
                        another_piece = self.pieces[item[0]]
                        if another_piece.color == 'black':
                            valid_moves.append(r_diagonal)

            else:  # piece color is black
                ranks = [6, 5, 4, 3, 2, 1]
                files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

                left_file = chr(ord(file) - 1) if chr(ord(file) - 1) in files else None
                right_file = chr(ord(file) + 1) if chr(ord(file) + 1) in files else None

                l_diagonal = f'{left_file}{rank - 1}' if left_file and (rank - 1) in ranks else None
                r_diagonal = f'{right_file}{rank - 1}' if right_file and (rank - 1) in ranks else None

                if rank == 4:  # enforcing en passant rule

                    # check to see if there is an enemy pawn to the left or right
                    left = f'{left_file}{rank}' if left_file else None
                    right = f'{right_file}{rank}' if right_file else None

                    if left:  # there is a left square
                        square_id = self.squares_dict[left]
                        item = self.find_withtag(f'image_in_{square_id}')

                        if item:
                            another_piece = self.pieces[item[0]]
                            if another_piece.color == 'white' and another_piece.name == 'pawn' \
                                    and len(another_piece.moves) == 1 and self.white_moves[-1] == left:
                                valid_moves.append(l_diagonal)

                    if right:  # is there a right square
                        square_id = self.squares_dict[right]
                        item = self.find_withtag(f'image_in_{square_id}')

                        if item:
                            another_piece = self.pieces[item[0]]
                            if another_piece.color == 'white' and another_piece.name == 'pawn' \
                                    and len(another_piece.moves) == 1 and self.white_moves[-1] == right:
                                valid_moves.append(r_diagonal)

                # check if left and right diagonal have pieces(for capture) of opposite color
                if l_diagonal:
                    square_id = self.squares_dict[l_diagonal]
                    item = self.find_withtag(f'image_in_{square_id}')

                    if item:
                        another_piece = self.pieces[item[0]]
                        if another_piece.color == 'white':
                            valid_moves.append(l_diagonal)
                if r_diagonal:
                    square_id = self.squares_dict[r_diagonal]
                    item = self.find_withtag(f'image_in_{square_id}')

                    if item:
                        another_piece = self.pieces[item[0]]
                        if another_piece.color == 'white':
                            valid_moves.append(r_diagonal)

        return valid_moves

    def generate_correct_piece_moves(self, piece) -> list:
        """Given a piece, this function gets its valid moves.
        Get the color of the enemy
        If piece == king:
            Check for en-passant and act accordingly
            For move in valid_moves:
                If that square is attacked by an enemy piece:
                    do not include the move
                Else:
                    include that move
        Else:

            """
        correct_moves = []
        color, name = piece.color, piece.name
        current_square = piece.current_square

        if color == 'white':
            enemy_color = 'black'
        else:
            enemy_color = 'white'

        if name == 'king':
            if color == 'white':
                r = 1
            else:
                r = 8

            # checking to see if castle is possible
            castle_types = self.can_castle(piece)

            if castle_types:
                print(f'castle_types for {color} are: {castle_types}')  # TODO delete after testing
                for castle_type in castle_types:
                    if castle_type == 'long_castle':
                        correct_moves.append(f'c{r}')
                    elif castle_type == 'short_castle':
                        correct_moves.append(f'g{r}')

            valid_moves = self.get_valid_piece_moves(piece)
            if valid_moves:
                for move in valid_moves:
                    # check if that square is attacked by the enemy color's color pieces
                    if not self.is_square_attacked(move, enemy_color):
                        correct_moves.append(move)

        else:
            # check if the King is in check
            attacking_pieces = self.is_check(color)

            if not attacking_pieces:  # if the king is not in check return the piece's valid moves
                # check if the piece is pinned
                pinning_piece = self.is_piece_pinned(piece)
                if pinning_piece:
                    pinning_piece_current_square = pinning_piece.current_square

                    # get the squares between our piece and the pinning piece current square
                    squares_between = self.get_in_between_squares(current_square, pinning_piece_current_square)

                    valid_moves = self.get_valid_piece_moves(piece)

                    print(f'Squares between are : {squares_between}')
                    print(f'{name} valid moves are: {valid_moves}')
                    for move in valid_moves:
                        if move in squares_between:
                            print(f'{move} is a correct move')
                            correct_moves.append(move)
                        else:
                            print(f'{move} is not a correct move')
                else:
                    return self.get_valid_piece_moves(piece)
            else:   # there are attacking pieces (King is in check)

                if len(attacking_pieces) > 1:  # if more than 1 piece are attacking the King, the King must move
                    return []

                # if there is only one attacking piece
                attack_piece = attacking_pieces[0]
                attack_piece_current_square, attack_piece_name = attack_piece.current_square, attack_piece.name

                king = self.get_king_object(color)
                king_current_square = king.current_square

                if attack_piece_name == 'knight' or attack_piece_name == 'pawn':
                    valid_moves = self.get_valid_piece_moves(piece)

                    if attack_piece_current_square in valid_moves:
                        correct_moves.append(attack_piece_current_square)

                else:  # attack piece is Queen, Rook or Bishop
                    # get the squares between the attacking piece and the king
                    squares_between = self.get_in_between_squares(king_current_square, attack_piece_current_square)
                    valid_moves = self.get_valid_piece_moves(piece)

                    for move in valid_moves:
                        if move in squares_between:
                            correct_moves.append(move)

        return correct_moves

    def get_enpassant_square_capture(self, piece: Pawn, move):
        """
        Checks if an en-passant move was played.
        If yes -> square that a piece was captured on.
        no -> None
        """
        color = piece.color

        # get the current_square
        current_square = piece.current_square
        file, rank = current_square[0], int(current_square[1])
        move_file, move_rank = move[0], int(move[1])

        valid_moves = self.get_valid_piece_moves(piece)
        item = self.find_withtag(f'image_in_{self.squares_dict[f"{move_file}{rank}"]}')
        if item:
            another_piece_color = self.pieces[item[0]].color
            if another_piece_color == color:
                return

        if color == 'white':
            if rank == 5 and move in valid_moves and item:
                # is there a piece in to the left or right

                return f'{move_file}{rank}'
            else:
                return None
        else:  # color is black
            if rank == 4 and move in valid_moves and item:
                return f'{move_file}{rank}'
            else:
                return None

    def promotion_pawn(self, color: str, square: str):
        """Gives the player the option to select the promotion piece"""

        def button_clicked(piece):
            print(f"Button clicked, Image: {piece}\n\n")
            piece_name, piece_color = piece.split('_')

            pawn = self.find_withtag(f'image_in_{square_id}')[0]
            # remove the pawn from the pieces attribute and the current pieces
            del self.pieces[pawn]
            if color == 'white':
                del self.current_white_pieces[pawn]
            else:
                del self.current_black_pieces[pawn]

            self.delete(pawn)

            # place the new image to the square_id
            image_path = f"chess_pieces/{piece}.png"
            image_object = self.get_image(image_path)

            piece_object = self.get_piece(piece_name, piece_color, image_object)
            piece_object.current_square = square
            image_id = self.put_piece_image(image_object, square_id, f'image_in_{square_id}')

            # add the new piece to the pieces and current pieces attribute
            self.pieces[image_id] = piece_object
            if color == 'white':
                self.current_white_pieces[image_id] = piece_object
            else:
                self.current_black_pieces[image_id] = piece_object

            frame.destroy()

        square_id = self.squares_dict[square]
        x, y = self.get_centred_coordinates(square_id)
        frame = tkinter.Frame(self)

        if color == 'white':
            frame.place(x=x, y=y)
            # create the buttons for white
            for index, (image, name) in enumerate(self.promotion_white_images):
                button = tkinter.Button(frame, image=image, borderwidth=0, highlightthickness=0,
                                        activebackground='brown1', background='gray27',
                                        command=lambda piece=name: button_clicked(piece))
                button.grid(row=index, column=0)
        else:
            frame.place(x=x, y=y-240)
            for index, (image, name) in enumerate(self.promotion_black_images):
                button = tkinter.Button(frame, image=image, borderwidth=0, highlightthickness=0,
                                        activebackground='brown1', background='silver',
                                        command=lambda piece=name: button_clicked(piece))
                button.grid(row=index, column=0)

    def can_castle(self, king: King) -> list:
        """
        Checks if the King can castle.

        For white or black:
            If square a1|a8 has a rook (checking for long castle).
                If the rook has not moved and the King has not moved.
                    If the squares d1(d8), c1(c8), and b1(b8) have pieces
                        castles not possible
                    Else
                        check whether squares e1(e8), d1(d8), c1(c8) and b1(b8) are attacked
                            If attacked:
                                castles not possible
                            Else
                                move c1(c8) is possible(long castle)
            Elif square h1|h8 has a rook (checking for short castle).
                If the rook and king have not moved.
                    If squares f1(f8) and g1(g8) have pieces.
                        short castle not possible
                    Else
                        If squares e1(e8), f1(f8) and g1(g8) are attacked:
                            castles not possible
                        Else
                            move g1(g8) is possible(short castle)
        """
        castle_moves = []
        king_color = king.color
        if king_color == 'white':
            # left_check_squares = ()
            check_color = 'black'
            rank = 1
        else:
            check_color = 'white'
            rank = 8

        # check if the gap squares are empty (e.g. d1, c1 and b1 for white)
        is_gap_left = not self.get_piece_on_square(f'd{rank}') and not self.get_piece_on_square(
            f'c{rank}') and not self.get_piece_on_square(f'b{rank}')
        is_gap_right = not self.get_piece_on_square(f'f{rank}') and not self.get_piece_on_square(f'g{rank}')

        # check whether the left squares of the king are attacked by enemy pieces
        for square in (f'e{rank}', f'd{rank}', f'c{rank}', f'b{rank}'):
            if self.is_square_attacked(square, check_color):
                is_left_square_attacked = True
                break
            else:
                is_left_square_attacked = False

        # check whether the right squares to king are attacked by enemy pieces
        for square in (f'e{rank}', f'f{rank}', f'g{rank}'):
            if self.is_square_attacked(square, check_color):
                is_right_square_attacked = True
                break
            else:
                is_right_square_attacked = False

        # check if there is a rook in a1(a8)
        a_image_id = self.get_piece_on_square(f'a{rank}')
        if a_image_id:
            if self.pieces[a_image_id].name == 'rook':
                a_rook = self.pieces[a_image_id]
                if not king.moves and not a_rook.moves:
                    if is_gap_left and not is_left_square_attacked:
                        castle_moves.append('long_castle')

        h_image_id = self.get_piece_on_square(f'h{rank}')
        if h_image_id:
            if self.pieces[h_image_id].name == 'rook':
                h_rook = self.pieces[h_image_id]
                if not king.moves and not h_rook.moves:
                    if is_gap_right and not is_right_square_attacked:
                        castle_moves.append('short_castle')
        return castle_moves

    def castle(self, color: str, castle_type: str):
        """
        Makes the move castle.

        If long_castle:
            - Move the king to c1(c8) and the a_rook to d1(d8)
        Else short_castle:
            - Move the king to g1(g8) and the h_rook to f1(f8)
        """
        if color == 'white':
            rank = 1
        else:
            rank = 8

        if castle_type == 'long_castle':
            king_id = self.get_piece_on_square(f'e{rank}')
            a_rook_id = self.get_piece_on_square(f'a{rank}')
            king_piece = self.pieces[king_id]
            a_rook_piece = self.pieces[a_rook_id]

            # move the king to c1(c8)
            self.place_image_on_square(king_id, f'c{rank}')

            # move the a_rook to d1(d8)
            self.place_image_on_square(a_rook_id, f'd{rank}')

            # update the piece's current square and add the move to the piece's moves attribute
            king_piece.current_square = f'c{rank}'
            a_rook_piece.current_square = f'd{rank}'

            king_piece.moves.append(f'c{rank}')
            a_rook_piece.moves.append(f'd{rank}')

        elif castle_type == 'short_castle':
            king_id = self.get_piece_on_square(f'e{rank}')
            h_rook_id = self.get_piece_on_square(f'h{rank}')
            king_piece = self.pieces[king_id]
            h_rook_piece = self.pieces[h_rook_id]

            # move the king to g1(g8)
            self.place_image_on_square(king_id, f'g{rank}')

            # move the h_rook to f1(f8)
            self.place_image_on_square(h_rook_id, f'f{rank}')

            # update the piece's current square and add the move to the piece's moves attribute
            king_piece.current_square = f'g{rank}'
            h_rook_piece.current_square = f'f{rank}'

            king_piece.moves.append(f'g{rank}')
            h_rook_piece.moves.append(f'f{rank}')

    def get_piece_on_square(self, square_name: str):
        """
        Given a square name(e.g. a4), this functions checks if there is a piece on that square.

        If a piece exists
            return the image_id of the piece
        Else
            return None
            """
        square_id = self.squares_dict[square_name]
        item = self.find_withtag(f'image_in_{square_id}')

        if item:
            return item[0]
        else:
            return None

    def is_check(self, color: str):
        """Checks whether the King of color `color` is in check(or attacked).

        If color == 'white':
            Get the appropriate king object
            For every black piece:
                check the valid moves of the piece

                For every valid move:
                    If the king's current square == valid move:
                        return attacking pieces

        Else: (color == 'black')
            Get the appropriate king object
            For every white piece:
                get the valid moves of the piece

                For every valid move:
                    If the king's current square == valid move:
                        return attacking pieces
        """
        king = None
        if color == 'white':
            for piece in self.current_white_pieces.values():
                if piece.name == 'king':
                    king = piece
                    break

            king_current_square = king.current_square

            attacking_pieces = self.is_square_attacked(king_current_square, 'black')

            if attacking_pieces:
                return attacking_pieces

        else:
            for piece in self.current_black_pieces.values():
                if piece.name == 'king':
                    king = piece
                    break

            king_current_square = king.current_square

            attacking_pieces = self.is_square_attacked(king_current_square, 'white')
            if attacking_pieces:
                return attacking_pieces

    def is_square_attacked(self, square_name: str, color: str) -> list:
        """Checks whether the `square_name` is attacked by the `color` player.
        This function checks for pieces other than the King piece.

        If color == 'white': (check whether a white piece is attacking the `square_name`)
            For each white piece:
                If piece is pawn:
                    check for diagonal squares
                    if square_name == diagonal squares (the pawn is attacking the square)
                        append the piece to the list
                Else:
                    get the piece valid moves
                    For each valid move:
                        If valid move == square name:
                            append the attacking piece to the list
        Else: (color == 'black')
            repeat the same steps as done if color == 'white'

        :return `list` containing attacking pieces
        """
        attacking_pieces = []

        if color == 'white':
            for white_piece in self.current_white_pieces.values():
                if white_piece.name == 'pawn':
                    current_square = white_piece.current_square
                    file, rank = current_square[0], int(current_square[1])
                    left_file = chr(ord(file) - 1) if chr(ord(file) - 1) in self.files else None
                    right_file = chr(ord(file) + 1) if chr(ord(file) + 1) in self.files else None

                    up_rank = rank + 1 if (rank + 1) in self.ranks else None

                    if square_name in (f'{left_file}{up_rank}', f'{right_file}{up_rank}'):
                        attacking_pieces.append(white_piece)
                elif white_piece.name == 'king' or white_piece.name == 'knight':
                    possible_moves = white_piece.generate_valid_moves()
                    for move in possible_moves:
                        if square_name == move:
                            attacking_pieces.append(white_piece)
                elif white_piece.name == 'queen' or white_piece.name == 'rook' or white_piece.name == 'bishop':
                    possible_moves = white_piece.generate_valid_moves()
                    for direction in possible_moves.values():
                        if direction:
                            for move in direction:
                                # check to see a piece exists in that square
                                square_id = self.squares_dict[move]
                                item = self.find_withtag(f'image_in_{square_id}')

                                if item:    # there is a piece in the square
                                    another_piece = self.pieces[item[0]]

                                    if square_name != move:
                                        # If the King is in the way and the square is not move, check remaining moves
                                        if another_piece.color != 'white' and another_piece.name == 'king':
                                            continue
                                        break

                                    attacking_pieces.append(white_piece)
                                    break
                                else:   # the square is empty
                                    if square_name != move:
                                        continue

                                    attacking_pieces.append(white_piece)

        else:  # color is black
            for black_piece in self.current_black_pieces.values():
                if black_piece.name == 'pawn':
                    current_square = black_piece.current_square
                    file, rank = current_square[0], int(current_square[1])
                    left_file = chr(ord(file) - 1) if chr(ord(file) - 1) in self.files else None
                    right_file = chr(ord(file) + 1) if chr(ord(file) + 1) in self.files else None

                    down_rank = rank - 1 if (rank - 1) in self.ranks else None

                    if square_name in (f'{left_file}{down_rank}', f'{right_file}{down_rank}'):
                        attacking_pieces.append(black_piece)
                elif black_piece.name == 'king' or black_piece.name == 'knight':
                    possible_moves = black_piece.generate_valid_moves()
                    for move in possible_moves:
                        if square_name == move:
                            attacking_pieces.append(black_piece)
                elif black_piece.name == 'queen' or black_piece.name == 'rook' or black_piece.name == 'bishop':
                    possible_moves = black_piece.generate_valid_moves()
                    for direction in possible_moves.values():
                        if direction:
                            for move in direction:
                                # check to see a piece exists in that square
                                square_id = self.squares_dict[move]
                                item = self.find_withtag(f'image_in_{square_id}')

                                if item:
                                    another_piece = self.pieces[item[0]]

                                    if square_name != move:
                                        # if the king is in the way, the squares after are also attacked
                                        if another_piece.color != 'black' and another_piece.name == 'king':
                                            continue
                                        break

                                    attacking_pieces.append(black_piece)
                                    break
                                else:
                                    if square_name != move:
                                        continue

                                    attacking_pieces.append(black_piece)

        return attacking_pieces

    def is_piece_pinned(self, piece):
        """
        Checks if a particular piece is pinned by an enemy Queen, Rook or Bishop.

        Checks if the piece stands in between the enemy's Queen, Rook or Bishop and the piece's color King.
        return: the enemy piece pinning the piece
        """
        current_square = piece.current_square
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # ranks = [8, 7, 6, 5, 4, 3, 2, 1]

        file, rank = current_square[0], int(current_square[1])
        files_left = files[:files.index(file)][::-1]
        files_right = files[files.index(file) + 1:]

        if rank == 8:
            ranks_up = []
            ranks_down = list(range(7, 0, -1))
        elif rank == 1:
            ranks_up = list(range(2, 9))
            ranks_down = []
        else:
            ranks_up = list(range(rank + 1, 9))
            ranks_down = list(range(rank - 1, 0, -1))

        ne = [f'{letter}{num}' for letter, num in zip(files_right, ranks_up)]
        e = [f'{letter}{rank}' for letter in files_right]
        se = [f'{letter}{num}' for letter, num in zip(files_right, ranks_down)]
        s = [f'{file}{num}' for num in ranks_down]
        sw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_down)]
        w = [f'{letter}{rank}' for letter in files_left]
        nw = [f'{letter}{num}' for letter, num in zip(files_left, ranks_up)]
        n = [f'{file}{num}' for num in ranks_up]

        color = piece.color
        if color == 'white':
            enemy_color = 'black'
        else:
            enemy_color = 'white'

        if n and s:  # if there are squares to the north and to the south of the piece
            if self.is_piece_in_list('king', color, n) and self.is_piece_in_list('queen', enemy_color, s):
                return self.is_piece_in_list('queen', enemy_color, s)

            elif self.is_piece_in_list('king', color, n) and self.is_piece_in_list('rook', enemy_color, s):
                return self.is_piece_in_list('rook', enemy_color, s)

            elif self.is_piece_in_list('king', color, s) and self.is_piece_in_list('queen', enemy_color, n):
                return self.is_piece_in_list('queen', enemy_color, n)

            elif self.is_piece_in_list('king', color, s) and self.is_piece_in_list('rook', enemy_color, n):
                return self.is_piece_in_list('rook', enemy_color, n)

        if e and w:  # if there are squares to the east and west of the piece
            if self.is_piece_in_list('king', color, e) and self.is_piece_in_list('queen', enemy_color, w):
                return self.is_piece_in_list('queen', enemy_color, w)

            elif self.is_piece_in_list('king', color, e) and self.is_piece_in_list('rook', enemy_color, w):
                return self.is_piece_in_list('rook', enemy_color, w)

            elif self.is_piece_in_list('king', color, w) and self.is_piece_in_list('queen', enemy_color, e):
                return self.is_piece_in_list('queen', enemy_color, e)

            elif self.is_piece_in_list('king', color, w) and self.is_piece_in_list('rook', enemy_color, e):
                return self.is_piece_in_list('rook', enemy_color, e)

        if ne and sw:  # if there are squares to the north-east and south-west of the piece
            if self.is_piece_in_list('king', color, ne) and self.is_piece_in_list('queen', enemy_color, sw):
                return self.is_piece_in_list('queen', enemy_color, sw)

            elif self.is_piece_in_list('king', color, ne) and self.is_piece_in_list('bishop', enemy_color, sw):
                return self.is_piece_in_list('bishop', enemy_color, sw)

            elif self.is_piece_in_list('king', color, sw) and self.is_piece_in_list('queen', enemy_color, ne):
                return self.is_piece_in_list('queen', enemy_color, ne)

            elif self.is_piece_in_list('king', color, sw) and self.is_piece_in_list('bishop', enemy_color, ne):
                return self.is_piece_in_list('bishop', enemy_color, ne)

        if nw and se:  # if there are squares to the north-west and south-east of the piece
            if self.is_piece_in_list('king', color, nw) and self.is_piece_in_list('queen', enemy_color, se):
                return self.is_piece_in_list('queen', enemy_color, se)

            elif self.is_piece_in_list('king', color, nw) and self.is_piece_in_list('bishop', enemy_color, se):
                return self.is_piece_in_list('bishop', enemy_color, se)

            elif self.is_piece_in_list('king', color, se) and self.is_piece_in_list('queen', enemy_color, nw):
                return self.is_piece_in_list('queen', enemy_color, nw)

            elif self.is_piece_in_list('king', color, se) and self.is_piece_in_list('bishop', enemy_color, nw):
                return self.is_piece_in_list('bishop', enemy_color, nw)

    def is_piece_in_list(self, name: str, color: str, squares: list):
        """
        Checks if there is a `color` piece `name` in the `squares` list provided
        :param name: name of the piece object
        :param color: color of the piece object
        :param squares: list of square names
        :return: boolean value whether the piece was found
        """
        for square in squares:
            # check to see if there is an item on the square
            square_id = self.squares_dict[square]
            item = self.find_withtag(f'image_in_{square_id}')

            if item:
                piece_id = item[0]
                piece = self.pieces[piece_id]

                if piece.color != color:  # the piece color is not the color we are searching for
                    return None
                else:  # it is color we are searching for
                    if piece.name != name:  # not the piece we are looking for
                        return None
                    else:  # the correct piece is found
                        return piece

        return None  # no item was found in the squares list

    def is_checkmate(self, color: str):
        """Checks if the King of `color` is checkmated

        1. Check if the King is in check
            If True:
                Check if there are any correct moves for any of the pieces
                    If not, the King is checkmated
                Else:
                    The King is not checkmated
            Else:
                The King is not checkmated
                """
        if self.is_check(color):
            if color == 'white':
                for white_piece in self.current_white_pieces.values():
                    correct_moves = self.generate_correct_piece_moves(white_piece)

                    if correct_moves:
                        return False

                return True     # executes if no correct moves were found for any piece
            else:
                for black_piece in self.current_black_pieces.values():
                    correct_moves = self.generate_correct_piece_moves(black_piece)

                    if correct_moves:
                        return False

                return True

    def is_stalemate(self, color: str):
        """Checks if the `color` player is in stalemate.

        A stalemate occurs when the `color` King is not in check and there are no valid moves for any of the `color`
        pieces

        If stalemate -> True
        Else -> False
        """
        if not self.is_check(color):
            if color == 'white':
                for white_piece in self.current_white_pieces.values():
                    correct_moves = self.generate_correct_piece_moves(white_piece)

                    if correct_moves:
                        return False

                return True     # executes if no correct moves were found for any piece
            else:
                for black_piece in self.current_black_pieces.values():
                    correct_moves = self.generate_correct_piece_moves(black_piece)

                    if correct_moves:
                        return False

                return True

    def check_game_state(self):
        """
        Checks the state of the game(stalemate, checkmate or draw).
        IN PROGRESS.
        """
        pass

    def game_over(self, state: str, color: str):
        """Prints who won the game or if the game is in stalemate"""

        def start_new_game():
            self.new_game()
            frame.destroy()

        square_id = self.squares_dict['a8']
        x, y = self.get_centred_coordinates(square_id)

        frame = tkinter.Frame(self, background='grey22')
        frame.place(x=x, y=y)

        if self.won == 'white':
            picture_label = tkinter.Label(frame, image=self.white_celebration)
            picture_label.grid(row=0, column=0, columnspan=2, sticky='news')
        else:
            picture_label = tkinter.Label(frame, image=self.black_celebration)
            picture_label.grid(row=0, column=0, columnspan=2, sticky='news')

        label = tkinter.Label(frame, text=f"{color.capitalize()} Player Wins by {state}",
                              font=('Arial', 16), background='grey22', fg='LightGreen')
        label.grid(row=1, column=0, columnspan=2, pady=20)

        new_game_button = tkinter.Button(frame, text='New Game', command=start_new_game)
        new_game_button.grid(row=2, column=0, pady=20)

        quit_frame_button = tkinter.Button(frame, text='quit', command=frame.destroy)
        quit_frame_button.grid(row=2, column=1, pady=20)


def resize_image(image_path, width, height):
    """Return a resized image object"""
    image = Image.open(image_path)

    return ImageTk.PhotoImage(image.resize((width, height)))


if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.title("Board")
    main_window.configure(bg='grey22')

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    main_window.geometry('800x600')

    background = resize_image('images/chess_background.jpeg', WINDOW_WIDTH, WINDOW_HEIGHT)
    chess_background = tkinter.Label(main_window, image=background)
    chess_background.place(x=0, y=0)

    # creating the ChessBoard
    BOARD_WIDTH = 480
    BOARD_HEIGHT = 480

    Board = ChessBoard(main_window, relief='sunken', width=BOARD_WIDTH, height=BOARD_HEIGHT)
    Board.grid(row=1, column=0, padx=20, pady=20)

    main_window.mainloop()
