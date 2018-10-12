# fireworks
#Name:Cheung Yan Shing (20276136)

import random   # module providing the randint function
import time     # time module to delay after drawing five fireworks
import turtle   # turtle module for drawing fireworks

##### Initialize variables used in the program

# The following width and height match the GIF used by the program
screen_width, screen_height = 900, 564

firework_radius = 100   # The maximum radius a firework can have
firework_count = 20     # The number of fireworks to shoot


# A list of colours to choose from for a firework
firework_colours = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "white"]


##### Initialize the turtle module

turtle.reset()                              # Reset the turtle
turtle.setup(screen_width, screen_height)   # Set the size of the screen
turtle.bgpic("hong_kong.gif")               # Put the background image on the
                                            # screen
turtle.width(2)                             # Draw lines with a width of two
turtle.speed(6)
turtle.hideturtle()


##### For loop to shoot individual firework

for i in range(firework_count):
    # Clear the sky (screen) for every five fireworks
    if i > 0 and i % 5 == 0:
        time.sleep(1)
        turtle.clear()
        

    ##### Add your code here
    # Initialize a starting position
    starty = -(screen_height/2)
    startx = random.randint(-(screen_width/2),(screen_width/2))

    turtle.up()
    turtle.goto(startx, starty)
    turtle.down()
    
    # Initialize a destination
    destx = random.randint(-(screen_width/2),(screen_width/2))
    desty = random.randint(0,screen_height/2)
    
    # Shoot a firework from the start to the destination
    turtle.color("yellow")
    turtle.goto(destx, desty)

    turtle.undo()
    turtle.up()
    turtle.goto(destx, desty)


    ##### The turtle is in the sky, explode the firework
    ##### Add your code here
    # Pick a firework color from the firework colour list
    colour = firework_colours[random.randint(0,7)]
    
    # Pick a size for the firework
    size = random.randint(firework_radius/2,firework_radius)
    
    # Pick the number of explosion directions
    no_ex = random.randint(10,20)

    ##### For loop to draw each ring of explosion
    ##### Add your code here
    turtle.up()
    turtle.tracer(False)
    
    circles = 0
    while circles <= (size/10):
        circles= circles + 1
        turtle.setheading(0)
        turtle.forward(10)
        turtle.left(90)
        turtle.color(colour)
        turtle.dot(0.5+circles)
        turtle.up()

        times=0
        while times < no_ex:
            times = times +1 
            turtle.circle(10*circles, 360/no_ex)
            turtle.dot(0.5+circles)
            turtle.up()
            
        turtle.setheading(0)
        turtle.right(90)
        turtle.forward(3.5)
        turtle.setheading(0)


    turtle.update()
    turtle.tracer(True)





turtle.done() # Need to keep the window display up
