import random
from minheap import MinHeap as mh
import gridworld as gw
import time




def agentlocation(grid):
    x = 0
    y = 0
    while(grid[x][y].blocked):
        x = random.randint(0, 100)
        y = random.randint(0,100)
    return (x,y)

def targetlocation(grid):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    while(grid[x][y].blocked):
        x = random.randint(0, 100)
        y = random.randint(0,100)
    return (x,y)

def exists(a, b):
  if(0 <= a <= 100 and 0 <= b <= 100):
    return True
  else: 
    return False

def hval(x1, y1, x2, y2):
    h = abs(x1 - x2) + abs(y1-y2)
    return h


def closed(closedlist, loc):
    if loc in closedlist:
        return True
    else:
        return False



#track the path and add proper counting of g values. its only astar right now and not repeated.

def ComputePath(ax, ay, tx, ty, grid, closedlist, blockedlist):
    node_expansions = 0
    openlist = []
    directions = [(1, 0), (0,1), (-1, 0), (0, -1)]
    parent = {}
    parent[(ax,ay)] = (None, None, 0)

    mh.push(openlist, (hval(ax,ay,tx, ty), 0, ax, ay))  #(f, g, x, y)

    while openlist:
        f, g, a, b = mh.pop(openlist)
        node_expansions += 1
        if (a, b) not in closedlist:
            closedlist.add((a,b))
            if (a,b) == (tx, ty):
                path = []
                while (a, b)!=(ax,ay): #adds middle and then start node before the check
                    path.append((a,b))
                    a, b, c = parent[(a,b)]
                path.append((ax, ay))
                path.reverse()
                return path, node_expansions

        for i in range(4):
            direction_x, direction_y = directions[i]    #SHOULSD ONLY BE CHECKING BLOCKED FOR DIRECT NEIGHBORS
            neighbor_x, neighbor_y = a + direction_x, b + direction_y
            if (a,b) == (ax, ay) and exists(neighbor_x, neighbor_y):
                if not grid[neighbor_x][neighbor_y].blocked:
                    if (neighbor_x, neighbor_y) not in closedlist:
                        gnew = g+1
                        h = hval(neighbor_x, neighbor_y, tx, ty)

                        #update if new path is better
                        if (neighbor_x, neighbor_y) not in parent or gnew < parent[(neighbor_x, neighbor_y)][2]:
                            mh.push(openlist, (gnew+h, -gnew, neighbor_x, neighbor_y))
                            parent[neighbor_x, neighbor_y] = (a, b, gnew)
                else:
                    closedlist.add((neighbor_x, neighbor_y))
                    blockedlist.add((neighbor_x, neighbor_y))

            elif exists(neighbor_x, neighbor_y):
                if (neighbor_x, neighbor_y) not in closedlist:
                    gnew = g+1
                    h = hval(neighbor_x, neighbor_y, tx, ty)
                    if (neighbor_x, neighbor_y) not in parent or gnew < parent[(neighbor_x, neighbor_y)][2]:
                            mh.push(openlist, (gnew+h, -gnew, neighbor_x, neighbor_y))
                            parent[neighbor_x, neighbor_y] = (a, b, gnew)



    return None, node_expansions
            

  
    
def main(ax, ay, tx, ty, grid):
    total_expansions = 0
    target = (tx, ty)
    counter = 0
    current = (ax, ay)
    closedlist = set()
    blockedlist = set()
    finalpath = []
    while current!=target:
        a, b = current
        path, node_expansions = ComputePath(a, b, tx, ty, grid, closedlist, blockedlist)
        total_expansions += node_expansions
        if path is None:
                print(f"I cannot reach the target.")
                return False, None, counter, total_expansions
        
        for x, y in path:
            if not grid[x][y].blocked:
                current = (x, y)
                if current != (ax, ay):
                    counter+=1
                finalpath.append(current)
                if len(finalpath) >=2:
                    if(finalpath[-1]==finalpath[-2]):
                        finalpath.remove(current)
                        counter-=1
                

            else:
                a, b = current
                finalpath.remove(current)
                closedlist.clear()
                blockedlist.add((x,y))
                closedlist.update(blockedlist)

                break



    if(current == target):
        print(f"I reached the target.")
        print(f"Blocked list: {blockedlist}")
        return True, finalpath, counter, total_expansions

if __name__ == "__main__":
    # testing the algorithm
    start_time = time.time()
    newgrid = gw.generate_gridworld()
    ax, ay = agentlocation(newgrid)
    tx, ty = targetlocation(newgrid)
    path = []
    counter = 0
    result, path, counter, node_expansions = main(ax, ay, tx, ty, newgrid)
    end_time = time.time()

    if result:
        print(f"Path: {path}")
        print(f"Steps taken: {counter}")
        print(f"Runtime: {end_time - start_time} seconds")
        print(f"Node expansions: {node_expansions}")    


        gw.visualize_grid(newgrid, path, 'purple', delay=50)
    else:
        print("Sorry!")
        print(f"Runtime: {end_time - start_time} seconds")
        print(f"Node expansions: {node_expansions}")
        gw.visualize_grid(newgrid, path, 'purple', delay=50)
