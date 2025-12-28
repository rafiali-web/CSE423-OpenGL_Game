from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000

# Player settings
player_pos = [0, 0, 50]
player_angle = 0
player_speed = 50
player_health = 5
max_health = 5
player_score = 0
is_dead = False
game_paused = False
dash_mode = False
dash_timer = 0
dash_duration = 0.5
dash_cooldown = 0
dash_cooldown_duration = 2.0
dash_speed_multiplier = 3.0

# Health bar colors (5 parts) - from green (full) to red (low)
HEALTH_COLORS = [
    (1.0, 0.0, 0.0),    # Red - lowest health
    (1.0, 0.5, 0.0),    # Orange
    (1.0, 1.0, 0.0),    # Yellow
    (0.8, 1.0, 0.0),    # Light Green
    (0.0, 1.0, 0.0)     # Green - full health
]

# Arena boundaries
ARENA_SIZE = 8000
BOUNDARY_SIZE = ARENA_SIZE - 400
GROUND_Z = 0

# Camera settings - Drone-like camera following player
camera_distance = 1200  # Increased to thrice the distance
camera_height = 600     # Increased height for better view
camera_angle = 0  # For orbiting around player

# Environment settings - More bustling
tree_count = 300        # Increased trees
rock_count = 150        # Increased rocks
house_count = 30        # Added houses


# Environment settings - More bustling
tree_count = 300        # Increased trees
rock_count = 150        # Increased rocks
house_count = 30        # Added houses

# Jungle environment
trees = []
rocks = []
houses = []

# Diamond spawn management
last_diamond_spawn = time.time()
diamond_spawn_interval = 4.0
ground_diamonds = []
falling_diamonds = []
regular_diamond_score = 10
special_diamond_health = 1
diamond_ground_lifetime = 10

# ==================== ENEMIES SYSTEM ====================
class Enemy:
    def __init__(self, enemy_type, pos):
        self.type = enemy_type  # 0: stationary (red human), 1: patrolling (giant), 2: chasing (dinosaur)
        self.pos = pos.copy()
        self.alive = True
        self.angle = random.uniform(0, 360)
        self.patrol_center = pos.copy()
        self.patrol_radius = 400
        self.patrol_angle = 0
        self.patrol_speed = 1
        
        # Enemy health based on type
        if enemy_type == 0:  # Stationary - 1 bullet to kill
            self.health = 1
            self.max_health = 1
            self.radius = 40
            self.size = 60
            self.color = (1.0, 0.0, 0.0)  # Bright red
            self.speed = 0  # Stationary
        elif enemy_type == 1:  # Patrolling (giant) - 2 bullets to kill
            self.health = 2
            self.max_health = 2
            self.radius = 120  # 3x bigger
            self.size = 180    # 3x bigger
            self.color = (0.8, 0.6, 0.4)  # Brownish giant
            self.speed = 1.5
        else:  # Chasing (dinosaur) - 3 bullets to kill, speed doubled
            self.health = 3
            self.max_health = 3
            self.radius = 80
            self.size = 100
            self.color = (0.4, 0.8, 0.2)  # Green dinosaur
            self.speed = 4.0  # Doubled speed
        
        self.damage_timer = 0
        self.damage_duration = 0.3

# Initialize enemies
enemies = []
# Stationary enemies (red humans) - 10 total
stationary_positions = set()
for _ in range(10):
    while True:
        x = random.randint(-BOUNDARY_SIZE + 500, BOUNDARY_SIZE - 500)
        y = random.randint(-BOUNDARY_SIZE + 500, BOUNDARY_SIZE - 500)
        pos = (x, y)
        if pos not in stationary_positions:
            stationary_positions.add(pos)
            enemies.append(Enemy(0, [x, y, 40]))
            break

# Patrolling enemies (giants) - 5 total
for _ in range(5):
    x = random.randint(-BOUNDARY_SIZE + 500, BOUNDARY_SIZE - 500)
    y = random.randint(-BOUNDARY_SIZE + 500, BOUNDARY_SIZE - 500)
    enemies.append(Enemy(1, [x, y, 40]))

# Chasing enemies (dinosaurs) - Will spawn one by one
chasing_enemies_to_spawn = 8  # Total dinosaurs to spawn
chasing_enemies_spawned = 0
last_chasing_spawn = time.time()
chasing_spawn_interval = 10  # Spawn a new dinosaur every 10 seconds


# ==================== DIAMONDS SYSTEM ====================
class Diamond:
    def __init__(self, pos, diamond_type=0):
        self.pos = pos.copy()
        self.type = diamond_type
        self.fall_speed = random.uniform(15, 25)
        self.collected = False
        self.spawn_time = time.time()
        self.radius = 75
        self.pulse = 0.0
        self.pulse_speed = 5.0
        self.on_ground = False
        self.ground_time = 0
        self.glitter_particles = []
        
        if diamond_type == 0:
            self.color = (0.0, 1.0, 1.0)  # Cyan
        else:
            self.color = (1.0, 0.84, 0.0)  # Golden
            
        if diamond_type == 1:
            for _ in range(20):
                self.glitter_particles.append({
                    'pos': [0, 0, 0],
                    'vel': [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(2, 8)],
                    'size': random.uniform(2, 5),
                    'life': random.uniform(0.5, 1.5)
                })

# ==================== BULLETS SYSTEM ====================
class Bullet:
    def __init__(self, pos, angle, bullet_type=0):
        # Bullet comes from gun direction
        self.pos = pos.copy()
        self.angle = angle
        self.type = bullet_type
        self.speed = 40 if bullet_type == 0 else 25
        self.radius = 8
        self.alive = True
        self.distance_traveled = 0
        self.max_distance = 800
        
        if bullet_type == 0:
            self.color = (1.0, 1.0, 0.0)  # Yellow
            self.trail = []
        else:
            self.color = (1.0, 0.5, 0.0)  # Orange

bullets = []

# ==================== JUNGLE ENVIRONMENT ====================
def create_jungle_environment():
    """Create trees, rocks, and houses for the bustling arena."""
    global trees, rocks, houses
    
    trees.clear()
    rocks.clear()
    houses.clear()
    
    # Create bustling environment
    boundary = BOUNDARY_SIZE - 100
    
    # Create perimeter trees
    trees_per_side = 40  # Increased perimeter trees
    for i in range(trees_per_side):
        # North side
        x = -boundary + (i * (2 * boundary) / (trees_per_side - 1))
        y = boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        # South side
        y = -boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        # East side
        x = boundary
        y = -boundary + (i * (2 * boundary) / (trees_per_side - 1))
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        # West side
        x = -boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
    
    # Random trees inside - more dense
    for _ in range(tree_count):
        x = random.randint(-boundary + 200, boundary - 200)
        y = random.randint(-boundary + 200, boundary - 200)
        create_tree_at([x, y, 0], size_factor=random.uniform(0.8, 1.8))
    
    # Colorful rocks - more dense
    for _ in range(rock_count):
        x = random.randint(-boundary + 200, boundary - 200)
        y = random.randint(-boundary + 200, boundary - 200)
        # Vibrant rock colors
        rock_color = random.choice([
            (0.8, 0.4, 0.2),  # Orange-brown
            (0.6, 0.3, 0.7),  # Purple
            (0.3, 0.6, 0.8),  # Blue
            (0.7, 0.7, 0.3),  # Yellowish
            (0.4, 0.8, 0.4),  # Green
            (0.9, 0.5, 0.8)   # Pink
        ])
        rocks.append({
            'pos': [x, y, 0],
            'size': random.uniform(40, 100),
            'color': rock_color,
            'rotation': random.uniform(0, 360)
        })
    
    # Create houses - bustling environment
    for _ in range(house_count):
        x = random.randint(-boundary + 300, boundary - 300)
        y = random.randint(-boundary + 300, boundary - 300)
        create_house_at([x, y, 0])

def create_tree_at(pos, size_factor=1.0):
    """Create a colorful tree."""
    tree_height = random.uniform(150, 250) * size_factor
    trunk_height = tree_height * 0.6
    crown_height = tree_height * 0.4
    
    # Vibrant tree colors
    crown_colors = [
        (0.3, 0.9, 0.4),   # Bright green
        (0.2, 0.95, 0.3),  # Lime green
        (0.4, 0.85, 0.3),  # Forest green
        (0.5, 0.9, 0.2),   # Light green
        (0.3, 0.8, 0.5),   # Emerald
        (0.4, 0.9, 0.3)    # Vibrant green
    ]
    
    trees.append({
        'pos': pos,
        'trunk_height': trunk_height,
        'trunk_radius': random.uniform(10, 20) * size_factor,
        'crown_radius': random.uniform(50, 80) * size_factor,
        'crown_height': crown_height,
        'trunk_color': (random.uniform(0.4, 0.6), random.uniform(0.3, 0.4), random.uniform(0.2, 0.3)),
        'crown_color': random.choice(crown_colors),
        'type': random.choice(['pine', 'round', 'palm', 'oak'])
    })

def create_house_at(pos):
    """Create a colorful house."""
    house_height = random.uniform(80, 150)
    house_width = random.uniform(60, 100)
    house_depth = random.uniform(60, 100)
    
    # Colorful house colors
    house_colors = [
        (0.9, 0.6, 0.5),  # Peach
        (0.7, 0.8, 0.9),  # Light blue
        (0.8, 0.9, 0.7),  # Light green
        (0.9, 0.8, 0.6),  # Beige
        (0.8, 0.7, 0.9),  # Lavender
        (0.6, 0.8, 0.8)   # Teal
    ]
    
    roof_colors = [
        (0.6, 0.3, 0.2),  # Brown
        (0.5, 0.2, 0.1),  # Dark brown
        (0.3, 0.3, 0.3),  # Dark gray
        (0.4, 0.2, 0.1)   # Chocolate
    ]
    
    houses.append({
        'pos': pos,
        'height': house_height,
        'width': house_width,
        'depth': house_depth,
        'color': random.choice(house_colors),
        'roof_color': random.choice(roof_colors),
        'rotation': random.uniform(0, 360)
    })
# ==================== UTILITY FUNCTIONS ====================
def distance_2d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def distance_3d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)

def normalize_angle(angle):
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def check_boundary_collision(pos):
    return (abs(pos[0]) > BOUNDARY_SIZE or 
            abs(pos[1]) > BOUNDARY_SIZE)

def bounce_from_boundary(pos):
    if pos[0] > BOUNDARY_SIZE:
        pos[0] = BOUNDARY_SIZE - 10
    elif pos[0] < -BOUNDARY_SIZE:
        pos[0] = -BOUNDARY_SIZE + 10
    
    if pos[1] > BOUNDARY_SIZE:
        pos[1] = BOUNDARY_SIZE - 10
    elif pos[1] < -BOUNDARY_SIZE:
        pos[1] = -BOUNDARY_SIZE + 10

# ==================== DRAWING FUNCTIONS ====================
def draw_player():
    """Draw the player character with proper gun placement and legs."""
    if is_dead:
        return
    
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)
    
    # Player torso
    if dash_mode:
        glColor3f(0.5, 0.8, 0.0)  # Dash mode color - brighter green
    else:
        glColor3f(0.0, 0.6, 0.0)  # Normal color
    
    glPushMatrix()
    glScalef(1.2, 0.8, 2.0)
    glutSolidCube(50)
    glPopMatrix()
    
    # Player head
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, 90)
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()
    
    # Player arms with gun on right hand
    glColor3f(1.0, 0.85, 0.7)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 30, 0, 60)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 6, 6, 40, 10, 10)
        glPopMatrix()
    
    # Player gun on right hand, facing forward (same as head)
    draw_player_gun()
    
    # Player legs (detailed with knees and feet)
    draw_player_legs()
    
    glPopMatrix()

def draw_player_gun():
    """Draw the gun on player's right hand, facing forward."""
    glColor3f(0.3, 0.3, 0.3)  # Gun metal color
    
    # Gun position on right hand
    glPushMatrix()
    # Position on right arm (side=1)
    glTranslatef(25, 20, 60)  # Adjusted position on arm
    
    # Gun body (facing forward)
    glRotatef(-90, 0, 1, 0)  # Rotate to point forward
    gluCylinder(gluNewQuadric(), 4, 4, 50, 10, 10)
    
    # Gun muzzle at the front
    glTranslatef(0, 0, 50)
    glutSolidCone(5, 12, 8, 8)
    
    # Gun handle
    glPushMatrix()
    glTranslatef(0, 0, 15)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 3, 15, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_player_legs():
    """Draw detailed player legs with knees and feet."""
    glColor3f(0.05, 0.05, 0.8)
    
    # Leg animation based on movement
    current_time = time.time()
    leg_swing = 0
    if dash_mode:
        leg_swing = 30 * math.sin(current_time * 20)  # Faster swing in dash mode
    else:
        leg_swing = 15 * math.sin(current_time * 10)  # Normal swing
    
    for side_idx, side in enumerate([-1, 1]):
        glPushMatrix()
        glTranslatef(side * 20, 0, 0)
        
        # Thigh
        glPushMatrix()
        glTranslatef(0, 0, -25)
        glRotatef(leg_swing * (1 if side_idx == 0 else -1), 1, 0, 0)  # Alternate swing
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 6, 30, 10, 10)
        
        # Knee
        glTranslatef(0, 0, -30)
        glutSolidSphere(5, 8, 8)
        
        # Shin
        glRotatef(-leg_swing * 0.5 * (1 if side_idx == 0 else -1), 1, 0, 0)
        gluCylinder(gluNewQuadric(), 6, 4, 25, 10, 10)
        
        # Foot
        glTranslatef(0, 0, -25)
        glColor3f(0.1, 0.1, 0.1)  # Dark color for shoes
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glScalef(1.5, 0.5, 1.0)
        glutSolidCube(15)
        glPopMatrix()
        
        glPopMatrix()
        glColor3f(0.05, 0.05, 0.8)  # Back to leg color
        
        glPopMatrix()

def draw_stationary_enemy(enemy):
    """Draw stationary enemy - looks like player but red."""
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    # Flash red when damaged
    if enemy.damage_timer > 0:
        glColor3f(1.0, 0.5, 0.5)  # Light red when damaged
    else:
        glColor3f(1.0, 0.0, 0.0)  # Bright red
    
    # Enemy torso (similar to player but red)
    glPushMatrix()
    glScalef(1.2, 0.8, 2.0)
    glutSolidCube(enemy.size)
    glPopMatrix()
    
    # Enemy head
    glColor3f(0.8, 0.0, 0.0)  # Dark red head
    glPushMatrix()
    glTranslatef(0, 0, 90)
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()
    
    # Enemy arms
    glColor3f(1.0, 0.5, 0.5)  # Light red arms
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 30, 0, 60)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 6, 6, 40, 10, 10)
        glPopMatrix()
    
    # Enemy legs
    glColor3f(0.8, 0.0, 0.0)  # Dark red legs
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, -25)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 2, 60, 10, 10)
        glPopMatrix()
    
    # Health bar above enemy
    draw_enemy_health_bar(enemy)
    
    glPopMatrix()

def draw_patrolling_enemy(enemy):
    """Draw patrolling enemy - giant (3x bigger)."""
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    # Flash when damaged
    if enemy.damage_timer > 0:
        glColor3f(1.0, 0.8, 0.6)  # Light brown when damaged
    else:
        glColor3f(0.8, 0.6, 0.4)  # Brown giant
    
    # Giant body (3x scale)
    glPushMatrix()
    glScalef(3.0, 3.0, 3.0)
    
    # Giant torso
    glPushMatrix()
    glScalef(1.2, 0.8, 2.0)
    glutSolidCube(20)  # Smaller base cube, scaled by 3x overall
    glPopMatrix()
    
    # Giant head
    glColor3f(0.7, 0.5, 0.3)  # Darker brown head
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glutSolidSphere(15, 20, 20)
    glPopMatrix()
    
    # Giant arms
    glColor3f(0.9, 0.7, 0.5)  # Light brown arms
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, 20)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 10)
        glPopMatrix()
    
    # Giant legs
    glColor3f(0.6, 0.4, 0.2)  # Dark brown legs
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 13, 0, -10)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 3, 40, 10, 10)
        glPopMatrix()
    
    glPopMatrix()  # End 3x scale
    
    # Health bar above giant
    draw_enemy_health_bar(enemy)
    
    glPopMatrix()

def draw_chasing_enemy(enemy):
    """Draw chasing enemy - dinosaur."""
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    # Flash when damaged
    if enemy.damage_timer > 0:
        glColor3f(0.6, 1.0, 0.4)  # Light green when damaged
    else:
        glColor3f(0.4, 0.8, 0.2)  # Green dinosaur
    
    # Dinosaur body
    glPushMatrix()
    glScalef(1.5, 0.8, 0.7)
    glutSolidSphere(enemy.radius * 0.8, 20, 20)
    glPopMatrix()
    
    # Dinosaur head
    glPushMatrix()
    glTranslatef(enemy.radius * 1.2, 0, enemy.radius * 0.3)
    glutSolidSphere(enemy.radius * 0.5, 15, 15)
    # Mouth
    glColor3f(0.8, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(enemy.radius * 0.3, 0, 0)
    glutSolidCone(enemy.radius * 0.2, enemy.radius * 0.4, 8, 8)
    glPopMatrix()
    glColor3f(0.4, 0.8, 0.2)  # Back to green
    glPopMatrix()
    
    # Dinosaur tail
    glPushMatrix()
    glTranslatef(-enemy.radius * 1.2, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glutSolidCone(enemy.radius * 0.4, enemy.radius * 1.5, 10, 10)
    glPopMatrix()
    
    # Dinosaur legs
    glColor3f(0.3, 0.7, 0.1)
    leg_positions = [
        (0.6, -0.5, -0.8),  # Front right
        (0.6, 0.5, -0.8),   # Front left
        (-0.6, -0.5, -0.8), # Back right
        (-0.6, 0.5, -0.8)   # Back left
    ]
    
    for dx, dy, dz in leg_positions:
        glPushMatrix()
        glTranslatef(enemy.radius * dx, enemy.radius * dy, enemy.radius * dz)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), enemy.radius * 0.2, enemy.radius * 0.15, enemy.radius * 0.8, 8, 8)
        glPopMatrix()
    
    # Health bar above dinosaur
    draw_enemy_health_bar(enemy)
    
    glPopMatrix()

def draw_enemy_health_bar(enemy):
    """Draw health bar above enemy."""
    if enemy.health < enemy.max_health:  # Only show if damaged
        glPushMatrix()
        glTranslatef(0, 0, enemy.size + 30)  # Position above enemy
        
        # Background
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(-30, -5)
        glVertex2f(30, -5)
        glVertex2f(30, 5)
        glVertex2f(-30, 5)
        glEnd()
        
        # Health
        health_ratio = enemy.health / enemy.max_health
        if enemy.type == 0:  # Red human
            glColor3f(1.0, 0.0, 0.0)
        elif enemy.type == 1:  # Giant
            glColor3f(1.0, 0.5, 0.0)
        else:  # Dinosaur
            glColor3f(0.0, 1.0, 0.0)
        
        glBegin(GL_QUADS)
        glVertex2f(-28, -3)
        glVertex2f(-28 + 56 * health_ratio, -3)
        glVertex2f(-28 + 56 * health_ratio, 3)
        glVertex2f(-28, 3)
        glEnd()
        
        glPopMatrix()

def draw_enemy(enemy):
    """Draw enemy based on type."""
    if not enemy.alive:
        return
    
    if enemy.type == 0:  # Stationary - red human
        draw_stationary_enemy(enemy)
    elif enemy.type == 1:  # Patrolling - giant
        draw_patrolling_enemy(enemy)
    else:  # Chasing - dinosaur
        draw_chasing_enemy(enemy)

def draw_diamond(diamond):
    """Draw a diamond with effects."""
    if diamond.collected:
        return
    
    glPushMatrix()
    glTranslatef(diamond.pos[0], diamond.pos[1], diamond.pos[2])
    
    pulse_size = 8.0 * math.sin(diamond.pulse)
    size = diamond.radius + pulse_size
    
    glColor3f(*diamond.color)
    
    glBegin(GL_TRIANGLES)
    # Top half
    for i in range(4):
        angle1 = i * 90
        angle2 = (i + 1) * 90
        x1 = size * 0.7 * math.cos(math.radians(angle1))
        y1 = size * 0.7 * math.sin(math.radians(angle1))
        x2 = size * 0.7 * math.cos(math.radians(angle2))
        y2 = size * 0.7 * math.sin(math.radians(angle2))
        
        glVertex3f(0, 0, size)
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
    
    # Bottom half
    for i in range(4):
        angle1 = i * 90
        angle2 = (i + 1) * 90
        x1 = size * 0.7 * math.cos(math.radians(angle1))
        y1 = size * 0.7 * math.sin(math.radians(angle1))
        x2 = size * 0.7 * math.cos(math.radians(angle2))
        y2 = size * 0.7 * math.sin(math.radians(angle2))
        
        glVertex3f(0, 0, -size)
        glVertex3f(x2, y2, 0)
        glVertex3f(x1, y1, 0)
    glEnd()
    
    if diamond.type == 1 and not diamond.on_ground:
        draw_glitter_effect(diamond)
    
    glPopMatrix()

def draw_glitter_effect(diamond):
    """Draw glitter particles for special diamonds."""
    for particle in diamond.glitter_particles:
        glPushMatrix()
        glTranslatef(particle['pos'][0], particle['pos'][1], particle['pos'][2])
        glColor3f(1.0, 1.0, 0.8)
        glutSolidSphere(particle['size'], 6, 6)
        glPopMatrix()

def draw_bullet(bullet):
    """Draw a bullet."""
    if not bullet.alive:
        return
    
    glPushMatrix()
    glTranslatef(bullet.pos[0], bullet.pos[1], bullet.pos[2])
    
    glColor3f(*bullet.color)
    
    if bullet.type == 0:
        gluSphere(gluNewQuadric(), bullet.radius, 10, 10)
        
        if len(bullet.trail) > 1:
            glBegin(GL_LINE_STRIP)
            for i, pos in enumerate(bullet.trail):
                alpha = i / len(bullet.trail)
                glColor4f(bullet.color[0], bullet.color[1], bullet.color[2], alpha * 0.5)
                glVertex3f(pos[0], pos[1], pos[2])
            glEnd()
    else:
        glColor3f(1.0, 0.5, 0.0)
        glutSolidSphere(bullet.radius * 1.5, 12, 12)
        glColor3f(1.0, 0.8, 0.0)
        glutSolidSphere(bullet.radius, 8, 8)
    
    glPopMatrix()

def draw_tree(tree):
    """Draw a colorful tree."""
    glPushMatrix()
    glTranslatef(tree['pos'][0], tree['pos'][1], tree['pos'][2])
    
    # Draw trunk
    glColor3f(*tree['trunk_color'])
    gluCylinder(gluNewQuadric(), tree['trunk_radius'], tree['trunk_radius'] * 0.7, 
                tree['trunk_height'], 12, 12)
    
    # Draw crown
    glColor3f(*tree['crown_color'])
    glTranslatef(0, 0, tree['trunk_height'])
    
    if tree['type'] == 'pine':
        glutSolidCone(tree['crown_radius'], tree['crown_height'], 12, 12)
    elif tree['type'] == 'palm':
        gluSphere(gluNewQuadric(), tree['crown_radius'] * 0.5, 10, 10)
        glColor3f(0.1, 0.5, 0.1)
        for i in range(6):
            glPushMatrix()
            glRotatef(i * 60, 0, 0, 1)
            glTranslatef(tree['crown_radius'] * 0.7, 0, 0)
            glutSolidCone(10, tree['crown_height'] * 0.7, 6, 6)
            glPopMatrix()
    elif tree['type'] == 'oak':
        # Oak tree with broader crown
        gluSphere(gluNewQuadric(), tree['crown_radius'] * 1.2, 15, 15)
    else:
        gluSphere(gluNewQuadric(), tree['crown_radius'], 12, 12)
    
    glPopMatrix()

def draw_rock(rock):
    """Draw a colorful rock."""
    glPushMatrix()
    glTranslatef(rock['pos'][0], rock['pos'][1], rock['pos'][2])
    glRotatef(rock['rotation'], 0, 1, 0)
    
    glColor3f(*rock['color'])
    glutSolidSphere(rock['size'], 10, 10)
    
    glPushMatrix()
    glTranslatef(rock['size'] * 0.3, rock['size'] * 0.2, rock['size'] * 0.4)
    glutSolidSphere(rock['size'] * 0.6, 8, 8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-rock['size'] * 0.4, rock['size'] * 0.3, -rock['size'] * 0.3)
    glutSolidSphere(rock['size'] * 0.5, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_house(house):
    """Draw a colorful house."""
    glPushMatrix()
    glTranslatef(house['pos'][0], house['pos'][1], house['pos'][2])
    glRotatef(house['rotation'], 0, 0, 1)
    
    # House body
    glColor3f(*house['color'])
    glPushMatrix()
    glScalef(house['width'], house['depth'], house['height'])
    glutSolidCube(1)
    glPopMatrix()
    
    # Roof
    glColor3f(*house['roof_color'])
    glPushMatrix()
    glTranslatef(0, 0, house['height'])
    glRotatef(90, 1, 0, 0)
    glutSolidCone(house['width'] * 0.8, house['height'] * 0.5, 4, 4)
    glPopMatrix()
    
    # Door
    glColor3f(0.4, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(0, house['depth'] * 0.5 + 1, 0)
    glScalef(0.3, 0.1, 0.5)
    glutSolidCube(house['height'])
    glPopMatrix()
    
    # Windows
    glColor3f(0.9, 0.9, 1.0)
    for i in [-1, 1]:
        for j in [-0.3, 0.3]:
            glPushMatrix()
            glTranslatef(i * house['width'] * 0.3, house['depth'] * 0.5 + 1, j * house['height'] * 0.3)
            glScalef(0.2, 0.1, 0.2)
            glutSolidCube(house['height'])
            glPopMatrix()
    
    glPopMatrix()

def draw_ground():
    """Draw vibrant daytime jungle ground."""
    # Vibrant green ground for daytime
    glColor3f(0.3, 0.85, 0.4)  # Brighter, more vibrant green
    glBegin(GL_QUADS)
    glVertex3f(-BOUNDARY_SIZE, -BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(BOUNDARY_SIZE, -BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(BOUNDARY_SIZE, BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(-BOUNDARY_SIZE, BOUNDARY_SIZE, GROUND_Z)
    glEnd()
    
    # Colorful grass details - more vibrant for daytime
    glPointSize(4)  # Slightly larger points
    glBegin(GL_POINTS)
    for _ in range(4000):  # More grass details
        x = random.uniform(-BOUNDARY_SIZE, BOUNDARY_SIZE)
        y = random.uniform(-BOUNDARY_SIZE, BOUNDARY_SIZE)
        # Random vibrant grass colors for daytime
        grass_color = random.choice([
            (0.4, 0.95, 0.3),   # Bright lime green
            (0.3, 0.9, 0.4),    # Emerald green
            (0.35, 0.85, 0.25), # Forest green
            (0.45, 0.9, 0.35),  # Light green
            (0.25, 0.8, 0.3),   # Dark green
        ])
        glColor3f(*grass_color)
        glVertex3f(x, y, GROUND_Z + 0.1)
    glEnd()

def draw_boundary_walls():
    """Draw solid, realistic-looking boundary walls."""
    wall_height = 400  # Increased height for more imposing walls
    wall_thickness = 50  # Thick walls
    
    # Wall textures/patterns
    wall_colors = [
        (0.65, 0.45, 0.25),   # Light brown stone
        (0.7, 0.5, 0.3),      # Medium brown stone
        (0.75, 0.55, 0.35),   # Light brown stone
        (0.8, 0.6, 0.4),      # Highlight stone
    ]
    
    # Draw all four walls
    walls = [
        # North wall
        {'pos': [0, BOUNDARY_SIZE, wall_height/2], 'rotation': 0},
        # South wall  
        {'pos': [0, -BOUNDARY_SIZE, wall_height/2], 'rotation': 0},
        # East wall
        {'pos': [BOUNDARY_SIZE, 0, wall_height/2], 'rotation': 90},
        # West wall
        {'pos': [-BOUNDARY_SIZE, 0, wall_height/2], 'rotation': 90},
    ]
    
    for wall in walls:
        glPushMatrix()
        glTranslatef(wall['pos'][0], wall['pos'][1], wall['pos'][2])
        glRotatef(wall['rotation'], 0, 0, 1)
        
        # Main wall structure
        glColor3f(0.4, 0.3, 0.2)  # Base color
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        
        # Back face
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        
        # Top face
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        
        # Bottom face
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glEnd()
        
        # Draw stone/brick pattern on front face
        brick_width = 200
        brick_height = 80
        brick_depth = 10
        
        for i in range(-int(BOUNDARY_SIZE/brick_width), int(BOUNDARY_SIZE/brick_width)):
            for j in range(-int(wall_height/(brick_height*2)), int(wall_height/(brick_height*2))):
                # Alternate brick pattern
                if (i + j) % 2 == 0:
                    continue
                    
                brick_x = i * brick_width + (brick_width/2 if j % 2 == 0 else 0)
                brick_z = j * brick_height * 0.8
                
                if (abs(brick_x) < BOUNDARY_SIZE - brick_width/2 and 
                    abs(brick_z) < wall_height/2 - brick_height/2):
                    
                    # Random brick color variation
                    brick_color = random.choice(wall_colors)
                    glColor3f(*brick_color)
                    
                    glPushMatrix()
                    glTranslatef(brick_x, -wall_thickness/2 - brick_depth/2, brick_z)
                    
                    # Brick face
                    glBegin(GL_QUADS)
                    glVertex3f(-brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(brick_width/2, -brick_depth/2, brick_height/2)
                    glVertex3f(-brick_width/2, -brick_depth/2, brick_height/2)
                    glEnd()
                    
                    # Brick edges (darker)
                    glColor3f(brick_color[0]*0.7, brick_color[1]*0.7, brick_color[2]*0.7)
                    glBegin(GL_QUADS)
                    # Top edge
                    glVertex3f(-brick_width/2, -brick_depth/2, brick_height/2)
                    glVertex3f(brick_width/2, -brick_depth/2, brick_height/2)
                    glVertex3f(brick_width/2, brick_depth/2, brick_height/2)
                    glVertex3f(-brick_width/2, brick_depth/2, brick_height/2)
                    # Bottom edge
                    glVertex3f(-brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(brick_width/2, brick_depth/2, -brick_height/2)
                    glVertex3f(-brick_width/2, brick_depth/2, -brick_height/2)
                    # Left edge
                    glVertex3f(-brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(-brick_width/2, -brick_depth/2, brick_height/2)
                    glVertex3f(-brick_width/2, brick_depth/2, brick_height/2)
                    glVertex3f(-brick_width/2, brick_depth/2, -brick_height/2)
                    # Right edge
                    glVertex3f(brick_width/2, -brick_depth/2, -brick_height/2)
                    glVertex3f(brick_width/2, -brick_depth/2, brick_height/2)
                    glVertex3f(brick_width/2, brick_depth/2, brick_height/2)
                    glVertex3f(brick_width/2, brick_depth/2, -brick_height/2)
                    glEnd()
                    
                    glPopMatrix()
        
        glPopMatrix()    




