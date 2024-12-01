# A* Algorithm Implementation Details

## Overview
The A* (A-Star) algorithm is an informed search algorithm that finds the shortest path between two points while avoiding obstacles.

## Components

### Cost Functions
The algorithm uses three main components to determine the optimal path:

1. **g(n)** - Path Cost
   - Represents the exact cost of the path from the starting point to current node
   - Calculated using actual distance traveled

2. **h(n)** - Heuristic
   - Estimated cost from current node to goal
   - Uses Manhattan distance or Euclidean distance
   - Must never overestimate the actual cost

3. **f(n)** - Total Cost
   - f(n) = g(n) + h(n)
   - Used to determine which node to explore next
   - Lower f(n) values are explored first

## Implementation Details

### Node Selection
```python
def h(p1, p2):  
    """Heuristic function for A* algorithm."""  
    x1, y1 = p1  
    x2, y2 = p2  
    return abs(x1 - x2) + abs(y1 - y2) 

f_score = {spot: float("inf") for row in grid for spot in row}  
f_score[start] = h(start.get_pos(), end.get_pos())  

f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
