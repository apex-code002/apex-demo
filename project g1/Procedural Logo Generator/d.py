import turtle
import random

# 1. Setup the Drawing Canvas
# -----------------------------
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black") # Set background to black for contrast
pen = turtle.Turtle()
pen.hideturtle()       # Make the drawing pen invisible
pen.speed(0)           # Set speed to maximum (fastest drawing)
pen.pensize(2)         # Set pen width

# 2. Main Drawing Loop
# -----------------------------
def draw_spiral_logo(sides, turns, scale):
    """Draws a complex geometric spiral."""
    
    # Calculate the angle needed to make a polygon shape
    angle = 360 / sides 
    
    for i in range(turns * sides):
        # Choose a random color for the segment
        r = random.random()
        g = random.random()
        b = random.random()
        pen.pencolor(r, g, b)
        
        # Move forward, increasing the length slightly each time
        pen.forward(i * scale)
        
        # Turn the initial polygon angle plus a small extra deviation
        # This deviation is what creates the spiral/rotating effect
        pen.right(angle + 1)

# 3. Execute the Drawing
# -----------------------------
# You can change these values to create different logos:
# - 4: for square-like rotation
# - 5: for pentagon-like rotation
# - 6: for hexagon-like rotation
SIDES = 4   # The base number of sides (e.g., 4 for a square)
TURNS = 12  # How many full rotations the shape makes
SCALE = 1.5 # Controls the size and spacing of the spiral

draw_spiral_logo(SIDES, TURNS, SCALE)

# 4. Finish the Program
# -----------------------------
turtle.done()