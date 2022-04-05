from tkinter import *
import random


class Square:

    def __init__(self, coords, length, size, state=False, active_col='black', inactive_col='white'):

        self.length = length                   
        self.coords = coords                   
        self.size = size                       
        self.state = state                     
        self.active_colour = active_col        
        self.inactive_colour = inactive_col    

    def rect(self):
        return (self.coords[0]+self.size, self.coords[1]+self.size)

    def inbounds(self, coord):
        (x, y) = coord
        return (x >= 0 and x <= self.length-self.size) and (y >= 0 and y <= self.length-self.size)

    def neighbours(self):
        (x, y) = self.coords
        return list(filter(self.inbounds, [
                    (x-self.size, y+self.size), (x, y+self.size), (x+self.size, y+self.size),
                    (x-self.size, y),                                      (x+self.size, y),
                    (x-self.size, y-self.size), (x, y-self.size), (x+self.size, y-self.size),
                ]))

    def get_colour(self):
        return self.active_colour if self.state else self.inactive_colour


class Grid:

    def __init__(self, length, size, tolerance, active_col='red', inactive_col='grey'):

        self.length = length                   
        self.tolerance = tolerance              
        self.active_col = active_col            
        self.inactive_col = inactive_col        

        self.squares = self.make_squares(size)  

    def make_squares(self, size):
        squares = {}
        for y in range(0, self.length, size):
            for x in range(0, self.length, size):
                if random.random() < self.tolerance:
                    squares[(x, y)] = Square((x, y),
                                             self.length,
                                             size,
                                             active_col=self.active_col,
                                             inactive_col=self.inactive_col)
                else:
                    squares[(x, y)] = Square((x, y),
                                             self.length,
                                             size,
                                             state=True,
                                             active_col=self.active_col,
                                             inactive_col=self.inactive_col)

        return squares

    def set_squares(self, on_coordinates):
        for coord, square in self.squares:
            if coord in on_coordinates:
                square.state = True

    
    def rules(self):
        for coord, square in self.squares.items():
            alive_neighbours = 0
            neighbours = square.neighbours()

            for neighbour in neighbours:
                if self.squares[neighbour].state:
                    alive_neighbours += 1

            if square.state:
                if alive_neighbours < 2:
                    square.state = False
                elif alive_neighbours > 3:
                    square.state = False
                else:
                    continue

            else:
                if alive_neighbours == 3:
                    square.state = True


class App:
    def __init__(self, length, size, tolerance=0.8):

        self.length = length  
        self.size = size      

        if not self.length % self.size == 0:
            raise Exception("Make square bidder please." +
                            "My dear make it to the full screen.")

        self.grid = Grid(self.length, self.size, tolerance, active_col='red', inactive_col = 'grey')

        
        self.root = Tk()

        self.canvas = Canvas(self.root, height=self.length, width=self.length)
        self.canvas.pack()
        self.items = self.update_canvas()
        self.root.after(5, self.refresh_screen)
        self.root.mainloop()

    def refresh_screen(self):
        self.grid.rules()
        self.update_canvas(canvas_done=True, canvas_items=self.items)

        self.root.after(5, self.refresh_screen)

    def update_canvas(self, canvas_done=False, canvas_items={}):

        square_items = self.grid.squares

        
        if not canvas_done:
            for coords, square in square_items.items():
                (b_r_x, b_r_y) = square.rect()  
                (t_l_x, t_l_y) = coords         

                canvas_items[coords] = self.canvas.create_rectangle(t_l_x, t_l_y, b_r_x, b_r_y, fill=square.get_colour())
            return canvas_items

        else:
            if canvas_items:
                for coords, item in canvas_items.items():
                    self.canvas.itemconfig(item, fill=square_items[coords].get_colour())
            else:
                raise ValueError("There is not given canvas_items given for reiterating over canvas squares.")


if __name__ == '__main__':
    app = App(1000, 25, tolerance=0.7)