import pygame
from display import Window, TextBox, SlideBox, DropdownBox, ButtonBox
from algs import algorithmsDict
from random import randint
import time
import math

# Initialize pygame modules
pygame.init()

# Font
baseFont = pygame.font.SysFont('Arial', 24)

# Colors
grey = (100, 100, 100)
green = (125, 240, 125)
white = (250, 250, 250)
red = (255, 50, 50)
black = (0, 0, 0)
blue = (50, 50, 255)

pygame.display.set_caption('Sorting Algorithms Visualizer')
screen = pygame.display.set_mode((900, 500))
window = Window(screen)

# Load images and get their sizes
slow_image = pygame.image.load('res/button_slow.png')
slow_width, slow_height = slow_image.get_size()

normal_image = pygame.image.load('res/button_normal.png')
normal_width, normal_height = normal_image.get_size()

fast_image = pygame.image.load('res/button_fast.png')
fast_width, fast_height = fast_image.get_size()

window.add_widget(
    widget_id = 'size_input',
    widget = TextBox((30, 440, 100, 50), 'Size', grey, baseFont, '100')
)
window.add_widget(
    widget_id = 'algorithm_input',
    widget = DropdownBox((140, 440, 200, 50), 'Algorithm', grey, baseFont, list(algorithmsDict.keys()), white)
)
window.add_widget(
    widget_id = 'play_button',
    widget = ButtonBox((350, 440, 40, 40), 'res/playButton.png', 'res/stopButton.png')
)
# Positions for speed buttons
slow_x = 425
normal_x = slow_x + slow_width + 20  # 20 pixels spacing
fast_x = normal_x + normal_width + 20

# Add speed buttons with accurate dimensions
window.add_widget(
    widget_id='slow_button',
    widget=ButtonBox((slow_x, 438, slow_width, slow_height), 'res/button_slow.png', 'res/button_slow.png')
)
window.add_widget(
    widget_id='normal_button',
    widget=ButtonBox((normal_x, 438, normal_width, normal_height), 'res/button_normal.png', 'res/button_normal.png')
)
window.add_widget(
    widget_id='fast_button',
    widget=ButtonBox((fast_x, 438, fast_width, fast_height), 'res/button_fast.png', 'res/button_fast.png')
)

def drawBars(screen, array, redBar1, redBar2, blueBar1, blueBar2, greenRows = {}):
    '''Draw the bars and control their colors'''
    numBars = len(array)
    if numBars != 0:
        bar_width  = 900 / numBars
        ceil_width = math.ceil(bar_width)

    for num in range(numBars):
        if   num in (redBar1, redBar2)  : color = red
        elif num in (blueBar1, blueBar2): color = blue
        elif num in greenRows           : color = green        
        else                            : color = grey
        pygame.draw.rect(screen, color, (num * bar_width, 400 - array[num], ceil_width, array[num]))

def main():
    numbers = []
    running = True
    isPlaying = False
    isSorting = False
    sortingIterator = None
    visualDelay = 100  # delay is set to 100 by default
    current_speed = 'normal'

    # speed modes in milliseconds
    speedModes = {
        'slow' : 250,  # delay is set to 200 in slow mode
        'normal' : 100, # delay is set to 100 is normal mode
        'fast' : 20 # delay is set to 20 in fast mode
    }
    
    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            window.update(event)

        # constantly check for mode changes
        if window.get_widget_value('slow_button'):
            if current_speed != 'slow':
                current_speed = 'slow'
                visualDelay = speedModes[current_speed]
                print("slow button is pressed")
        elif window.get_widget_value('normal_button'):
            if current_speed != 'normal':
                current_speed = 'normal'
                visualDelay = speedModes[current_speed]
                print("normal button is pressed")
        elif window.get_widget_value('fast_button'):
            if current_speed != 'fast':
                current_speed = 'fast'
                visualDelay = speedModes[current_speed]
                print("fast button is pressed")

        isPlaying = window.get_widget_value('play_button')
        if isPlaying and not isSorting:
            print("play button is pressed")
            # random list to be sorted
            numBars = int(window.get_widget_value('size_input'))
            numbers = [randint(10, 400) for i in range(numBars)] 

            # initialize sorting iterator
            sortingAlgorithm = window.get_widget_value('algorithm_input')
            sortingIterator = algorithmsDict[sortingAlgorithm](numbers, 0, numBars-1)
            isSorting = True

        if not isPlaying and isSorting:
            current_speed = 'normal'
            visualDelay = speedModes[current_speed]
            isSorting = False


        if isSorting:
            try:
                numbers, redBar1, redBar2, blueBar1, blueBar2 = next(sortingIterator)
                drawBars(screen, numbers, redBar1, redBar2, blueBar1, blueBar2)
                pygame.time.delay(visualDelay)  # control speed of sorting visuals
            except StopIteration:
                isSorting = False
                window.set_widget_value('play_button', False)
        else:
            drawBars(screen, numbers, -1, -1, -1, -1, greenRows=set(range(len(numbers))))

        window.render()
        pygame.display.update()


if __name__ == '__main__':
    main()
