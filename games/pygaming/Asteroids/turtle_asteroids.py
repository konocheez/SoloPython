from turtle import *
import tkinter.messagebox
import tkinter
import random
import math

screenMinX = -500
screenMinY = -500
screenMaxX = 500
screenMaxY = 500

class Asteroid(RawTurtle):
    def __init__(self,canvas,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvas)
        self.penup()
        self.goto(x,y)
        self.size = size
        self.dx = dx
        self.dy = dy
        self.shape("rock" + str(size))

    def getSize(self):
        return self.size

    def getDX(self):
        return self.dx

    def getDY(self):
        return self.dy

    def setDX(self,dx):
        self.dx = dx

    def setDY(self,dy):
        self.dy = dy

    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    def getRadius(self):
        return self.size * 10 - 5

class SpaceShip(RawTurtle):
    def __init__(self,canvas,dx,dy,x,y):
        RawTurtle.__init__(self,canvas)
        self.penup()
        self.color("purple")
        self.goto(x,y)
        self.dx = dx
        self.dy = dy
        self.shape("ship")

    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    def fireEngine(self):
        angle = self.heading()
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        self.dx = self.dx + x
        self.dy = self.dy + y

    def getRadius(self):
        return 2

    def getDX(self):
        return self.dx

    def getDY(self):
        return self.dy

def intersect(object1,object2):
        dist = math.sqrt((object1.xcor() - object2.xcor())**2 + (object1.ycor() - object2.ycor())**2)

        radius1 = object1.getRadius()
        radius2 = object2.getRadius()

        # The following if statement could be written as
        # return dist <= radius1+radius2
        if dist <= radius1+radius2:
            return True
        else:
            return False

def main():

    # Start by creating a RawTurtle object for the window.
    root = tkinter.Tk()
    root.title("Asteroids!")
    cv = ScrolledCanvas(root,600,600,600,600)
    cv.pack(side = tkinter.LEFT)
    t = RawTurtle(cv)

    screen = t.getscreen()
    screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
    screen.register_shape("rock3",((-20, -16),(-21, 0), (-20,18),(0,27),(17,15),(25,0),(16,-15),(0,-21)))
    screen.register_shape("rock2",((-15, -10),(-16, 0), (-13,12),(0,19),(12,10),(20,0),(12,-10),(0,-13)))
    screen.register_shape("rock1",((-10,-5),(-12,0),(-8,8),(0,13),(8,6),(14,0),(12,0),(8,-6),(0,-7)))
    screen.register_shape("ship",((-10,-10),(0,-5),(10,-10),(0,10)))
    screen.register_shape("bullet",((-2,-4),(-2,4),(2,4),(2,-4)))
    frame = tkinter.Frame(root)
    frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
    t.ht()

    def quitHandler():
        root.destroy()
        root.quit()

    quitButton = tkinter.Button(frame, text = "Quit", command=quitHandler)
    quitButton.pack()

    screen.tracer(10)

    ship = SpaceShip(cv,0,0,(screenMaxX-screenMinX)/2+screenMinX,(screenMaxY-screenMinY)/2 + screenMinY)

    asteroids = []

    for k in range(5):
        dx = random.random() * 6 - 3
        dy = random.random() * 6 - 3
        x = random.random() * (screenMaxX - screenMinX) + screenMinX
        y = random.random() * (screenMaxY - screenMinY) + screenMinY

        asteroid = Asteroid(cv,dx,dy,x,y,3)

        asteroids.append(asteroid)

    def play():
        # Tell all the elements of the game to move
        ship.move()

        for asteroid in asteroids:
            asteroid.move()

        # Set the timer to go off again in 5 milliseconds
        screen.ontimer(play, 5)

    # Set the timer to go off the first time in 5 milliseconds
    screen.ontimer(play, 5)

    def turnLeft():
        ship.setheading(ship.heading()+7)

    screen.onkeypress(turnLeft,"4")

    def forward():
        ship.fireEngine()

    screen.onkeypress(forward,"5")

    screen.listen()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
