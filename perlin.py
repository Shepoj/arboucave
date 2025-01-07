import random
import math


def generate_gradients(grid_size):
    gradients = {}
    for y in range(grid_size):
        for x in range(grid_size):
            angle = random.uniform(0, 2 * math.pi)
            gradients[(x, y)] = (math.cos(angle), math.sin(angle))
    return gradients


def fade(t):
    return (t**3)*(t*(t*6-15)+10)


def lerp(a,b,t):
    return a+t*(b-a)


def dot(grad,x,y):
    return grad[0]*x+grad[1]*y

def perlin_noise(x, y, gradients, grid_size):
    X = int(x) % grid_size
    Y = int(y) % grid_size
    x_offset = x - int(x)
    y_offset = y - int(y)
    grad00 = gradients[(X, Y)]
    grad01 = gradients[(X, (Y + 1) % grid_size)]  
    grad10 = gradients[((X + 1) % grid_size, Y)]  
    grad11 = gradients[((X + 1) % grid_size, (Y + 1) % grid_size)] 
    pt00 = dot(grad00, x_offset, y_offset)
    pt01 = dot(grad01, x_offset, y_offset - 1)
    pt10 = dot(grad10, x_offset - 1, y_offset)
    pt11 = dot(grad11, x_offset - 1, y_offset - 1)
    
    u = fade(x_offset)
    v = fade(y_offset)
    
    x0 = lerp(pt00, pt10, u)
    x1 = lerp(pt01, pt11, u)
    
    return lerp(x0, x1, v)

def generate_perlin_grid(width, height, grid_size, ampli) -> list[list[float]]:
    gradients = generate_gradients(grid_size)
    
    grid = []
    for x in range(width):
        row = []
        for y in range(height):
            value = perlin_noise(x * 0.1, y * 0.1, gradients, grid_size)  
            amplified = value * ampli
            row.append(amplified)
        grid.append(row)
    
    return grid