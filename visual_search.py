import pygame
import math
import sys
from queue import PriorityQueue, Queue



WIDTH= 650

window = pygame.display.set_mode((WIDTH,WIDTH+100))#set display
pygame.display.set_caption("Pathfinding Game")
pygame.init()

WHITE, BLACK, RED, GREEN, BLUE ,PURPLE, ORANGE,GREY,TURQUOISE= (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),(128,0,128),(255,165,0),(128,128,128),(64,224,208)
BFS, DFS, UCS, DIJKSTRA, ASTAR = "BFS", "DFS", "UCS", "DIJKSTRA", "ASTAR"



class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 30)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text = self.font.render(self.text, True, BLACK)
        text_place = text.get_rect(center=self.rect.center)
        window.blit(text, text_place)
        
    def is_over(self, pos):
        return self.rect.collidepoint(pos) 
        
class Draw:
    def __init__(self,row,col,WIDTH,ROWS):
        self.row=row
        self.col=col
        self.WIDTH=WIDTH
        self.total_rows=ROWS
        self.x=col * WIDTH
        self.y=row * WIDTH
        self.color=WHITE #we have not visited this node
        self.neighbors=[]
         
    def get_pos(self):
        return self.row,self.col
    def is_visited(self):
        return self.color==RED #we have visited this node
    def is_open(self):
        return self.color==GREEN
    def is_barrier(self):
        return self.color==BLACK
    def is_start(self):
        return self.color==BLUE
    def is_end(self):
        return self.color==PURPLE
    def reset(self):
        self.color=WHITE
    
    def make_visited(self):
        self.color=RED #we have visited this node
        
    def make_open(self):
        self.color=GREEN
        
    def make_barrier(self):
        self.color=BLACK
        
    def make_start(self):
        self.color=BLUE
        
    def make_end(self):
        self.color=PURPLE
        
    def make_path(self):
        self.color=ORANGE
        
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.WIDTH,self.WIDTH))
    
    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #Down
            self.neighbors.append(grid[self.row+1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #Up
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Right
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self. col > 0 and not grid[self.row][self.col -1 ].is_barrier(): #Left
            self.neighbors.append(grid[self.row][self.col - 1])
    
#this calculates Manhatan distance
def heuristic(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    path=[]
    while current in came_from:
        path.append(current.get_pos())
        current = came_from[current]
        current.make_path()
        draw()
        
    print("Path:")
    print("Start:")
    for i in reversed(path):
        print(f"{i},")
    print("Goal")
    print(f"Lenght: {len(path)} steps")
    
        
def reconstruct_path2(came_from, current, draw):
    path=[]
    while current is not None: 
        path.append(current.get_pos())
        current.make_path()
        current = came_from.get(current)  
    draw()
    
    print("Path:")
    print("Start:")
    for i in reversed(path):
        print(f"{i},")
    print("Goal")
    print(f"Lenght: {len(path)} steps")
 
def astar(draw, grid, start, end): 
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {} #dictionary
    g_score = {spot:float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot:float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    
    open_set_hash = {start} # check if anything is in priority queue
    
    while not open_set.empty(): 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                
        current=open_set.get()[2] #take the actual node
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
            
        draw()
        if current!=start:
            current.make_visited()
            
    return False   

def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    came_from[start] = None

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get() 
        
        if current == end:
            if current in came_from:
                reconstruct_path2(came_from, current, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from and not neighbor.is_visited():  # ensure neighbor isn't visited
                came_from[neighbor] = current
                queue.put(neighbor)
                neighbor.make_open() #we consider it

        draw()
        if current != start:
            current.make_visited()

    return False



def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    came_from[start] = None

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        if current == end:
            if current in came_from:
                reconstruct_path2(came_from, current, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from and not neighbor.is_visited():  # ensure neighbor isn't visited
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_visited()

    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

       
        for neighbor in current.neighbors:
            temp_distance = distance[current] + 1 

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((distance[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_visited()

    if end in came_from:
        reconstruct_path(came_from, end, draw)
    start.make_start()
    end.make_end()
    return True

def ucs(draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))  
        came_from = {}
        cost_so_far = {start: 0}
        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                reconstruct_path(came_from, end, draw)
                start.make_start()
                end.make_end()
                return True

            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + 1 

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((new_cost, count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()
            if current != start:
                current.make_visited()

        return False

def algorithm(draw, grid, start, end,selected_algorithm):
 print(f"Running algorithm: {selected_algorithm}")  
 if selected_algorithm == BFS: 
    bfs(draw, grid, start, end) 
     
 elif selected_algorithm == DFS:
    dfs(draw, grid, start, end)
     
 elif selected_algorithm == UCS:
    ucs(draw, grid, start, end)

 elif selected_algorithm == DIJKSTRA:
    dijkstra(draw, grid, start, end)
    

 elif selected_algorithm == ASTAR:
    astar(draw, grid, start, end)
                    
                    
    
def make_grid(rows,width):
    grid=[]
    CELL_SIZE = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Draw(i, j, CELL_SIZE, rows)
            grid[i].append(spot)
    return grid

def draw_grid(rows,width):
    CELL_SIZE = width // rows
    for i in range(rows):
        pygame.draw.line(window,GREY,(0, i*CELL_SIZE), (width, i*CELL_SIZE))
    for j in range(rows):
        pygame.draw.line(window,GREY,(j*CELL_SIZE, 0),(j*CELL_SIZE, width))
        
def draw(rows, width, window, grid, buttons):
    window.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(window)
    draw_grid(rows, width)
    for button in buttons:
        button.draw(window)
    pygame.display.update()
    
def click_the_position(pos,rows,width):
    CELL_SIZE = width // rows
    y, x = pos
    row = x//CELL_SIZE
    col = y//CELL_SIZE
    
    return row,col
def increase_grid_size(rows):
    return min(rows + 5, 50) 

def decrease_grid_size(rows):
    return max(rows - 5, 5) 

def main(window, width):
    ROWS = 40
    grid = make_grid(ROWS, width)
    button_width = 100
    button_height = 30
    button_spacing = 20
    button_y = width + 20

    
    buttons = [
        Button(20, button_y, button_width, button_height, "BFS", (0, 128, 255)),
        Button(20 + button_width + button_spacing, button_y, button_width, button_height, "DFS", (0, 255, 128)),
        Button(20 + 2 * (button_width + button_spacing), button_y, button_width, button_height, "UCS", (255, 128, 0)),
        Button(20 + 3 * (button_width + button_spacing), button_y, button_width, button_height, "DIJKSTRA", (255, 0, 128)),
        Button(20 + 4 * (button_width + button_spacing), button_y, button_width, button_height, "ASTAR", (128, 0, 255)),
        Button(20, button_y + button_height + button_spacing, button_width+40, button_height, "Increase Size", (0, 255, 255)),
        Button(70 + button_width + button_spacing, button_y + button_height + button_spacing, button_width+40, button_height, "Decrease Size", (255, 255, 0)),
    ]
    
    increase_size_button = buttons[-2] 
    decrease_size_button = buttons[-1]  

    selected_algorithm = None
    start, end = None, None
    running = True
    algorithm_running = True 
    while running:
        draw(ROWS, width, window, grid, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = click_the_position(pos, ROWS, width)
                if 0 <= row < ROWS and 0 <= col < ROWS:  
                    spot = grid[row][col]
                    if not start and spot != end:  
                        start = spot
                        start.make_start()
                    elif not end and spot != start:  
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()

                for button in buttons:
                    if button.is_over(pos):
                        if button.text == "Increase Size":
                            ROWS = increase_grid_size(ROWS)
                            grid = make_grid(ROWS, width) 
                        elif button.text == "Decrease Size":
                            ROWS = decrease_grid_size(ROWS)
                            grid = make_grid(ROWS, width) 
                        else:
                            selected_algorithm = button.text
                            algorithm_running = True  

            elif pygame.mouse.get_pressed()[2]:  
                pos = pygame.mouse.get_pos()
                row, col = click_the_position(pos, ROWS, width)
                if 0 <= row < ROWS and 0 <= col < ROWS:
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start, end = None, None
                    grid = make_grid(ROWS, width)
                    selected_algorithm = None  

        if selected_algorithm and start and end and algorithm_running:
            for row in grid:
                for spot in row:
                    spot.update_neighbors(grid)
            algorithm(lambda: draw(ROWS, width, window, grid, buttons), grid, start, end, selected_algorithm)
            algorithm_running = False
    pygame.quit()


main(window, WIDTH)
