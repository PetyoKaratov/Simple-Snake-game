from tkinter import *
import random

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True
apples = 0

def create_block():
    global BLOCK
    posx = SEG_SIZE * (random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE))
        
    BLOCK = c.create_oval(posx, posy,
                            posx + SEG_SIZE,
                            posy + SEG_SIZE,
                            fill="red")
        
def main():
    global IN_GAME
    global apples
        
    if IN_GAME:
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1,y1,x2,y2 = head_coords
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            apples += 1
            c.delete(BLOCK)
            create_block()
        else:
            for index in range(len(s.segments)-1):
                if c.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False
        root.after(100, main)
    else:
        t = "Game over!\nScore: " + str(apples)
        c.create_text(WIDTH/2, HEIGHT/2,
                      text=t,
                      font="Ariel 20",
                      fill="#ff0000")
   

class Segment():
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="green")
        
class Snake():
    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0,1), "Up": (0,-1), "Left": (-1,0), "Right": (1,0)}
        self.vector = self.mapping["Down"]
        
    def move(self):
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1,y1,x2,y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment,x1,y1,x2,y2)
            
        x1,y1,x2,y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0]*SEG_SIZE,
                 y1 + self.vector[1]*SEG_SIZE,
                 x2 + self.vector[0]*SEG_SIZE,
                 y2 + self.vector[1]*SEG_SIZE)
        
    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
            
    def add_segment(self):
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x,y))
                               
        

root = Tk()

root.title("Python")
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#ffffff")
c.grid()
c.focus_set()
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
s = Snake(segments)
c.bind("<KeyPress>", s.change_direction)
create_block()
main()

root.mainloop()