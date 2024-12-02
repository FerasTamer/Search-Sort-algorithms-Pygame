import pygame  
from collections import deque  

# Constants  
WIDTH = 600  
HEIGHT = 600  
ROWS = 30  
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Depth-First Search Path Finding Algorithm")  

# Colors  
COLORS = {  
    "RED": (255, 0, 0),  
    "GREEN": (0, 255, 0),  
    "BLUE": (0, 0, 255),  
    "YELLOW": (255, 255, 0),  
    "WHITE": (255, 255, 255),  
    "BLACK": (0, 0, 0),  
    "PURPLE": (128, 0, 128),  
    "ORANGE": (255, 165, 0),  
    "GREY": (128, 128, 128),  
    "TURQUOISE": (64, 224, 208),  
}  

class Spot:  
    def __init__(self, row: int, col: int, width: int, total_rows: int):  
        self.row = row  
        self.col = col  
        self.x = row * width  
        self.y = col * width  
        self.color = COLORS["WHITE"]  
        self.neighbors = []  
        self.width = width  
        self.total_rows = total_rows  

    def get_pos(self):  
        return self.row, self.col  

    def is_closed(self):  
        return self.color == COLORS["RED"]  

    def is_open(self):  
        return self.color == COLORS["GREEN"]  

    def is_barrier(self):  
        return self.color == COLORS["BLACK"]  

    def is_start(self):  
        return self.color == COLORS["ORANGE"]  

    def is_end(self):  
        return self.color == COLORS["TURQUOISE"]  

    def reset(self):  
        self.color = COLORS["WHITE"]  

    def make_start(self):  
        self.color = COLORS["ORANGE"]  

    def make_closed(self):  
        self.color = COLORS["RED"]  

    def make_open(self):  
        self.color = COLORS["GREEN"]  

    def make_barrier(self):  
        self.color = COLORS["BLACK"]  

    def make_end(self):  
        self.color = COLORS["TURQUOISE"]  

    def make_path(self):  
        self.color = COLORS["PURPLE"]  

    def draw(self, win):  
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  

    def update_neighbors(self, grid):  
        self.neighbors = []  
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN  
            self.neighbors.append(grid[self.row + 1][self.col])  
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP  
            self.neighbors.append(grid[self.row - 1][self.col])  
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT  
            self.neighbors.append(grid[self.row][self.col + 1])  
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT  
            self.neighbors.append(grid[self.row][self.col - 1])  

def reconstruct_path(came_from, current, draw):  
    while current in came_from:  
        current = came_from[current]  
        current.make_path()  
        draw()  

def dfs(draw, grid, start, end):  
    stack = [start]  
    visited = {start}  
    came_from = {}  

    while stack:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  

        current = stack.pop()  

        if current == end:  
            reconstruct_path(came_from, end, draw)  
            end.make_end()  
            return True  

        for neighbor in current.neighbors:  
            if neighbor not in visited and not neighbor.is_barrier():  
                visited.add(neighbor)  
                came_from[neighbor] = current  
                stack.append(neighbor)  
                neighbor.make_open()  

        draw()  

        if current != start:  
            current.make_closed()  

    return False  

def make_grid(rows: int, width: int):  
    grid = []  
    gap = width // rows  
    for i in range(rows):  
        grid.append([])  
        for j in range(rows):  
            spot = Spot(i, j, gap, rows)  
            grid[i].append(spot)  
    return grid  

def draw_grid(win, rows: int, width: int):  
    gap = width // rows  
    for i in range(rows):  
        pygame.draw.line(win, COLORS["GREY"], (0, i * gap), (width, i * gap))  
    for j in range(rows):  
        pygame.draw.line(win, COLORS["GREY"], (j * gap, 0), (j * gap, width))  

def draw(win, grid, rows: int, width: int):  
    win.fill(COLORS["WHITE"])  
    for row in grid:  
        for spot in row:  
            spot.draw(win)  
    draw_grid(win, rows, width)  
    pygame.display.update()  

def get_clicked_pos(pos, rows: int, width: int):  
    gap = width // rows  
    y, x = pos  
    row = y // gap  
    col = x // gap  
    return row, col  

def handle_events(grid, start, end):  
    """Handles all the events during the main loop."""  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            return False  

        if pygame.mouse.get_pressed()[0]:  # LEFT  
            pos = pygame.mouse.get_pos()  
            row, col = get_clicked_pos(pos, ROWS, WIDTH)  
            spot = grid[row][col]  
            if not start and spot != end:  
                start = spot  
                start.make_start()  

            elif not end and spot != start:  
                end = spot  
                end.make_end()  

            elif spot != end and spot != start:  
                spot.make_barrier()  

        elif pygame.mouse.get_pressed()[2]:  # RIGHT  
            pos = pygame.mouse.get_pos()  
            row, col = get_clicked_pos(pos, ROWS, WIDTH)  
            spot = grid[row][col]  
            spot.reset()  
            if spot == start:  
                start = None  
            elif spot == end:  
                end = None  

    return start, end  

def main(win, width):  
    """The main function to run the pathfinding algorithm."""  
    grid = make_grid(ROWS, width)  
    start = None  
    end = None  
    run = True  

    while run:  
        draw(win, grid, ROWS, width)  

        # Handle events  
        start, end = handle_events(grid, start, end)  
        if start and end:  
            for row in grid:  
                for spot in row:  
                    spot.update_neighbors(grid)  

            if pygame.key.get_pressed()[pygame.K_SPACE]:  
                dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)  

        if pygame.key.get_pressed()[pygame.K_c]:  
            start = None  
            end = None  
            grid = make_grid(ROWS, width)  

    pygame.quit()  

# Entry point for the program  
if __name__ == "__main__":  
    main(WIN, WIDTH)  
