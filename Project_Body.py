from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

print("rafi was here")
print ("rafi was NO here")
Rafi
rafiali.
Invisible

Rafi — 11/27/2025 3:15 AM
😭😭😭😭😭😭
Image
Image
Image
Image
Image
Image
Image
Image
Image
Image
Image
Image
👀 👀 👀 👀 👀 👀 👀
🐣
👎 🥹
😓
🐣
👀 👀
❤️ ❤️ ❤️
❌ ❌ ❌ ❌ ❌ ❌
🙉
🐣 🐣 🐣 🐣 🐣 🐣 🐣
🙉 🙉 🙉 🙉 🙉 🙉 🙉 🙉 🙉 🙉 🙉
Wordle
APP
 — 11/27/2025 3:22 AM
Rafi and NUSRAT were playing 
2 unfinished games of Wordle
Bobble League
APP
 — 11/27/2025 3:26 AM
Game Invitation
Bobble League
Game ended. Start a new one?

Play
NUSRAT — 11/27/2025 3:27 AM
😭
⚠️
Wordle
APP
 — 11/28/2025 3:30 AM
Nobody got yesterday's Wordle... but today is a new day @Rafi @NUSRAT 🌞
NUSRAT — 12/6/2025 8:43 AM
https://www.researchgate.net/publication/385647173_Study_on_the_Factors_Affecting_Employability_Among_the_Private_Universities_Graduates_Global_Viewpoint https://link.springer.com/article/10.1007/s40888-024-00328-z https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1664249/full https://ijarped.com/index.php/journal/article/view/3095 https://link.springer.com/chapter/10.1007/978-3-031-20653-5_7
SpringerLink
Education, educational mismatch and occupational status: an analysi...
Economia Politica - The aim of this paper is to estimate the effect of longer schooling on the probability of entering a high-skill job and analyse whether the size of this effect depends on the...
Education, educational mismatch and occupational status: an analysi...
Frontiers | Career paths and university education: factors that det...
Employment outcomes are more strongly associated with specific career paths than with academic performance. Despite expanding university access, significant ...
SpringerLink
Are Graduates Working in Graduate Occupations? Insights from the Portu
Our study draws on the Portuguese linked employer-employee data (2007–2019) to examine the type of occupations assigned to young bachelor and master graduates. Empirical findings show positive signs but sound some alarms. Postgraduates are assigned to...
Image
Rafi — 12/7/2025 10:42 PM
ki pora shuna kmn jai
NUSRAT — 12/8/2025 1:06 PM
tmi amk dc e knk deo kn
🌚🌚
Rafi — 12/8/2025 7:03 PM
🌚
patta dilo na ei meye
bujchiii
bujchii
NUSRAT — 12/8/2025 7:19 PM
tumi eineo knock diso
oma
Rafi — 12/8/2025 7:20 PM
hehe
aree ami dc te boschilam so tmk dekhi active
NUSRAT — 12/17/2025 3:59 PM
Forwarded
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import sys
import random

# Camera-related variables
camera_pos = (0, 600, 400)
previous_camera_pos = (0, 800, 600)
fovY = 120
GRID_LENGTH = 800
first_person_view = False
top_view_mode = False
top_view_height = 1000

# --- Gun constants ---
NUZZLE_DISTANCE = 45   # Distance in front of Jerry where gun barrel extends
MUZZLE_FLASH_TIME = 0.08  # Seconds the muzzle flash is visible

# Game state variables
jerry_pos = [0, 0, 30]  # 1.5x larger (was 20)
jerry_angle = 0
jerry_lives = 10
jerry_speed = 8
jerry_score = 0
is_dead = False  # Added death state like code 2

# Two Toms system - slower speed
tom_positions = [[300, 300, 30], [-300, -300, 30]]  # 1.5x larger
tom_speed = 1  # Same as first code

# Zombies guard cheese in corners
zombie_positions = [[-600, -600, 30], [600, -600, 30], [600, 600, 30], [-600, 600, 30]]  # 1.5x larger
zombie_angles = [0, 90, 180, 270]
zombie_speed = 1
zombie_radius = 120

# Cheese positions
cheese_positions = [[-500, -500, 22], [500, -500, 22], [500, 500, 22], [-500, 500, 22]]  # 1.5x larger
cheese_active = [True, True, True, True]
cheese_respawn_timers = [0, 0, 0, 0]

# Falling diamonds system with breathing effect - MODIFIED DURATION
falling_diamonds = []
diamond_spawn_timer = 0
diamond_spawn_interval = 3
diamond_collected = 0
max_diamonds = 3
diamond_base_size = 25  # Increased base size for better visibility
diamond_fall_duration = 5  # Diamond stays for 3.5 seconds (3-4 sec range)
diamond_pulse = 5.0  # Added fattening effect like code 2
elapsed_time = 0.0  # Added elapsed time for diamond pulse

# Game objects
bullets = []
cheat_ball = None
cheat_ball_timer = 0
cheat_ball_duration = 5
cheat_ball_pulse = 5.0  # Added fattening effect like code 2
enemies_distracted = False

# Shield system
shield_active = False
shield_timer = 0
shield_duration = 5

# Enemy system
enemy_alive = [True, True, True, True, True, True]
enemy_respawn_timers = [0, 0, 0, 0, 0, 0]

# Invisible boundary
BOUNDARY_DISTANCE = 750

# Tree system
trees = []
tree_count = 10

# Game state
game_over = False
game_won = False
last_time = time.time()
last_collision_time = 0

def distance_2d(pos1, pos2):
    """Calculate 2D distance between two positions."""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def normalize_angle(angle):
    """Normalize angle to 0-360 range."""
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def create_trees():
    """Create trees around the boundary."""
    global trees
... (1,128 lines left)
Collapse
message.txt
45 KB
NUSRAT — 12/17/2025 6:37 PM
Forwarded
ass03
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
Expand
message.txt
22 KB
Rafi — 12/21/2025 12:40 AM
👀
dc
NUSRAT — 12/21/2025 12:40 AM
Rafi — 12/21/2025 12:40 AM
🙉
NUSRAT — 12/21/2025 12:41 AM
Rafi — 12/21/2025 12:41 AM
NUSRAT — 12/21/2025 12:41 AM
Rafi — 12/21/2025 12:41 AM
NUSRAT — 12/21/2025 12:41 AM
ew dlt
dlt
Rafi — 12/21/2025 12:41 AM
NUSRAT — 12/21/2025 12:41 AM
NUSRAT — 12/21/2025 12:42 AM
tmr e baccha tmr skin tone
🌚🌚
tumina pora bujhba
🙄🙄🙄🙄🙄
gesega
kmn ta lage
aschorjo
ami r bujhabona bole dilam
Rafi — 12/21/2025 12:43 AM
reee
Rafi — 12/21/2025 12:43 AM
what
Rafi
 started a call that lasted 19 minutes. — 12/21/2025 12:43 AM
NUSRAT — 12/21/2025 1:02 AM
meri marzi
Rafi — 12/21/2025 1:02 AM
NUSRAT — 12/21/2025 1:02 AM
porte boso
Rafi — 12/21/2025 1:02 AM
NUSRAT — 12/21/2025 8:53 PM
kya human
Rafi — 12/21/2025 8:53 PM
tmi messenger rekhe dc te
NUSRAT — 12/22/2025 5:17 PM
oi
oi
oi
Rafi
 started a call that lasted an hour. — 12/22/2025 6:51 PM
NUSRAT — 12/22/2025 7:44 PM
oi
oi
oi
oi
oi
oi
oi
oi
oi
gugugaga
huhaha
hihihuhu
Rafi — 12/22/2025 7:44 PM
asi asi
NUSRAT — 12/22/2025 7:44 PM
porba na jaboga
Rafi — 12/22/2025 7:47 PM
helllooo
NUSRAT — 12/22/2025 7:48 PM
gelam ga
Rafi — 12/23/2025 12:04 AM
yooo
yoooo
NUSRAT — 12/23/2025 12:06 AM
ji
NUSRAT
 started a call that lasted an hour. — 12/23/2025 12:06 AM
Rafi — Yesterday at 8:23 AM
import heapq

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def astar_maze_solver(maze, start, goal, n, m):
    directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    pq = []
    heapq.heappush(pq, (0, start))

    g_cost = {start: 0}
    parent = {start: None}
    movetaken = {}

    while pq:
        , current = heapq.heappop(pq)

        if current == goal:
            path = []
            while parent[current] is not None:
                path.append(move_taken[current])
                current = parent[current]
            path.reverse()
            return len(path), "".join(path)

        x, y = current

        for move, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == '0':
                new_cost = g_cost[current] + 1
                next_cell = (nx, ny)

                if next_cell not in g_cost or new_cost < g_cost[next_cell]:
                    g_cost[next_cell] = new_cost
                    priority = new_cost + manhattan(nx, ny, goal[0], goal[1])
                    heapq.heappush(pq, (priority, next_cell))
                    parent[next_cell] = current
                    move_taken[next_cell] = move

    return -1, ""

def solvemaze():
    n, m = map(int, input().split())
    a, b = map(int, input().split())
    c, d = map(int, input().split())

    maze = [input().strip() for  in range(n)]

    cost, path = astar_maze_solver(maze, (a, b), (c, d), n, m)

    if cost == -1:
        print(-1)
    else:
        print(cost)
        print(path)
﻿
NUSRAT
nusrat_10
 
Human Are Human
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import sys
import random

# Camera-related variables
camera_pos = (0, 600, 400)
previous_camera_pos = (0, 800, 600)
fovY = 120
GRID_LENGTH = 800
first_person_view = False
top_view_mode = False
top_view_height = 1000

# --- Gun constants ---
NUZZLE_DISTANCE = 45   # Distance in front of Jerry where gun barrel extends
MUZZLE_FLASH_TIME = 0.08  # Seconds the muzzle flash is visible

# Game state variables
jerry_pos = [0, 0, 30]  # 1.5x larger (was 20)
jerry_angle = 0
jerry_lives = 10
jerry_speed = 8
jerry_score = 0
is_dead = False  # Added death state like code 2

# Two Toms system - slower speed
tom_positions = [[300, 300, 30], [-300, -300, 30]]  # 1.5x larger
tom_speed = 1  # Same as first code

# Zombies guard cheese in corners
zombie_positions = [[-600, -600, 30], [600, -600, 30], [600, 600, 30], [-600, 600, 30]]  # 1.5x larger
zombie_angles = [0, 90, 180, 270]
zombie_speed = 1
zombie_radius = 120

# Cheese positions
cheese_positions = [[-500, -500, 22], [500, -500, 22], [500, 500, 22], [-500, 500, 22]]  # 1.5x larger
cheese_active = [True, True, True, True]
cheese_respawn_timers = [0, 0, 0, 0]

# Falling diamonds system with breathing effect - MODIFIED DURATION
falling_diamonds = []
diamond_spawn_timer = 0
diamond_spawn_interval = 3
diamond_collected = 0
max_diamonds = 3
diamond_base_size = 25  # Increased base size for better visibility
diamond_fall_duration = 5  # Diamond stays for 3.5 seconds (3-4 sec range)
diamond_pulse = 5.0  # Added fattening effect like code 2
elapsed_time = 0.0  # Added elapsed time for diamond pulse

# Game objects
bullets = []
cheat_ball = None
cheat_ball_timer = 0
cheat_ball_duration = 5
cheat_ball_pulse = 5.0  # Added fattening effect like code 2
enemies_distracted = False

# Shield system
shield_active = False
shield_timer = 0
shield_duration = 5

# Enemy system
enemy_alive = [True, True, True, True, True, True]
enemy_respawn_timers = [0, 0, 0, 0, 0, 0]

# Invisible boundary
BOUNDARY_DISTANCE = 750

# Tree system
trees = []
tree_count = 10

# Game state
game_over = False
game_won = False
last_time = time.time()
last_collision_time = 0

def distance_2d(pos1, pos2):
    """Calculate 2D distance between two positions."""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def normalize_angle(angle):
    """Normalize angle to 0-360 range."""
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def create_trees():
    """Create trees around the boundary."""
    global trees
    trees = []
    
    # Create trees along the four sides of the square boundary (like 2nd code)
    # Each side will have 5 trees evenly spaced
    trees_per_side = 5
    boundary_offset = BOUNDARY_DISTANCE + 10  # Place trees outside the boundary
    
    # Top side (y = boundary_offset)
    for i in range(trees_per_side):
        x = -BOUNDARY_DISTANCE + (i * (2 * BOUNDARY_DISTANCE) / (trees_per_side - 1))
        y = boundary_offset
        tree = {
            'pos': [x, y, 0],
            'trunk_height': random.uniform(80, 120),
            'trunk_radius': random.uniform(8, 15),
            'crown_radius': random.uniform(40, 60),
            'trunk_color': [random.uniform(0.4, 0.6), random.uniform(0.2, 0.4), random.uniform(0.1, 0.2)],
            'crown_color': [random.uniform(0.1, 0.3), random.uniform(0.4, 0.8), random.uniform(0.1, 0.3)]
        }
        trees.append(tree)
    
    # Bottom side (y = -boundary_offset)
    for i in range(trees_per_side):
        x = -BOUNDARY_DISTANCE + (i * (2 * BOUNDARY_DISTANCE) / (trees_per_side - 1))
        y = -boundary_offset
        tree = {
            'pos': [x, y, 0],
            'trunk_height': random.uniform(80, 120),
            'trunk_radius': random.uniform(8, 15),
            'crown_radius': random.uniform(40, 60),
            'trunk_color': [random.uniform(0.4, 0.6), random.uniform(0.2, 0.4), random.uniform(0.1, 0.2)],
            'crown_color': [random.uniform(0.1, 0.3), random.uniform(0.4, 0.8), random.uniform(0.1, 0.3)]
        }
        trees.append(tree)
    
    # Left side (x = -boundary_offset)
    for i in range(trees_per_side):
        x = -boundary_offset
        y = -BOUNDARY_DISTANCE + (i * (2 * BOUNDARY_DISTANCE) / (trees_per_side - 1))
        tree = {
            'pos': [x, y, 0],
            'trunk_height': random.uniform(80, 120),
            'trunk_radius': random.uniform(8, 15),
            'crown_radius': random.uniform(40, 60),
            'trunk_color': [random.uniform(0.4, 0.6), random.uniform(0.2, 0.4), random.uniform(0.1, 0.2)],
            'crown_color': [random.uniform(0.1, 0.3), random.uniform(0.4, 0.8), random.uniform(0.1, 0.3)]
        }
        trees.append(tree)
    
    # Right side (x = boundary_offset)
    for i in range(trees_per_side):
        x = boundary_offset
        y = -BOUNDARY_DISTANCE + (i * (2 * BOUNDARY_DISTANCE) / (trees_per_side - 1))
        tree = {
            'pos': [x, y, 0],
            'trunk_height': random.uniform(80, 120),
            'trunk_radius': random.uniform(8, 15),
            'crown_radius': random.uniform(40, 60),
            'trunk_color': [random.uniform(0.4, 0.6), random.uniform(0.2, 0.4), random.uniform(0.1, 0.2)],
            'crown_color': [random.uniform(0.1, 0.3), random.uniform(0.4, 0.8), random.uniform(0.1, 0.3)]
        }
        trees.append(tree)

def check_boundary_collision(pos):
    """Check if position is outside boundary."""
    distance = math.sqrt(pos[0]**2 + pos[1]**2)
    return distance > BOUNDARY_DISTANCE

def bounce_from_boundary(pos, vel=None):
    """Handle boundary collision with scientific bouncing."""
    distance = math.sqrt(pos[0]**2 + pos[1]**2)
    if distance > BOUNDARY_DISTANCE:
        # Calculate normal vector pointing inward
        normal_x = -pos[0] / distance
        normal_y = -pos[1] / distance
        
        # Move position back inside boundary (fixed positioning)
        scale_factor = BOUNDARY_DISTANCE * 0.95 / distance
        pos[0] = pos[0] * scale_factor
        pos[1] = pos[1] * scale_factor
        
        # If velocity provided, reflect it scientifically
        if vel:
            dot_product = vel[0] * normal_x + vel[1] * normal_y
            vel[0] = vel[0] - 2 * dot_product * normal_x
            vel[1] = vel[1] - 2 * dot_product * normal_y

def random_position_away_from_center(min_distance=100):
    """Generate random position away from center."""
    while True:
        x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        y = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        if math.sqrt(x*x + y*y) > min_distance and not check_boundary_collision([x, y]):
            return [x, y, 30]

def spawn_falling_diamond():
    """Spawn a new falling diamond."""
    x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
    y = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
    if not check_boundary_collision([x, y]):
        # Calculate fall height based on desired duration
        fall_speed = random.uniform(3, 5)
        initial_height = fall_speed * diamond_fall_duration * 60  # 60 FPS approximation
        
        diamond = {
            'pos': [x, y, initial_height],
            'fall_speed': fall_speed,
            'spawn_time': time.time()
        }
        falling_diamonds.append(diamond)

def update_falling_diamonds():
    """Update falling diamonds positions and remove expired ones."""
    global diamond_spawn_timer, falling_diamonds
    
    current_time = time.time()
    
    if current_time - diamond_spawn_timer > diamond_spawn_interval:
        spawn_falling_diamond()
        diamond_spawn_timer = current_time
    
    for diamond in falling_diamonds[:]:
        diamond['pos'][2] -= diamond['fall_speed']
        
        # Remove diamond when it hits the ground or after duration
        if diamond['pos'][2] <= 15:
            falling_diamonds.remove(diamond)

def draw_diamond_landing_predictions():
    """Draw red marks on ground showing where diamonds will land (only while falling)."""
    glColor3f(1.0, 0.0, 0.0)  # Red color
    
    for diamond in falling_diamonds:
        # Only show prediction if diamond is still falling
        if diamond['pos'][2] > 15:
            x, y = diamond['pos'][0], diamond['pos'][1]
            size = 40  # Size of prediction mark
            
            # Draw a red square on the ground using GL_QUADS
            glBegin(GL_QUADS)
            glVertex3f(x - size, y - size, 0.5)
            glVertex3f(x + size, y - size, 0.5)
            glVertex3f(x + size, y + size, 0.5)
            glVertex3f(x - size, y + size, 0.5)
            glEnd()
            
            # Draw an X pattern for better visibility using GL_LINES
            glBegin(GL_LINES)
            glVertex3f(x - size, y - size, 1.0)
            glVertex3f(x + size, y + size, 1.0)
            glVertex3f(x - size, y + size, 1.0)
            glVertex3f(x + size, y - size, 1.0)
            glEnd()

def update_fattening_effects(dt):
    """Update fattening effects for diamonds and cheat ball."""
    global diamond_pulse, cheat_ball_pulse, elapsed_time
    if not is_dead:
        elapsed_time += dt
        diamond_pulse = 5.0 * math.sin(elapsed_time)
        cheat_ball_pulse = 5.0 * math.sin(elapsed_time)

def get_diamond_size(diamond):
    """Get diamond size with fattening effect."""
    return diamond_base_size + diamond_pulse

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text at specified screen coordinates."""
    glColor3f(.9,.2,.4)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_gun():
    """Draw gun barrel attached to Jerry's body using only template functions."""
    # Position gun at Jerry's front, slightly to the right and at chest level
    glPushMatrix()
    glTranslatef(25, -10, 5)  # Position: front-right of Jerry, chest level
    glRotatef(90, 0, 1, 0)    # Point barrel forward along Jerry's facing direction
    
    # Gun barrel using cylinder (template function)
    glColor3f(0.1, 0.1, 0.1)  # Dark gray barrel
    quad = gluNewQuadric()
    gluCylinder(quad, 4, 4, NUZZLE_DISTANCE, 8, 4)  # Barrel extends forward
    
    # Muzzle tip using small cube instead of gluDisk
    glTranslatef(0, 0, NUZZLE_DISTANCE)
    glutSolidCube(8)  # Small cube as muzzle tip
    
    glPopMatrix()

def draw_muzzle_flash_at(pos, angle):
    """Draw a brief flash at the muzzle when firing using template functions."""
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(angle, 0, 0, 1)   # match Jerry's facing direction
    
    # Use scaled cube instead of cone for muzzle flash
    glColor3f(1.0, 0.8, 0.0)    # bright yellow-orange
    glScalef(2, 2, 4)  # Make it elongated like a flash
    glutSolidCube(8)
    
    glPopMatrix()

def draw_jerry():
    """Draw Jerry the mouse with attached gun."""
    # Only draw Jerry if not in first person mode AND not dead
    if first_person_view or is_dead:
        return

    glPushMatrix()
    glTranslatef(jerry_pos[0], jerry_pos[1], jerry_pos[2])
    glRotatef(jerry_angle, 0, 0, 1)

    # Jerry's body
    glColor3f(1.0, 0.6, 0.2)
    glutSolidCube(70)

    # Jerry's head
    glColor3f(1.0, 0.7, 0.3)
    glTranslatef(0, 0, 50)
    gluSphere(gluNewQuadric(), 20, 10, 10)

    # Jerry's ears
    glColor3f(1.0, 0, 0)
    glTranslatef(-12, 0, 8)
    glutSolidCube(19)
    glTranslatef(24, 0, 0)
    glutSolidCube(19)
    
    # Reset position for gun (back to Jerry's body center)
    glTranslatef(-12, 0, -58)  # Back to Jerry's center
    
    # Draw the gun barrel attached to Jerry
    draw_gun()

    glPopMatrix()

def draw_tom(index):
    """Draw Tom cat enemy."""
    if not enemy_alive[index]:
        return
        
    glPushMatrix()
    glTranslatef(tom_positions[index][0], tom_positions[index][1], tom_positions[index][2])
    
    # Tom's body (larger gray cube) - same as first code
    glColor3f(0.3, 0.3, 0.3)
    glutSolidCube(70)  # 1.5x larger (was 35)
    
    # Tom's head (sphere)
    glColor3f(0.6, 0.6, 0.6)
    glTranslatef(0, 0, 37)  # 1.5x larger
    gluSphere(gluNewQuadric(), 22, 10, 10)  # 1.5x larger
    
    glColor3f(0.4, 0.4, 0.4)
    glTranslatef(-15, 0, 10)  # Move to first ear
    glutSolidCube(20)         # Draw first ear
    glTranslatef(30, 0, 0)    # Move to second ear (15 - (-15) = 30)
    glutSolidCube(20)         # Draw second ear
    glTranslatef(-15, 0, -10) # Move back to head center
    
    glPopMatrix()

def draw_zombie(index):
    """Draw zombie enemy."""
    if not enemy_alive[index + 2]:  # Zombies are indices 2-5 like first code
        return
        
    glPushMatrix()
    glTranslatef(zombie_positions[index][0], zombie_positions[index][1], zombie_positions[index][2])
    
    # Zombie body (dark green cube) - same as first code
    glColor3f(0.2, 0.3, 0.2)
    glutSolidCube(45)  # 1.5x larger (was 30)
    
    # Zombie head (sphere)
    glColor3f(0.3, 0.5, 0.3)
    glTranslatef(0, 0, 33)  # 1.5x larger
    gluSphere(gluNewQuadric(), 19, 10, 10)  # 1.5x larger
    
    # Zombie arms (cylinders) - same as first code
    glColor3f(0.2, 0.9, 0.2)
    glTranslatef(-30, 0, -15)  # 1.5x larger
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 22, 6, 6)  # 1.5x larger
    
    glTranslatef(0, 0, 37)  # 1.5x larger
    gluCylinder(gluNewQuadric(), 4, 4, 22, 6, 6)
    
    glPopMatrix()

def draw_cheese(index):
    """Draw cheese collectible."""
    if not cheese_active[index]:
        return
        
    pos = cheese_positions[index]
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    # Cheese wedge - brighter and more visible yellow
    glColor3f(0.9, 0.4, 0.2)  # Changed from (1.0, 0.4, 0.2) to bright yellow
    glBegin(GL_TRIANGLES)
    # Front face - scaled up by ~1.5x
    glVertex3f(0, 0, 0)
    glVertex3f(35, 0, 0)      # Changed from 25 to 35
    glVertex3f(20, 25, 18)    # Changed from (15, 18, 12) to (20, 25, 18)
    # Back face  
    glVertex3f(0, 0, 18)      # Changed from 12 to 18
    glVertex3f(35, 0, 18)     # Changed from 25 to 35
    glVertex3f(20, 25, 18)    # Changed from (15, 18, 12) to (20, 25, 18)
    glEnd()

    # Side faces - scaled proportionally
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 18)      # Changed from 12 to 18
    glVertex3f(20, 25, 18)    # Changed from (11, 18, 12) to (20, 25, 18)
    glVertex3f(20, 25, 0)     # Changed from (11, 18, 0) to (20, 25, 0)

    glVertex3f(35, 0, 0)      # Changed from 22 to 35
    glVertex3f(35, 0, 18)     # Changed from (22, 0, 12) to (35, 0, 18)
    glVertex3f(20, 25, 18)    # Changed from (11, 18, 12) to (20, 25, 18)
    glVertex3f(20, 25, 0)     # Changed from (11, 18, 0) to (20, 25, 0)
    glEnd()

    # Cheese holes - more visible orange/red
    glColor3f(0.9, 0.9, 0.1)  # Brighter, more contrasting color
    glPointSize(15)           # Changed from 9 to 15 for bigger holes
    glBegin(GL_POINTS)
    glVertex3f(8, 5, 9)       # Scaled proportionally
    glVertex3f(22, 5, 9)      # Scaled proportionally
    glVertex3f(15, 15, 9)     # Scaled proportionally
    glEnd()

    glPopMatrix()

def draw_falling_diamond(diamond):
    """Draw a falling diamond with fattening effect."""
    glPushMatrix()
    glTranslatef(diamond['pos'][0], diamond['pos'][1], diamond['pos'][2])
    
    # Get fattening size like code 2
    size = get_diamond_size(diamond)
    
    # Much brighter and more visible diamond
    glColor3f(0.0, 1.0, 1.0)  # Bright cyan
    
    # Top pyramid
    glBegin(GL_TRIANGLES)
    # Front face
    glVertex3f(0, 0, size)
    glVertex3f(-size*0.7, -size*0.7, 0)
    glVertex3f(size*0.7, -size*0.7, 0)
    
    # Right face
    glVertex3f(0, 0, size)
    glVertex3f(size*0.7, -size*0.7, 0)
    glVertex3f(size*0.7, size*0.7, 0)
    
    # Back face
    glVertex3f(0, 0, size)
    glVertex3f(size*0.7, size*0.7, 0)
    glVertex3f(-size*0.7, size*0.7, 0)
    
    # Left face
    glVertex3f(0, 0, size)
    glVertex3f(-size*0.7, size*0.7, 0)
    glVertex3f(-size*0.7, -size*0.7, 0)
    glEnd()
    
    # Bottom pyramid
    glBegin(GL_TRIANGLES)
    # Front face
    glVertex3f(0, 0, -size)
    glVertex3f(size*0.7, -size*0.7, 0)
    glVertex3f(-size*0.7, -size*0.7, 0)
    
    # Right face
    glVertex3f(0, 0, -size)
    glVertex3f(size*0.7, size*0.7, 0)
    glVertex3f(size*0.7, -size*0.7, 0)
    
    # Back face
    glVertex3f(0, 0, -size)
    glVertex3f(-size*0.7, size*0.7, 0)
    glVertex3f(size*0.7, size*0.7, 0)
    
    # Left face
    glVertex3f(0, 0, -size)
    glVertex3f(-size*0.7, -size*0.7, 0)
    glVertex3f(-size*0.7, size*0.7, 0)
    glEnd()
    
    glPopMatrix()

def draw_bullet(bullet):
    """Draw bullet projectile."""
    glPushMatrix()
    glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
    
    # RED bullets as requested
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 6, 8, 8)  # Bigger bullets for visibility
    
    glPopMatrix()

def draw_cheat_ball():
    """Draw the cheat ball that distracts enemies."""
    if cheat_ball is None:
        return
        
    glPushMatrix()
    glTranslatef(cheat_ball['pos'][0], cheat_ball['pos'][1], cheat_ball['pos'][2])
    
    # Bright magenta ball with fattening effect like code 2
    ball_size = 20 + cheat_ball_pulse
    glColor3f(1, 0.2, 1)
    gluSphere(gluNewQuadric(), ball_size, 16, 16)  # Now with fattening effect
    
    glPopMatrix()

def draw_shield():
    """Draw protective shield around Jerry."""
    if not shield_active:
        return
        
    glPushMatrix()
    glTranslatef(jerry_pos[0], jerry_pos[1], jerry_pos[2])
    
    current_time = time.time()
    pulse = abs(math.sin(current_time * 10)) * 0.5 + 0.5
    
    glColor3f(0.2 + pulse * 0.6, 0.8, 1)
    
    # Shield using quads in circular pattern - 1.5x larger
    glBegin(GL_QUADS)
    for i in range(12):
        angle1 = i * 30
        angle2 = (i + 1) * 30
        
        inner_radius = 60  # 1.5x larger
        outer_radius = 90  # 1.5x larger
        
        x1_inner = inner_radius * math.cos(math.radians(angle1))
        y1_inner = inner_radius * math.sin(math.radians(angle1))
        x2_inner = inner_radius * math.cos(math.radians(angle2))
        y2_inner = inner_radius * math.sin(math.radians(angle2))
        
        x1_outer = outer_radius * math.cos(math.radians(angle1))
        y1_outer = outer_radius * math.sin(math.radians(angle1))
        x2_outer = outer_radius * math.cos(math.radians(angle2))
        y2_outer = outer_radius * math.sin(math.radians(angle2))
        
        glVertex3f(x1_inner, y1_inner, 0)
        glVertex3f(x2_inner, y2_inner, 0)
        glVertex3f(x2_outer, y2_outer, 0)
        glVertex3f(x1_outer, y1_outer, 0)
        
        glVertex3f(x1_inner, y1_inner, 45)  # 1.5x larger
        glVertex3f(x2_inner, y2_inner, 45)
        glVertex3f(x2_outer, y2_outer, 45)
        glVertex3f(x1_outer, y1_outer, 45)
    glEnd()
    
    glPopMatrix()

def draw_tree(tree):
    """Draw a tree with trunk and crown."""
    glPushMatrix()
    glTranslatef(tree['pos'][0], tree['pos'][1], tree['pos'][2])
    
    # Draw trunk
    glColor3f(tree['trunk_color'][0], tree['trunk_color'][1], tree['trunk_color'][2])
    gluCylinder(gluNewQuadric(), tree['trunk_radius'], tree['trunk_radius'] * 0.8, 
                tree['trunk_height'], 8, 8)
    
    # Draw crown
    glColor3f(tree['crown_color'][0], tree['crown_color'][1], tree['crown_color'][2])
    glTranslatef(0, 0, tree['trunk_height'])
    gluSphere(gluNewQuadric(), tree['crown_radius'], 12, 12)
    
    glPopMatrix()

def draw_floor():
    """Draw the game floor with colorful tiles."""
    tile_size = 80
    tiles_per_side = int(GRID_LENGTH * 2 / tile_size)
    
    glBegin(GL_QUADS)
    for i in range(-tiles_per_side//2, tiles_per_side//2):
        for j in range(-tiles_per_side//2, tiles_per_side//2):
            x = i * tile_size
            y = j * tile_size
            
            # Colorful floor pattern
            if (i + j) % 4 == 0:
                glColor3f(0.9, 0.9, 1.0)  # Light blue
            elif (i + j) % 4 == 1:
                glColor3f(1.0, 0.9, 0.9)  # Light pink
            elif (i + j) % 4 == 2:
                glColor3f(0.9, 1.0, 0.9)  # Light green
            else:
                glColor3f(1.0, 1.0, 0.9)  # Light yellow
            
            glVertex3f(x, y, 0)
            glVertex3f(x + tile_size, y, 0)
            glVertex3f(x + tile_size, y + tile_size, 0)
            glVertex3f(x, y + tile_size, 0)
    glEnd()

def update_jerry():
    """Update Jerry's position and handle boundary collisions."""
    if check_boundary_collision(jerry_pos):
        bounce_from_boundary(jerry_pos)

def update_toms():
    """Update Tom enemies movement and AI."""
    # Update both Toms - EXACTLY like first code
    for i in range(2):
        if not enemy_alive[i] or enemies_distracted:
            if enemies_distracted and cheat_ball:
                # Move toward cheat ball
                dx = cheat_ball['pos'][0] - tom_positions[i][0]
                dy = cheat_ball['pos'][1] - tom_positions[i][1]
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist > 5:
                    tom_positions[i][0] += (dx/dist) * tom_speed
                    tom_positions[i][1] += (dy/dist) * tom_speed
            continue
        
        # Each Tom follows Jerry
        dx = jerry_pos[0] - tom_positions[i][0]
        dy = jerry_pos[1] - tom_positions[i][1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 5:
            tom_positions[i][0] += (dx/dist) * tom_speed
            tom_positions[i][1] += (dy/dist) * tom_speed

def update_zombies():
    """Update zombie enemies movement and AI."""
    # EXACTLY like first code
    for i in range(4):
        if not enemy_alive[i + 2]:  # Zombies are now indices 2-5
            continue
            
        if enemies_distracted and cheat_ball:
            # Move toward cheat ball
            dx = cheat_ball['pos'][0] - zombie_positions[i][0]
            dy = cheat_ball['pos'][1] - zombie_positions[i][1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 5:
                zombie_positions[i][0] += (dx/dist) * zombie_speed
                zombie_positions[i][1] += (dy/dist) * zombie_speed
        else:
            # Circular movement around cheese
            if cheese_active[i]:  # Only circle if cheese is there
                center_x = cheese_positions[i][0]
                center_y = cheese_positions[i][1]
                
                zombie_angles[i] += zombie_speed
                zombie_angles[i] = normalize_angle(zombie_angles[i])
                
                zombie_positions[i][0] = center_x + zombie_radius * math.cos(math.radians(zombie_angles[i]))
                zombie_positions[i][1] = center_y + zombie_radius * math.sin(math.radians(zombie_angles[i]))

def update_bullets():
    """Update bullet positions and handle collisions."""
    global bullets, jerry_score
    
    # EXACTLY like first code
    for bullet in bullets[:]:
        # Move bullet
        bullet['pos'][0] += bullet['vel'][0]
        bullet['pos'][1] += bullet['vel'][1]
        
        # Remove if out of bounds
        if (abs(bullet['pos'][0]) > GRID_LENGTH + 50 or 
            abs(bullet['pos'][1]) > GRID_LENGTH + 50):
            bullets.remove(bullet)
            continue
            
        # Check collision with enemies
        # Tom collisions (both Toms) - EXACTLY like first code
        for i in range(2):
            if enemy_alive[i] and distance_2d(bullet['pos'], tom_positions[i]) < 25:
                bullets.remove(bullet)
                enemy_alive[i] = False
                enemy_respawn_timers[i] = time.time() + 0.1
                jerry_score += 1  # Point for shooting Tom
                break
        else:
            # Zombie collision (only check if bullet wasn't removed by Tom collision)
            for i in range(4):
                if enemy_alive[i + 2] and distance_2d(bullet['pos'], zombie_positions[i]) < 20:
                    bullets.remove(bullet)
                    enemy_alive[i + 2] = False
                    enemy_respawn_timers[i + 2] = time.time() + 0.1
                    break

def update_cheat_ball():
    """Update cheat ball position and lifetime."""
    global cheat_ball, cheat_ball_timer, enemies_distracted
    
    if cheat_ball:
        current_time = time.time()
        
        cheat_ball['pos'][0] += cheat_ball['vel'][0]
        cheat_ball['pos'][1] += cheat_ball['vel'][1]
        
        # Scientific bouncing off boundary (like assignment 02)
        if check_boundary_collision(cheat_ball['pos']):
            bounce_from_boundary(cheat_ball['pos'], cheat_ball['vel'])
        
        # Ball stays in air for exactly 5 seconds
        if current_time - cheat_ball_timer >= cheat_ball_duration:
            cheat_ball = None
            enemies_distracted = False

def update_shield():
    """Update shield duration and deactivation."""
    global shield_active, shield_timer
    
    if shield_active:
        current_time = time.time()
        if current_time - shield_timer > shield_duration:
            shield_active = False

def update_cheese():
    """Update cheese respawn timers."""
    global cheese_active, cheese_respawn_timers
    
    current_time = time.time()
    
    for i in range(4):
        if (not cheese_active[i] and 
            current_time > cheese_respawn_timers[i]):
            cheese_active[i] = True

def update_respawn():
    """Handle enemy respawning."""
    current_time = time.time()
    
    # Respawn both Toms at random positions
    for i in range(2):
        if not enemy_alive[i] and current_time > enemy_respawn_timers[i]:
            enemy_alive[i] = True
            new_pos = random_position_away_from_center(200)
            tom_positions[i][0] = new_pos[0]
            tom_positions[i][1] = new_pos[1]
    
    # Respawn zombies at random positions
    for i in range(4):
        if not enemy_alive[i + 2] and current_time > enemy_respawn_timers[i + 2]:
            enemy_alive[i + 2] = True
            new_pos = random_position_away_from_center(200)
            zombie_positions[i][0] = new_pos[0]
            zombie_positions[i][1] = new_pos[1]

def check_collisions():
    """Check all collision detection and handle game state changes."""
    global jerry_lives, game_over, jerry_score, diamond_collected, falling_diamonds, last_collision_time, is_dead
    
    current_time = time.time()
    
    # Jerry vs enemies (if no shield and collision cooldown has expired) - FIXED RESPAWN BEHAVIOR
    if not shield_active and current_time > last_collision_time + 1.5:  # 1.5 second cooldown
        collision_occurred = False
        
        # Check both Toms collision
        for i in range(2):
            if enemy_alive[i] and distance_2d(jerry_pos, tom_positions[i]) < 52:  # Adjusted for 1.5x size
                jerry_lives -= 1
                collision_occurred = True
                last_collision_time = current_time
                print(f"Jerry hit by Tom {i+1}! Lives remaining: {jerry_lives}")
                
                # Respawn enemy immediately like code 2
                enemy_alive[i] = False
                enemy_respawn_timers[i] = time.time() + 0.1
                new_pos = random_position_away_from_center(200)
                tom_positions[i][0] = new_pos[0]
                tom_positions[i][1] = new_pos[1]
                enemy_alive[i] = True
                
                if jerry_lives <= 0:
                    is_dead = True
                    game_over = True
                    return
                break
            
        # Check zombie collision (only if no collision with Tom already)
        if not collision_occurred:
            for i in range(4):
                if enemy_alive[i + 2] and distance_2d(jerry_pos, zombie_positions[i]) < 45:
                    jerry_lives -= 1
                    collision_occurred = True
                    last_collision_time = current_time
                    print(f"Jerry hit by Zombie! Lives remaining: {jerry_lives}")
                    
                    # Respawn enemy immediately like code 2
                    enemy_alive[i + 2] = False
                    enemy_respawn_timers[i + 2] = time.time() + 0.1
                    new_pos = random_position_away_from_center(200)
                    zombie_positions[i][0] = new_pos[0]
                    zombie_positions[i][1] = new_pos[1]
                    enemy_alive[i + 2] = True
                    
                    if jerry_lives <= 0:
                        is_dead = True
                        game_over = True
                        return
                    break
        
        # FIXED: Don't reset Jerry position - only set death state when lives reach 0
        # This follows code 2's logic exactly
        
    else:
        # Shield destroys enemies on contact
        for i in range(2):
            if enemy_alive[i] and distance_2d(jerry_pos, tom_positions[i]) < 75:  # 1.5x larger shield range
                enemy_alive[i] = False
                enemy_respawn_timers[i] = time.time() + 0.1
            
        for i in range(4):
            if enemy_alive[i + 2] and distance_2d(jerry_pos, zombie_positions[i]) < 75:  # 1.5x larger shield range
                enemy_alive[i + 2] = False
                enemy_respawn_timers[i + 2] = time.time() + 0.1
    
    # Jerry vs cheese
    for i in range(4):
        if cheese_active[i] and distance_2d(jerry_pos, cheese_positions[i]) < 40:  # 1.5x larger
            cheese_active[i] = False
            cheese_respawn_timers[i] = time.time() + 1.0  # 1 second respawn
            jerry_score += 1
            
            # Check win condition
            if jerry_score >= 10:
                global game_won
                game_won = True
    
    # Jerry vs falling diamonds
    for diamond in falling_diamonds[:]:
        if (distance_2d(jerry_pos, diamond['pos']) < 25 and 
            abs(jerry_pos[2] - diamond['pos'][2]) < 30):  # Check Z distance too
            falling_diamonds.remove(diamond)
            diamond_collected += 1
            
            # Every 3 diamonds = 1 life
            if diamond_collected >= 3:
                jerry_lives += 1
                diamond_collected = 0

def draw_shapes():
    """Draw all game objects on screen."""
    draw_floor()
    draw_diamond_landing_predictions()  # Draw red marks for falling diamonds (only while falling)
    # Draw trees
    for tree in trees:
        draw_tree(tree)
    
    for i in range(4):
        draw_cheese(i)
    
    for diamond in falling_diamonds:
        draw_falling_diamond(diamond)
    
    # Only draw Jerry if not dead and not in first person
    draw_jerry()
    
    for i in range(2):
        draw_tom(i)
    
    for i in range(4):
        draw_zombie(i)
    
    for bullet in bullets:
        draw_bullet(bullet)
        # quick muzzle flash for bullets just spawned
        if time.time() - bullet.get('spawn_time', 0) < MUZZLE_FLASH_TIME:
            draw_muzzle_flash_at(bullet['pos'], bullet.get('angle', jerry_angle))

    draw_cheat_ball()
    draw_shield()

def keyboardListener(key, x, y):
    """Handle keyboard inputs for player movement and game controls."""
    global jerry_pos, jerry_angle, jerry_lives, jerry_score
    global cheat_ball, cheat_ball_timer, enemies_distracted
    global shield_active, shield_timer
    global game_over, game_won, cheese_active, enemy_alive, falling_diamonds
    global bullets, diamond_collected, last_collision_time, first_person_view
    global top_view_mode, camera_pos, previous_camera_pos, is_dead
    
    if game_over or game_won:
        if key == b'r':
            # Reset game
            jerry_pos = [0, 0, 30]
            jerry_angle = 0
            jerry_lives = 10
            jerry_score = 0
            is_dead = False
            tom_positions[0] = [300, 300, 30]
            tom_positions[1] = [-300, -300, 30]
            cheese_active = [True, True, True, True]
            enemy_alive = [True, True, True, True, True, True]
            game_over = False
            game_won = False
            bullets = []
            cheat_ball = None
            shield_active = False
            falling_diamonds = []
            diamond_collected = 0
            last_collision_time = 0
            first_person_view = False
            top_view_mode = False
            camera_pos = (0, 800, 600)
            create_trees()
        return
    
    # Don't allow movement if dead
    if not is_dead:
        # Move forward (W key)
        if key == b'w':
            jerry_pos[0] += jerry_speed * math.cos(math.radians(jerry_angle))
            jerry_pos[1] += jerry_speed * math.sin(math.radians(jerry_angle))
            update_jerry()

        # Move backward (S key)
        if key == b's':
            jerry_pos[0] -= jerry_speed * math.cos(math.radians(jerry_angle))
            jerry_pos[1] -= jerry_speed * math.sin(math.radians(jerry_angle))
            update_jerry()

        # Rotate left (A key)
        if key == b'a':
            jerry_angle += 15
            jerry_angle = normalize_angle(jerry_angle)

        # Rotate right (D key)
        if key == b'd':
            jerry_angle -= 15
            jerry_angle = normalize_angle(jerry_angle)

        # Toggle cheat ball (C key)
        if key == b'c':
            if cheat_ball is None:
                cheat_ball = {
                    'pos': [jerry_pos[0], jerry_pos[1], jerry_pos[2]],
                    'vel': [random.uniform(-6, 6), random.uniform(-6, 6)]
                }
                cheat_ball_timer = time.time()
                enemies_distracted = True

        # Activate shield (Space key)
        if key == b' ' and not shield_active:
            shield_active = True
            shield_timer = time.time()

    # Toggle first person view (V key)
    if key == b'v':
        first_person_view = not first_person_view

    # Toggle top view (T key)
    if key == b't':
        if not top_view_mode:
            # Switch to top view
            previous_camera_pos = camera_pos
            top_view_mode = True
            camera_pos = (0, 0, top_view_height)
        else:
            # Switch back to previous view
            top_view_mode = False
            camera_pos = previous_camera_pos

    # Reset game (R key)
    if key == b'r':
        # Reset game
        jerry_pos = [0, 0, 30]
        jerry_angle = 0
        jerry_lives = 10
        jerry_score = 0
        is_dead = False
        tom_positions[0] = [300, 300, 30]
        tom_positions[1] = [-300, -300, 30]
        cheese_active = [True, True, True, True]
        enemy_alive = [True, True, True, True, True, True]
        game_over = False
        game_won = False
        bullets = []
        cheat_ball = None
        shield_active = False
        falling_diamonds = []
        diamond_collected = 0
        last_collision_time = 0
        first_person_view = False
        top_view_mode = False
        camera_pos = (0, 800, 600)
        create_trees()

def specialKeyListener(key, x, y):
    """Handle special key inputs (arrow keys) for camera control."""
    global camera_pos, top_view_height
    x, y, z = camera_pos
    
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        if top_view_mode:
            top_view_height += 50
            camera_pos = (0, 0, top_view_height)
        else:
            z += 30

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        if top_view_mode:
            top_view_height = max(200, top_view_height - 50)
            camera_pos = (0, 0, top_view_height)
        else:
            z -= 30

    # Move camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        if not top_view_mode:
            x -= 30

    # Move camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        if not top_view_mode:
            x += 30

    if not top_view_mode:
        camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """Handle mouse inputs for firing bullets."""
    global bullets
    
    if game_over or game_won or is_dead:
        return
    
    # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if len(bullets) < 15:  # Limit bullets
            # Calculate gun muzzle position (front of Jerry where gun barrel ends)
            # Gun extends from Jerry's front-right position
            gun_offset_x = 25 * math.cos(math.radians(jerry_angle)) - 10 * math.sin(math.radians(jerry_angle))
            gun_offset_y = 25 * math.sin(math.radians(jerry_angle)) + 10 * math.cos(math.radians(jerry_angle))
            
            # Muzzle is at the end of the gun barrel
            muzzle_x = jerry_pos[0] + gun_offset_x + NUZZLE_DISTANCE * math.cos(math.radians(jerry_angle))
            muzzle_y = jerry_pos[1] + gun_offset_y + NUZZLE_DISTANCE * math.sin(math.radians(jerry_angle))
            muzzle_z = jerry_pos[2] + 5  # Gun is at chest level (5 units above Jerry's center)
            
            bullet = {
                'pos': [muzzle_x, muzzle_y, muzzle_z],
                'vel': [10 * math.cos(math.radians(jerry_angle)), 
                        10 * math.sin(math.radians(jerry_angle))],
                'spawn_time': time.time(),   # record fire time
                'angle': jerry_angle         # so flash matches rotation
            }
            bullets.append(bullet)

def setupCamera():
    """Configure the camera's projection and view settings."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 2500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person_view:
        eye_height = 52  # 1.5x larger
        look_distance = 225  # 1.5x larger
        
        cam_x = jerry_pos[0]
        cam_y = jerry_pos[1]
        cam_z = jerry_pos[2] + eye_height
        
        look_x = jerry_pos[0] + look_distance * math.cos(math.radians(jerry_angle))
        look_y = jerry_pos[1] + look_distance * math.sin(math.radians(jerry_angle))
        look_z = jerry_pos[2] + eye_height
        
        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    elif top_view_mode:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)  # Look down at center
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def idle():
    """Idle function that runs continuously to update game state."""
    global last_time
    
    current_time = time.time()
    dt = current_time - last_time if last_time else 0.016
    
    if dt > 0.1:
        dt = 0.1
    
    if current_time - last_time > 0.016:
        if not game_over and not game_won:
            update_fattening_effects(dt)  # Add fattening effects update
            if not is_dead:  # Only update game logic if not dead
                update_toms()
                update_zombies()
                update_bullets()
                update_cheat_ball()
                update_shield()
                update_falling_diamonds()
                update_cheese()
                check_collisions()
                update_respawn()
        last_time = current_time
    
    glutPostRedisplay()

def showScreen():
    """Display function to render the game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    draw_shapes()
    
    if game_over:
        draw_text(350, 400, "GAME OVER!")
        draw_text(320, 370, "Press R to restart")
    elif game_won:
        draw_text(350, 400, "YOU WON!")
        draw_text(300, 370, "10 points collected!")
        draw_text(320, 340, "Press R to restart")
    else:
        draw_text(10, 770, f"Lives: {jerry_lives}")
        draw_text(10, 740, f"Score: {jerry_score}/10")
        draw_text(10, 710, f"Diamonds: {diamond_collected}/3")
        # draw_text(10, 680, f"Falling Diamonds: {len(falling_diamonds)}")
        
        if top_view_mode:
            draw_text(10, 650, f"View: Top View (Height: {int(top_view_height)})")
        elif first_person_view:
            draw_text(10, 650, f"View: First Person")
        else:
            draw_text(10, 650, f"View: Third Person")
        
        if is_dead:
            draw_text(400, 400, "GAME OVER!")
            draw_text(320, 370, "Press R to restart")
        
        # Debug info - show both Toms distances (like first code)
        tom1_distance = distance_2d(jerry_pos, tom_positions[0]) if enemy_alive[0] else 999
        tom2_distance = distance_2d(jerry_pos, tom_positions[1]) if enemy_alive[1] else 999

        # draw_text(10, 500, f"Collision Cooldown: {(time.time() - last_collision_time):.1f}")
        
        if shield_active:
            remaining = shield_duration - (time.time() - shield_timer)
            draw_text(10, 620, f"Shield: {remaining:.1f}s")
        
        if cheat_ball:
            remaining = cheat_ball_duration - (time.time() - cheat_ball_timer)
            draw_text(10, 590, f"Cheat Ball: {remaining:.1f}s")
            draw_text(10, 470, "Enemies Distracted!")
        
        # Show diamond duration info
        if falling_diamonds:
            oldest_diamond = min(falling_diamonds, key=lambda d: d['spawn_time'])
            elapsed = time.time() - oldest_diamond['spawn_time']
            remaining = diamond_fall_duration - elapsed
            # draw_text(10, 440, f"Diamond Time Left: {remaining:.1f}s")
        
        # Controls - updated to match first code style
        # draw_text(10, 180, "WASD: Move/Rotate")
        # draw_text(10, 150, "Mouse: Shoot")
        # draw_text(10, 120, "V: Toggle First Person")
        # draw_text(10, 90, "C: Cheat Ball")
        # draw_text(10, 60, "Space: Shield")
        # draw_text(10, 30, "R: Reset Game")

    glutSwapBuffers()

def main():
    """Main function to set up OpenGL window and start game loop."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Fixed Tom and Jerry 3D Game - Template Functions Only")

    glClearColor(0.1, 0.1, 0.3, 1.0)
    # glEnable(GL_DEPTH_TEST)

    # Initialize trees
    create_trees()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
