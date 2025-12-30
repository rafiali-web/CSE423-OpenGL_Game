from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random

# ==================== GAME CONSTANTS & VARIABLES ====================
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000

# Delta time variables
last_frame_time = time.time()
delta_time = 0.016

# Player settings - FASTER MOVEMENT
player_pos = [0, 0, 100]
player_angle = 0
player_speed = 600
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
dash_speed_multiplier = 4.0

# Health bar colors (5 parts) - from green (full) to red (low)
HEALTH_COLORS = [
    (1.0, 0.0, 0.0),    # Red
    (1.0, 0.5, 0.0),    # Orange
    (1.0, 1.0, 0.0),    # Yellow
    (0.5, 1.0, 0.0),    # Yellow-Green
    (0.0, 1.0, 0.0)     # Green
]

# Arena boundaries - MADE SMALLER
ARENA_SIZE = 5000
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

# Diamonds
last_diamond_spawn = time.time()
diamond_spawn_interval = 4.0
ground_diamonds = []
falling_diamonds = []
regular_diamond_score = 10
special_diamond_health = 1
diamond_ground_lifetime = 10

# ==================== GOLDEN KEYS ====================
class GoldenKey:        
    def __init__(self, pos):
        self.pos = pos.copy()
        self.collected = False
        self.radius = 60
        self.rotation_angle = 0.0
        self.hover_offset = 0.0
        self.hover_speed = 2.0
        self.color = (1.0, 0.84, 0.0)
        self.glow_pulse = 0.0

golden_keys = []

# ==================== ENEMIES ====================
class Enemy:
    def __init__(self, enemy_type, pos):
        self.type = enemy_type
        self.pos = pos.copy()
        self.alive = True
        self.angle = random.uniform(0, 360)
        self.patrol_center = pos.copy()
        self.patrol_radius = 400
        self.patrol_angle = 0
        self.patrol_speed = 60
        
        # Type 0: Stationary Human with shooting ability
        if enemy_type == 0:
            self.health = 1
            self.max_health = 1
            self.radius = 40
            self.size = 60
            self.color = (1.0, 0.0, 0.0)
            self.speed = 0
            self.score_value = 50
            self.shoot_cooldown = 0
            self.shoot_interval = 3.0
            
        # Type 1: Patrolling Giant
        elif enemy_type == 1:
            self.health = 2
            self.max_health = 2
            self.radius = 120
            self.size = 180
            self.color = (0.8, 0.6, 0.4)
            self.speed = 80
            self.score_value = 100
            
        # Type 2: Chasing Dinosaur
        elif enemy_type == 2:
            self.health = 3
            self.max_health = 3
            self.radius = 120
            self.size = 150
            self.color = (0.8, 0.0, 0.8)
            self.speed = 240
            self.score_value = 150
        
        self.damage_timer = 0
        self.damage_duration = 0.3

enemies = []

# ==================== ENEMY PROJECTILES ====================
class EnemyProjectile:
    def __init__(self, pos, target_pos):
        self.pos = pos.copy()
        self.alive = True
        self.radius = 15
        self.color = (1.0, 0.3, 0.0)
        self.damage = 1
        
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            self.velocity_x = (dx / dist) * 300
            self.velocity_y = (dy / dist) * 300
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        self.velocity_z = 200
        self.gravity = 300
        self.lifetime = 0
        self.max_lifetime = 5.0

enemy_projectiles = []

# ==================== DIAMONDS ====================
class Diamond:
    def __init__(self, pos, diamond_type=0):
        self.pos = pos.copy()
        self.type = diamond_type
        self.fall_speed = random.uniform(80, 120)
        self.collected = False
        self.spawn_time = time.time()
        self.radius = 75
        self.pulse = 0.0
        self.pulse_speed = 5.0
        self.on_ground = False
        self.ground_time = 0
        self.rotation_angle = 0.0
        
        if diamond_type == 0:
            self.color = (0.0, 1.0, 1.0)
        else:
            self.color = (1.0, 0.84, 0.0)

# ==================== BULLETS ====================
# ==================== BULLETS ====================
class Bullet:
    def __init__(self, pos, angle, bullet_type=0):
        self.pos = pos.copy()
        self.angle = angle
        self.type = bullet_type
        self.alive = True
        self.distance_traveled = 0
        
        # Type 0: Pistol (1 damage, long range)
        if bullet_type == 0:
            self.speed = 600
            self.radius = 8
            self.max_distance = 15000
            self.damage = 1
            self.color = (1.0, 1.0, 0.0)
            self.trail = []
        
        # Type 2: Cannon (5 DAMAGE - ONE-SHOTS ALL ENEMIES, short range, arc trajectory)
        elif bullet_type == 2:
            self.speed = 450
            self.radius = 30
            self.max_distance = 800
            self.damage = 5  # HIGHEST DAMAGE - ONE-SHOT KILL
            self.color = (1.0, 0.3, 0.0)
            self.gravity = 200
            self.velocity_z = 250
            self.trail = []
        
        # Default fallback
        else:
            self.speed = 400
            self.radius = 20
            self.max_distance = 800
            self.damage = 1
            self.color = (1.0, 0.5, 0.0)

bullets = []
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
    return (abs(pos[0]) > BOUNDARY_SIZE or abs(pos[1]) > BOUNDARY_SIZE)

def bounce_from_boundary(pos):
    if pos[0] > BOUNDARY_SIZE:
        pos[0] = BOUNDARY_SIZE - 10
    elif pos[0] < -BOUNDARY_SIZE:
        pos[0] = -BOUNDARY_SIZE + 10
    
    if pos[1] > BOUNDARY_SIZE:
        pos[1] = BOUNDARY_SIZE - 10
    elif pos[1] < -BOUNDARY_SIZE:
        pos[1] = -BOUNDARY_SIZE + 10

# ==================== LEVEL MANAGEMENT ====================
def get_level_info():
    level_configs = {
        1: {"name": "Level 1", "description": "Starting challenge", "enemies": [0, 0, 1]},
        2: {"name": "Level 2", "description": "More enemies", "enemies": [0, 0, 1, 1, 2]},
        3: {"name": "Level 3", "description": "Getting tough", "enemies": [0, 1, 1, 2, 2]},
        4: {"name": "Level 4", "description": "Many foes", "enemies": [0, 1, 2, 2, 2]},
        5: {"name": "Level 5", "description": "Halfway there", "enemies": [1, 1, 2, 2, 2]},
        6: {"name": "Level 6", "description": "Heavy assault", "enemies": [0, 1, 1, 2, 2, 2]},
        7: {"name": "Level 7", "description": "Intense battle", "enemies": [1, 1, 2, 2, 2, 2]},
        8: {"name": "Level 8", "description": "Near the end", "enemies": [1, 2, 2, 2, 2, 2]},
        9: {"name": "Level 9", "description": "Almost done", "enemies": [2, 2, 2, 2, 2, 2]},
        10: {"name": "Level 10 - FINAL", "description": "Final challenge!", "enemies": [1, 2, 2, 2, 2, 2, 2]},
    }
    
    return level_configs.get(current_level, level_configs[1])

def spawn_enemies_for_level():
    global enemies
    
    enemies.clear()
    level_info = get_level_info()
    
    enemy_types = level_info["enemies"]
    enemies_per_type = 5 + current_level * 2
    
    for enemy_type in enemy_types:
        for _ in range(enemies_per_type):
            angle = random.uniform(0, 360)
            distance = random.uniform(500, BOUNDARY_SIZE - 200)
            x = distance * math.cos(math.radians(angle))
            y = distance * math.sin(math.radians(angle))
            z = 40
            
            enemy = Enemy(enemy_type, [x, y, z])
            
            # Scale health with level
            difficulty_multiplier = 1 + (current_level - 1) * 0.3
            enemy.health = int(enemy.health * difficulty_multiplier)
            enemy.max_health = enemy.health
            
            enemies.append(enemy)

def check_level_completion():
    global level_complete, level_transition_timer, enemies_killed_this_level
    
    if level_complete:
        return
    
    required = enemies_required_per_level[min(current_level - 1, len(enemies_required_per_level) - 1)]
    if enemies_killed_this_level >= required:
        level_complete = True
        level_transition_timer = level_transition_duration

def advance_level():
    global current_level, level_complete, enemies_killed_this_level, player_pos, player_angle
    
    if current_level >= max_level:
        return
    
    current_level += 1
    level_complete = False
    enemies_killed_this_level = 0
    
    randomize_player_position()
    create_jungle_environment()
    spawn_enemies_for_level()

def update_level_transition():
    global level_transition_timer
    
    if level_complete and level_transition_timer > 0:
        level_transition_timer -= delta_time
        
        if level_transition_timer <= 0:
            advance_level()

def randomize_player_position():
    global player_pos, player_angle
    
    safe_zone = BOUNDARY_SIZE - 1000
    player_pos[0] = random.uniform(-safe_zone, safe_zone)
    player_pos[1] = random.uniform(-safe_zone, safe_zone)
    player_pos[2] = 100
    
    player_angle = random.uniform(0, 360)
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



def draw_sky():
    """Draw vibrant daytime sky with gradient and clouds."""
    # Disable depth testing for sky to ensure it's in background
    glDisable(GL_DEPTH_TEST)
    
    # Vibrant daytime sky gradient - from bright blue at top to light cyan at horizon
    glBegin(GL_QUADS)
    # Top - bright blue
    glColor3f(0.4, 0.7, 1.0)  # Bright sky blue
    glVertex3f(-BOUNDARY_SIZE * 2, -BOUNDARY_SIZE * 2, 2500)
    glVertex3f(BOUNDARY_SIZE * 2, -BOUNDARY_SIZE * 2, 2500)
    # Upper middle - light blue
    glColor3f(0.6, 0.85, 1.0)  # Light sky blue
    glVertex3f(BOUNDARY_SIZE * 2, BOUNDARY_SIZE * 2, 1800)
    glVertex3f(-BOUNDARY_SIZE * 2, BOUNDARY_SIZE * 2, 1800)
    glEnd()
    
    glBegin(GL_QUADS)
    # Lower middle - very light blue
    glColor3f(0.7, 0.9, 1.0)  # Very light blue
    glVertex3f(-BOUNDARY_SIZE * 2, -BOUNDARY_SIZE * 2, 1800)
    glVertex3f(BOUNDARY_SIZE * 2, -BOUNDARY_SIZE * 2, 1800)
    # Horizon - light cyan/white
    glColor3f(0.85, 0.95, 1.0)  # Near white with blue tint
    glVertex3f(BOUNDARY_SIZE * 2, BOUNDARY_SIZE * 2, 300)
    glVertex3f(-BOUNDARY_SIZE * 2, BOUNDARY_SIZE * 2, 300)
    glEnd()
    
    # Bright sun - daytime version
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslatef(BOUNDARY_SIZE * 0.6, BOUNDARY_SIZE * 0.6, 1800)  # Position in sky
    glColor3f(1.0, 0.98, 0.7)  # Bright yellow sun
    glutSolidSphere(120, 24, 24)  # Larger, brighter sun
    glPopMatrix()
    glDisable(GL_DEPTH_TEST)
    
    # Fluffy white clouds for daytime
    glColor3f(1.0, 1.0, 1.0)  # Pure white clouds
    cloud_positions = [
        (BOUNDARY_SIZE * 0.4, BOUNDARY_SIZE * 0.4, 1500),
        (-BOUNDARY_SIZE * 0.3, BOUNDARY_SIZE * 0.7, 1400),
        (BOUNDARY_SIZE * 0.5, -BOUNDARY_SIZE * 0.4, 1300),
        (-BOUNDARY_SIZE * 0.7, -BOUNDARY_SIZE * 0.2, 1200),
        (BOUNDARY_SIZE * 0.8, BOUNDARY_SIZE * 0.8, 1600),
        (-BOUNDARY_SIZE * 0.6, BOUNDARY_SIZE * 0.9, 1450),
    ]
    
    for cx, cy, cz in cloud_positions:
        glPushMatrix()
        glTranslatef(cx, cy, cz)
        for i in range(6):  # More cloud particles
            glPushMatrix()
            glTranslatef(random.uniform(-50, 50), random.uniform(-35, 35), random.uniform(-20, 20))
            glutSolidSphere(random.uniform(50, 90), 12, 12)  # Larger, fluffier clouds
            glPopMatrix()
        glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)

def draw_health_bar():
    """Draw health bar on top of screen with 5 distinct colored segments."""
    # Background for the entire bar
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 60)
    glVertex2f(WINDOW_WIDTH//2 + 150, WINDOW_HEIGHT - 60)
    glVertex2f(WINDOW_WIDTH//2 + 150, WINDOW_HEIGHT - 30)
    glVertex2f(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 30)
    glEnd()
    
    # Draw 5 distinct segments
    segment_width = 50
    spacing = 5
    total_width = 5 * segment_width + 4 * spacing
    
    # Start position (centered)
    start_x = WINDOW_WIDTH//2 - total_width//2
    
    for i in range(max_health):
        segment_x = start_x + i * (segment_width + spacing)
        segment_y = WINDOW_HEIGHT - 55
        
        if i < player_health:
            glColor3f(*HEALTH_COLORS[i])
        else:
            glColor3f(0.1, 0.1, 0.1)  # Dark gray for empty segment
        
        glBegin(GL_QUADS)
        glVertex2f(segment_x, segment_y)
        glVertex2f(segment_x + segment_width, segment_y)
        glVertex2f(segment_x + segment_width, segment_y + 20)
        glVertex2f(segment_x, segment_y + 20)
        glEnd()
        
        # Draw segment border
        glColor3f(0.8, 0.8, 0.8)
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(segment_x, segment_y)
        glVertex2f(segment_x + segment_width, segment_y)
        glVertex2f(segment_x + segment_width, segment_y + 20)
        glVertex2f(segment_x, segment_y + 20)
        glEnd()

def draw_dash_indicator():
    """Draw dash mode indicator."""
    if dash_timer > 0:
        glColor4f(0.5, 0.8, 0.0, 0.5)  # Semi-transparent dash color
        glBegin(GL_QUADS)
        glVertex2f(WINDOW_WIDTH//2 - 200, 30)
        glVertex2f(WINDOW_WIDTH//2 - 200 + 400 * (dash_timer / dash_duration), 30)
        glVertex2f(WINDOW_WIDTH//2 - 200 + 400 * (dash_timer / dash_duration), 50)
        glVertex2f(WINDOW_WIDTH//2 - 200, 50)
        glEnd()
        
        glColor3f(1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH//2 - 100, 15, "DASH ACTIVE")
    elif dash_cooldown > 0:
        glColor4f(1.0, 0.5, 0.0, 0.5)  # Semi-transparent cooldown color
        glBegin(GL_QUADS)
        glVertex2f(WINDOW_WIDTH//2 - 200, 30)
        glVertex2f(WINDOW_WIDTH//2 - 200 + 400 * (1 - dash_cooldown / dash_cooldown_duration), 30)
        glVertex2f(WINDOW_WIDTH//2 - 200 + 400 * (1 - dash_cooldown / dash_cooldown_duration), 50)
        glVertex2f(WINDOW_WIDTH//2 - 200, 50)
        glEnd()
        
        glColor3f(1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH//2 - 100, 15, "DASH COOLDOWN")

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text at screen coordinates."""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
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

def draw_pause_overlay():
    """Draw pause overlay screen."""
    glColor4f(0.1, 0.1, 0.1, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    glVertex2f(0, WINDOW_HEIGHT)
    glEnd()
    
    draw_text(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 50, "GAME PAUSED", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 20, "Press SPACE to Resume")
    draw_text(WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 60, f"Score: {player_score}")
    draw_text(WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 100, f"Health: {player_health}/{max_health}")

def draw_minimap():
    """Draw a minimap."""
    map_size = 200
    map_pos = [WINDOW_WIDTH - map_size - 20, 20]
    
    glColor4f(0.1, 0.1, 0.1, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(map_pos[0], map_pos[1])
    glVertex2f(map_pos[0] + map_size, map_pos[1])
    glVertex2f(map_pos[0] + map_size, map_pos[1] + map_size)
    glVertex2f(map_pos[0], map_pos[1] + map_size)
    glEnd()
    
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(map_pos[0], map_pos[1])
    glVertex2f(map_pos[0] + map_size, map_pos[1])
    glVertex2f(map_pos[0] + map_size, map_pos[1] + map_size)
    glVertex2f(map_pos[0], map_pos[1] + map_size)
    glEnd()
    
    player_map_x = map_pos[0] + (player_pos[0] + BOUNDARY_SIZE) / (2 * BOUNDARY_SIZE) * map_size
    player_map_y = map_pos[1] + (player_pos[1] + BOUNDARY_SIZE) / (2 * BOUNDARY_SIZE) * map_size
    
    player_map_x = max(map_pos[0] + 2, min(player_map_x, map_pos[0] + map_size - 2))
    player_map_y = max(map_pos[1] + 2, min(player_map_y, map_pos[1] + map_size - 2))
    
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(player_map_x, player_map_y, 0)
    glRotatef(player_angle, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 5)
    glVertex2f(-3, -3)
    glVertex2f(3, -3)
    glEnd()
    glPopMatrix()
    
    for enemy in enemies:
        if enemy.alive:
            enemy_map_x = map_pos[0] + (enemy.pos[0] + BOUNDARY_SIZE) / (2 * BOUNDARY_SIZE) * map_size
            enemy_map_y = map_pos[1] + (enemy.pos[1] + BOUNDARY_SIZE) / (2 * BOUNDARY_SIZE) * map_size
            
            if (map_pos[0] <= enemy_map_x <= map_pos[0] + map_size and
                map_pos[1] <= enemy_map_y <= map_pos[1] + map_size):
                
                if enemy.type == 0:
                    glColor3f(1.0, 0.0, 0.0)  # Red for stationary
                elif enemy.type == 1:
                    glColor3f(0.8, 0.6, 0.4)  # Brown for giant
                else:
                    glColor3f(0.4, 0.8, 0.2)  # Green for dinosaur
                
                glPointSize(4)
                glBegin(GL_POINTS)
                glVertex2f(enemy_map_x, enemy_map_y)
                glEnd()

# ==================== UPDATE FUNCTIONS ====================
def update_dash_mode():
    """Update dash mode timer and cooldown."""
    global dash_timer, dash_mode, dash_cooldown
    
    current_time = time.time()
    
    if dash_timer > 0:
        dash_timer -= 0.016  # Assuming 60 FPS
        if dash_timer <= 0:
            dash_mode = False
            dash_timer = 0
    
    if dash_cooldown > 0:
        dash_cooldown -= 0.016
        if dash_cooldown <= 0:
            dash_cooldown = 0

def update_dash_mode():
    """Update dash mode timer and cooldown."""
    global dash_timer, dash_mode, dash_cooldown
    
    current_time = time.time()
    
    if dash_timer > 0:
        dash_timer -= 0.016  # Assuming 60 FPS
        if dash_timer <= 0:
            dash_mode = False
            dash_timer = 0
    
    if dash_cooldown > 0:
        dash_cooldown -= 0.016
        if dash_cooldown <= 0:
            dash_cooldown = 0

def update_player():
    """Update player position."""
    global dash_mode, dash_timer
    
    if is_dead or game_paused:
        return
    
    # Update dash mode
    update_dash_mode()
    
    if check_boundary_collision(player_pos):
        bounce_from_boundary(player_pos)

def update_enemies():
    """Update enemy movements and spawn chasing enemies."""
    global chasing_enemies_spawned, last_chasing_spawn
    
    if game_paused:
        return
    
    current_time = time.time()
    
    # Spawn chasing enemies one by one
    if (chasing_enemies_spawned < chasing_enemies_to_spawn and
        current_time - last_chasing_spawn > chasing_spawn_interval):
        
        # Spawn dinosaur at edge of arena
        angle = random.uniform(0, 360)
        distance = BOUNDARY_SIZE - 100
        x = distance * math.cos(math.radians(angle))
        y = distance * math.sin(math.radians(angle))
        
        enemies.append(Enemy(2, [x, y, 40]))
        chasing_enemies_spawned += 1
        last_chasing_spawn = current_time
    
    for enemy in enemies:
        if not enemy.alive:
            continue
        
        # Update damage timer
        if enemy.damage_timer > 0:
            enemy.damage_timer -= 0.016
        
        if enemy.type == 1:  # Patrolling enemy (giant)
            enemy.patrol_angle += enemy.patrol_speed
            enemy.patrol_angle = normalize_angle(enemy.patrol_angle)
            
            enemy.pos[0] = enemy.patrol_center[0] + enemy.patrol_radius * math.cos(math.radians(enemy.patrol_angle))
            enemy.pos[1] = enemy.patrol_center[1] + enemy.patrol_radius * math.sin(math.radians(enemy.patrol_angle))
            
        elif enemy.type == 2:  # Chasing enemy (dinosaur) - faster movement
            dx = player_pos[0] - enemy.pos[0]
            dy = player_pos[1] - enemy.pos[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 50:
                enemy.pos[0] += (dx/dist) * enemy.speed
                enemy.pos[1] += (dy/dist) * enemy.speed
                
                # Face player
                enemy.angle = math.degrees(math.atan2(dy, dx))
        
        if check_boundary_collision(enemy.pos):
            bounce_from_boundary(enemy.pos)

def update_bullets():
    """Update bullet positions and check collisions."""
    global player_score
    
    if game_paused:
        return
    
    for bullet in bullets[:]:
        if not bullet.alive:
            bullets.remove(bullet)
            continue
        
        bullet.pos[0] += bullet.speed * math.cos(math.radians(bullet.angle))
        bullet.pos[1] += bullet.speed * math.sin(math.radians(bullet.angle))
        bullet.distance_traveled += bullet.speed
        
        if bullet.type == 0:
            bullet.trail.append(bullet.pos.copy())
            if len(bullet.trail) > 10:
                bullet.trail.pop(0)
        
        if bullet.distance_traveled > bullet.max_distance:
            bullet.alive = False
            continue
        
        if check_boundary_collision(bullet.pos):
            bullet.alive = False
            continue
        
        # Check collision with enemies
        for enemy in enemies:
            if enemy.alive and distance_2d(bullet.pos, enemy.pos) < (bullet.radius + enemy.radius):
                enemy.health -= 1
                enemy.damage_timer = enemy.damage_duration
                
                if enemy.health <= 0:
                    enemy.alive = False
                    # Different scores for different enemies
                    if enemy.type == 0:  # Stationary
                        player_score += 50
                    elif enemy.type == 1:  # Giant
                        player_score += 100
                    else:  # Dinosaur
                        player_score += 150
                
                bullet.alive = False
                break

def update_diamonds():
    """Update falling diamonds and ground diamonds."""
    global last_diamond_spawn, player_score, player_health, falling_diamonds, ground_diamonds
    
    if game_paused:
        return
    
    current_time = time.time()
    
    if current_time - last_diamond_spawn > diamond_spawn_interval and not is_dead:
        x = player_pos[0] + random.randint(-500, 500)
        y = player_pos[1] + random.randint(-500, 500)
        
        x = max(-BOUNDARY_SIZE + 100, min(x, BOUNDARY_SIZE - 100))
        y = max(-BOUNDARY_SIZE + 100, min(y, BOUNDARY_SIZE - 100))
        
        diamond_type = 1 if random.random() < 0.25 else 0
        diamond = Diamond([x, y, 500], diamond_type)
        falling_diamonds.append(diamond)
        
        last_diamond_spawn = current_time
    
    for diamond in falling_diamonds[:]:
        diamond.pulse += diamond.pulse_speed * 0.016
        
        if diamond.type == 1:
            for particle in diamond.glitter_particles:
                particle['pos'][0] += particle['vel'][0] * 0.016
                particle['pos'][1] += particle['vel'][1] * 0.016
                particle['pos'][2] += particle['vel'][2] * 0.016
                particle['life'] -= 0.016
                if particle['life'] <= 0:
                    particle['pos'] = [0, 0, 0]
                    particle['vel'] = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(2, 8)]
                    particle['life'] = random.uniform(0.5, 1.5)
        
        diamond.pos[2] -= diamond.fall_speed
        
        if diamond.pos[2] <= GROUND_Z + 20:
            diamond.pos[2] = GROUND_Z + 20
            diamond.on_ground = True
            diamond.ground_time = current_time
            
            falling_diamonds.remove(diamond)
            ground_diamonds.append(diamond)
            continue
        
        if (not diamond.collected and 
            distance_3d(diamond.pos, player_pos) < 50):
            
            diamond.collected = True
            if diamond.type == 0:
                player_score += regular_diamond_score
            else:
                if player_health < max_health:
                    player_health += special_diamond_health
            
            falling_diamonds.remove(diamond)
            continue
    
    for diamond in ground_diamonds[:]:
        diamond.pulse += diamond.pulse_speed * 0.008
        
        if (not diamond.collected and 
            distance_2d(diamond.pos, player_pos) < 40 and
            abs(diamond.pos[2] - player_pos[2]) < 60):
            
            diamond.collected = True
            if diamond.type == 0:
                player_score += regular_diamond_score
            else:
                if player_health < max_health:
                    player_health += special_diamond_health
            
            ground_diamonds.remove(diamond)
            continue
        
        if current_time - diamond.ground_time > diamond_ground_lifetime:
            ground_diamonds.remove(diamond)

def check_enemy_collisions():
    """Check collisions between player and enemies."""
    global player_health, is_dead
    
    if is_dead or game_paused:
        return
    
    for enemy in enemies:
        if enemy.alive and distance_2d(player_pos, enemy.pos) < 60:
            player_health -= 1
            
            dx = player_pos[0] - enemy.pos[0]
            dy = player_pos[1] - enemy.pos[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                player_pos[0] += (dx/dist) * 30
                player_pos[1] += (dy/dist) * 30
            
            if player_health <= 0:
                is_dead = True
                player_health = 0
            break

def setup_camera():
    """Configure drone-like camera following player from farther distance."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Drone camera: behind and above player, looking at player
    camera_offset_x = camera_distance * math.cos(math.radians(player_angle + 180))
    camera_offset_y = camera_distance * math.sin(math.radians(player_angle + 180))
    
    camera_x = player_pos[0] + camera_offset_x
    camera_y = player_pos[1] + camera_offset_y
    camera_z = player_pos[2] + camera_height
    
    # Look at player's upper body to see legs better
    gluLookAt(camera_x, camera_y, camera_z,
              player_pos[0], player_pos[1], player_pos[2] + 40,  # Look at upper body
              0, 0, 1)

# ==================== INPUT HANDLERS ====================
def activate_dash():
    """Activate dash mode."""
    global dash_mode, dash_timer, dash_cooldown
    
    if dash_cooldown <= 0 and not dash_mode:
        dash_mode = True
        dash_timer = dash_duration
        dash_cooldown = dash_cooldown_duration

def keyboardListener(key, x, y):
    """Handle keyboard input for movement."""
    global player_pos, player_angle, is_dead, player_health, player_score, game_paused
    
    if key == b' ' and not is_dead:
        game_paused = not game_paused
        return
    
    if game_paused:
        return
    
    if is_dead:
        if key == b'r' or key == b'R':
            reset_game()
        return
    
    # Dash mode activation
    if key == b'f' or key == b'F':
        activate_dash()
        return
    
    # Calculate movement speed (dash mode is faster)
    move_speed = player_speed * (dash_speed_multiplier if dash_mode else 1.0)
    
    if key == b'w' or key == b'W':
        # Move forward in direction player is facing
        player_pos[0] += move_speed * math.cos(math.radians(player_angle))
        player_pos[1] += move_speed * math.sin(math.radians(player_angle))
        update_player()
    
    elif key == b's' or key == b'S':
        # Move backward (opposite direction)
        player_pos[0] -= move_speed * math.cos(math.radians(player_angle))
        player_pos[1] -= move_speed * math.sin(math.radians(player_angle))
        update_player()
    
    elif key == b'a' or key == b'A':
        # Strafe left (perpendicular to facing direction)
        player_pos[0] += move_speed * math.cos(math.radians(player_angle + 90))
        player_pos[1] += move_speed * math.sin(math.radians(player_angle + 90))
        update_player()
    
    elif key == b'd' or key == b'D':
        # Strafe right (perpendicular to facing direction)
        player_pos[0] += move_speed * math.cos(math.radians(player_angle - 90))
        player_pos[1] += move_speed * math.sin(math.radians(player_angle - 90))
        update_player()
    
    elif key == b'q' or key == b'Q':
        # Rotate left
        player_angle += 10
        player_angle = normalize_angle(player_angle)
    
    elif key == b'e' or key == b'E':
        # Rotate right
        player_angle -= 10
        player_angle = normalize_angle(player_angle)
    
    elif key == b'r' or key == b'R':
        reset_game()

def specialKeyListener(key, x, y):
    """Handle special keys (not used for camera anymore)."""
    pass

def mouseListener(button, state, x, y):
    """Handle mouse clicks for shooting."""
    if is_dead or state != GLUT_DOWN or game_paused:
        return
    
    # Bullet comes from gun direction (player's facing angle)
    # Gun position relative to player (on right hand)
    gun_offset_x = 25 * math.cos(math.radians(player_angle + 90))
    gun_offset_y = 25 * math.sin(math.radians(player_angle + 90))
    
    muzzle_distance = 60
    muzzle_x = player_pos[0] + gun_offset_x + muzzle_distance * math.cos(math.radians(player_angle))
    muzzle_y = player_pos[1] + gun_offset_y + muzzle_distance * math.sin(math.radians(player_angle))
    muzzle_z = player_pos[2] + 40
    
    if button == GLUT_LEFT_BUTTON:
        bullet = Bullet([muzzle_x, muzzle_y, muzzle_z], player_angle, 0)
        bullets.append(bullet)
    
    elif button == GLUT_RIGHT_BUTTON:
        bullet = Bullet([muzzle_x, muzzle_y, muzzle_z], player_angle, 1)
        bullets.append(bullet)



####
def idle():
    """Idle function for game updates."""
    if not is_dead and not game_paused:
        update_enemies()
        update_bullets()
        update_diamonds()
        check_enemy_collisions()
    
    glutPostRedisplay()

# ==================== MAIN FUNCTION ====================
def main():
    """Initialize and run the game."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"DRONE CAMERA ARENA - Enhanced Version")
    
    glClearColor(0.7, 0.85, 1.0, 1.0)  # Darker background color
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    
    # Disable blending for most objects (except UI)
    glDisable(GL_BLEND)
    
    # Better lighting setup
    light_pos = [BOUNDARY_SIZE * 0.6, BOUNDARY_SIZE * 0.6, 1000, 1]
    light_color = [1.0, 1.0, 0.95, 1.0]
    ambient_color = [0.6, 0.6, 0.6, 1.0]
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0003)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0000005)
    
    create_jungle_environment()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    print("=" * 60)
    print("DRONE CAMERA ARENA - ENHANCED VERSION")
    print("=" * 60)
    print("FIXES & IMPROVEMENTS:")
    print("- FIXED: Yellow screen issue by simplifying sky colors")
    print("- ADDED: Solid, realistic boundary walls with brick pattern")
    print("- IMPROVED: Better lighting with attenuation")
    print("- FIXED: Drawing order to prevent visual artifacts")
    print("- ADDED: Proper depth testing for sky")
    print("=" * 60)
    print("FEATURES:")
    print("- DASH MODE: Press F to activate temporary speed boost")
    print("- Camera shows thrice the view distance")
    print("- Gun properly attached to player's hand, faces forward")
    print("- Detailed player legs with animation")
    print("- Dinosaurs move twice as fast (more challenging!)")
    print("- Bustling environment with trees, rocks, and houses")
    print("- Solid boundary walls that look like real stone walls")
    print("=" * 60)
    print("CONTROLS:")
    print("W - Move forward (facing direction)")
    print("S - Move backward")
    print("A - Strafe left")
    print("D - Strafe right")
    print("Q/E - Rotate player")
    print("F - Activate Dash Mode (speed boost)")
    print("Left Click - Fast shot")
    print("Right Click - Fireball")
    print("SPACE - Pause/Resume")
    print("R - Reset game")
    print("=" * 60)
    
    glutMainLoop()

if __name__ == "__main__":
    main()


