import pygame
import random
import math
pygame.init()

class DrawInformation:
        BLACK = 0,0,0
        WHITE =252, 195, 237
        GREEN = 0,255,0
        BLUE = 0,0,255
        RED = 255,0,0
        GREY = 128,128,128
        BACKGROUND_COLOR = WHITE

        GRADIENTS = [
            (62,149,223),
            (153,200,241),
            (10,74,129)
        ]
        SIDE_PAD = 100
        TOP_PAD = 160
        FONT = pygame.font.SysFont('calibri',30)
        LARGE_FONT = pygame.font.SysFont('timesnewroman', 40)


        def __init__(self,width,height,lst):
            self.width = width
            self.height = height
            self.window = pygame.display.set_mode((width,height))
            pygame.display.set_caption("Sorting Algorithm and Visualizations")
            self.set_list(lst)
        def set_list(self,lst):
            self.lst = lst
            self.min_val = min(lst)
            self.max_val = max(lst)
            self.block_width = round((self.width - self.SIDE_PAD)/len(lst))
            self.block_height = math.floor((self.height - self.TOP_PAD)/(self.max_val-self.min_val))
            self.start_x = self.SIDE_PAD//2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                     draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))


    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending ",1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2,50))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Shell Sort", 1 ,draw_info.RED)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 86))
    draw_list(draw_info)

    pygame.display.update()

def draw_list(draw_info,color_positions={}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width- draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i,val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * (draw_info.block_height)

        color = draw_info.GRADIENTS[i%3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x,y,draw_info.block_width,draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_list(n, min_val, max_val ):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(n):
        for j in range(0,n-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1>num2 and ascending) or (num1 < num2 and not ascending):
                lst[j] = num2
                lst[j+1] = num1
                draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)
                yield True
    # next()

def shellSort(draw_info, ascending = True):
    lst = draw_info.lst
    gap = len(lst) // 2  # initialize the gap
    while gap > 0:
        i = 0
        j = gap

        # check the lstay in from left to right
        # till the last possible index of j
        while j < len(lst):

            if(lst[i] > lst[j] and ascending) or (lst[i] < lst[j] and not ascending):
                lst[i], lst[j] = lst[j], lst[i]

            i += 1
            j += 1

            # now, we look back from ith index to the left
            # we swap the values which are not in the right order.
            k = i
            while k - gap > -1:

                if lst[k - gap] > lst[k]:
                    lst[k - gap], lst[k] = lst[k], lst[k - gap]
                    draw_list(draw_info, {k - gap: draw_info.GREEN, k: draw_info.RED}, True)
                    yield True
                k -= 1
        gap //= 2
    return lst
def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i> 0 and lst[i-1]>current and ascending
            descending_sort = i> 0 and lst[i-1]<current and not ascending

            if not ascending_sort  and not descending_sort:
                break
            lst[i] = lst[i-1]
            i=i-1
            lst[i] = current
            draw_list(draw_info,{i:draw_info.GREEN,i-1:draw_info.RED},True)
            yield True
    return lst



def main():
    run = True
    clock = pygame.time.Clock()

    n=50
    min_val = 0
    max_val = 100
    lst = generate_list(n,min_val,max_val)
    draw_info = DrawInformation(1000,800,lst)
    sorting = False
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    ascending = True
    descending = False
    while(run):
        clock.tick(10)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting=False
        else:
            draw(draw_info,sorting_algo_name,ascending)


        # clock.tick(60)
        # draw(draw_info)
        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending=True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and sorting == False:
                sorting_algorithm = shellSort
                sorting_algo_name = "Shell Sort"

    pygame.quit()
if __name__ == "__main__":
    main()



