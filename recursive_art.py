""" 
author: Rachel Yang

Generates random computational art by using recursion and a given set of mathematical 
functions that have a range between [-1,1] that overlap one another with different color pixels
"""

import random
from PIL import Image
import math

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

	sometimes the doctests will fail (expected x, got y | expected y, got x) because 
	the function randomly chooses either 0 and 1, and will then pick either x or y depending on that

	it's difficult to expect which one the random.randint operator will choose. therefore, 
	I chose not to implement any doctests for this function.
    """
    build_blocks = ["prod","avg","cos_pi","sin_pi","arctan_pi","circle","x","y"]

    if max_depth <= 0:
    	random1 = random.randint(0,1)
    	if random1 == 0:
    		return "x"
    	elif random1 == 1:
    		return "y"
    elif min_depth <= 0:
    	random2 = random.randint(0,1)
    	if random2 == 0:
    		return "x"
    	elif random2 == 1:
    		return "y"
    else:
    	brf = build_random_function(min_depth - 1, max_depth - 1)
    	index = random.randint(0,5)
    	if index <= 5:
    		return [build_blocks[index], brf, brf]
    	if index >= 6:
    		return [build_blocks[index],brf]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod", "x", "y"], -1, 1)
        -1
        >>> evaluate_random_function(["avg", "x", "y"], 1, 2)
        1.5
        >>> evaluate_random_function(["cos_pi", "x"], 1, 2)
        -1.0
        >>> evaluate_random_function(["sin_pi", "x"], 0, 2)
        0.0
        >>> evaluate_random_function(["arctan_pi", "x"], 0.25, 2)
        0.6657737500283538
        >>> evaluate_random_function(["circle", "x", "y"], 1, 2)
        5
    """
    if f[0] == "x":
    	return x
    elif f[0] == "y":
    	return y
    elif f[0] == "prod":
    	return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
    	return 0.5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    elif f[0] == "cos_pi":
    	return math.cos(math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
    	return math.sin(math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "arctan_pi":
    	return math.atan(math.pi * evaluate_random_function(f[1], x, y))
    #elif f[0] == "cot_pi":
    	#return 1 / (math.tan(math.pi * evaluate_random_function(f[1], x, y)))
    #elif f[0] == "squared": 
    	#return (evaluate_random_function(f[1], x, y))**2 + (evaluate_random_function(f[2], x, y))**2
    elif f[0] == "circle":
    	return x**2 + y**2

def remap_interval(val,
                   input_interval_start,                   
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(3, 1, 5, 6, 7)
        6.5
    """
    input_range = float(input_interval_end - input_interval_start)
    output_range = float(output_interval_end - output_interval_start)
    output_value = ((val - input_interval_start)/input_range) * (output_range) + output_interval_start
    return output_value

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
        >>> color_map(-0.3)
        89
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(15, 17)
    green_function = build_random_function(2, 4)
    blue_function = build_random_function(10, 12)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    generate_art("myart40.png")

    # Test that PIL is installed correctly
    # test_image("noise.png")
