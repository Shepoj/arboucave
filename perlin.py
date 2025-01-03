import random
import math

def precompute_gradients(IXMAX, IYMAX):
    gradients=[[[0,0] for i in range(IXMAX)] for j in range(IYMAX)]
    for i in range(IYMAX):
        for j in range(IXMAX):
            angle = random.uniform(0, 2 * math.pi)
            gradients[i][j][0] = math.cos(angle)
            gradients[i][j][1] = math.sin(angle)
    return gradients
    

def smoothstep(w):
    if (w <= 0.0) :
        return 0.0
    if (w >= 1.0) :
        return 1.0
    return 4*(w-0.5)**(3)+0.5 

def lerp(a, b, w):
    return a + (b - a) * smoothstep(w)

def dotGridGradient(ix, iy, x, y, gradients):
    dx = x - float(ix)
    dy = y - float(iy)
    return (dx*gradients[iy][ix][0] + dy*gradients[iy][ix][1])

def generatePerlin(x,y,gradients):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    sx = x - float(x0)
    sy = y - float(y0)
    n0 = dotGridGradient(x0, y0, x, y, gradients)
    n1 = dotGridGradient(x1, y0, x, y, gradients)
    ix0 = lerp(n0, n1, sx)
    n0 = dotGridGradient(x0, y1, x, y, gradients)
    n1 = dotGridGradient(x1, y1, x, y, gradients)
    ix1 = lerp(n0, n1, sx)
    value = lerp(ix0, ix1, sy)
    return value    

def perlinGrid(xmin, ymin, xmax, ymax, ixmax, iymax):
    gradients = precompute_gradients(ixmax, iymax)
    perlin_noise = [[0 for i in range(ixmax)] for j in range(iymax)]
    for i in range(iymax):
        for j in range(ixmax):
            x = xmin + (xmax - xmin) * float(i) / float(iymax)
            y = ymin + (ymax - ymin) * float(j) / float(ixmax)
            perlin_noise[i][j] = generatePerlin(10*x, 10*y, gradients)
    return perlin_noise
    

#https://github.com/wadefletch/terrain/blob/main/map.py interessant

