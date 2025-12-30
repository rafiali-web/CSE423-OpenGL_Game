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
# ==================== UTILITY FUNCTIONS ==================== #rafi
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
# ==================== PLAYER DRAWING ====================
def draw_player():
    """Draw player with TWO GUNS"""
    if is_dead:
        return
    
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)
    
    scale = 1.5
    
    # Body
    glColor3f(*current_shirt_color)
    glPushMatrix()
    glScalef(1.2 * scale, 0.9 * scale, 1.8 * scale)
    glutSolidCube(45)
    glPopMatrix()
    
    # Head
    glColor3f(0.9, 0.7, 0.6)
    glPushMatrix()
    glTranslatef(0, 0, 70 * scale)
    gluSphere(gluNewQuadric(), 22 * scale, 12, 12)
    glPopMatrix()
    
    # Helmet
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 0, 75 * scale)
    glScalef(1.1, 1.1, 0.7)
    gluSphere(gluNewQuadric(), 23 * scale, 10, 10)
    glPopMatrix()
    
    # Arms
    arm_color = (0.9, 0.7, 0.6)
    
    # Left arm
    glColor3f(*arm_color)
    glPushMatrix()
    glTranslatef(-35 * scale, 0, 35 * scale)
    glRotatef(-20, 0, 1, 0)
    glRotatef(-30, 1, 0, 0)
    glScalef(0.3 * scale, 0.3 * scale, 1.2 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    # Right arm
    glPushMatrix()
    glTranslatef(35 * scale, 0, 35 * scale)
    glRotatef(20, 0, 1, 0)
    glRotatef(-30, 1, 0, 0)
    glScalef(0.3 * scale, 0.3 * scale, 1.2 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    # Legs
    glColor3f(0.2, 0.2, 0.4)
    
    glPushMatrix()
    glTranslatef(-15 * scale, 0, -35 * scale)
    glScalef(0.4 * scale, 0.4 * scale, 1.5 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15 * scale, 0, -35 * scale)
    glScalef(0.4 * scale, 0.4 * scale, 1.5 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    # Feet
    glColor3f(0.3, 0.2, 0.1)
    
    glPushMatrix()
    glTranslatef(-15 * scale, 8 * scale, -65 * scale)
    glScalef(0.4 * scale, 0.6 * scale, 0.3 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15 * scale, 8 * scale, -65 * scale)
    glScalef(0.4 * scale, 0.6 * scale, 0.3 * scale)
    glutSolidCube(35)
    glPopMatrix()
    
    # Draw both guns
    draw_pistol()
    draw_cannon()
    
    glPopMatrix()

def draw_pistol():
    """Draw pistol on LEFT hand"""
    scale = 1.5
    
    glColor3f(0.2, 0.2, 0.2)
    
    glPushMatrix()
    glTranslatef(-30 * scale, 50 * scale, 40 * scale)
    glRotatef(-90, 1, 0, 0)
    
    glPushMatrix()
    gluCylinder(gluNewQuadric(), 4 * scale, 4 * scale, 50 * scale, 8, 8)
    glPopMatrix()
    
    glColor3f(0.4, 0.3, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, -10 * scale)
    glRotatef(45, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5 * scale, 3 * scale, 20 * scale, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_cannon():
    """Draw cannon on RIGHT hand"""
    scale = 1.5
    
    if fire_gun_active:
        glColor3f(1.0, 0.3, 0.0)
    else:
        glColor3f(0.3, 0.3, 0.3)
    
    glPushMatrix()
    glTranslatef(30 * scale, 50 * scale, 40 * scale)
    glRotatef(-90, 1, 0, 0)
    
    glPushMatrix()
    gluCylinder(gluNewQuadric(), 12 * scale, 12 * scale, 30 * scale, 12, 12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 30 * scale)
    barrel_length = 100 * scale
    gluCylinder(gluNewQuadric(), 10 * scale, 8 * scale, barrel_length, 12, 12)
    glPopMatrix()
    
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0, 0, 30 * scale + barrel_length)
    gluSphere(gluNewQuadric(), 11 * scale, 8, 8)
    glPopMatrix()
    
    glPopMatrix()


#Rafi Start from here
# ==================== ENEMY DRAWING ====================
def draw_enemy_health_bar(enemy):
    if enemy.health < enemy.max_health:
        glPushMatrix()
        glTranslatef(0, 0, enemy.size + 40)
        
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-32, -7, 0)
        glVertex3f(32, -7, 0)
        glVertex3f(32, 7, 0)
        glVertex3f(-32, 7, 0)
        glEnd()
        
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-30, -5, 0)
        glVertex3f(30, -5, 0)
        glVertex3f(30, 5, 0)
        glVertex3f(-30, 5, 0)
        glEnd()
        
        health_ratio = enemy.health / enemy.max_health
        if enemy.type == 0:
            glColor3f(1.0, 0.0, 0.0)
        elif enemy.type == 1:
            glColor3f(1.0, 0.5, 0.0)
        else:
            glColor3f(0.8, 0.0, 0.8)
        
        glBegin(GL_QUADS)
        glVertex3f(-28, -3, 0)
        glVertex3f(-28 + 56 * health_ratio, -3, 0)
        glVertex3f(-28 + 56 * health_ratio, 3, 0)
        glVertex3f(-28, 3, 0)
        glEnd()
        
        glPopMatrix()

def draw_stationary_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    if enemy.damage_timer > 0:
        glColor3f(1.0, 0.5, 0.5)
    else:
        glColor3f(1.0, 0.0, 0.0)
    
    glPushMatrix()
    glScalef(1.2, 0.8, 2.0)
    glutSolidCube(enemy.size)
    glPopMatrix()
    
    glColor3f(0.8, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 90)
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()
    
    glColor3f(1.0, 0.5, 0.5)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 30, 0, 60)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 6, 6, 40, 10, 10)
        glPopMatrix()
    
    glColor3f(0.8, 0.0, 0.0)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, -25)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 2, 60, 10, 10)
        glPopMatrix()
    
    draw_enemy_health_bar(enemy)
    glPopMatrix() # YASIN START FROM HERE

def draw_patrolling_enemy(enemy):   #YASIN here
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    if enemy.damage_timer > 0:
        glColor3f(1.0, 0.8, 0.6)
    else:
        glColor3f(0.8, 0.6, 0.4)
    
    glPushMatrix()
    glScalef(3.0, 3.0, 3.0)
    
    glPushMatrix()
    glScalef(1.2, 0.8, 2.0)
    glutSolidCube(20)
    glPopMatrix()
    
    glColor3f(0.7, 0.5, 0.3)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    gluSphere(gluNewQuadric(), 15, 20, 20)
    glPopMatrix()
    
    glColor3f(0.9, 0.7, 0.5)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, 20)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 10)
        glPopMatrix()
    
    glColor3f(0.6, 0.4, 0.2)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 13, 0, -10)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 3, 40, 10, 10)
        glPopMatrix()
    
    glPopMatrix()
    
    draw_enemy_health_bar(enemy)
    glPopMatrix()

def draw_chasing_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    
    if enemy.damage_timer > 0:
        glColor3f(1.0, 0.5, 1.0)
    else:
        glColor3f(0.8, 0.0, 0.8)
    
    glPushMatrix()
    glScalef(1.8, 1.0, 0.9)
    gluSphere(gluNewQuadric(), enemy.radius * 0.8, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(enemy.radius * 1.4, 0, enemy.radius * 0.3)
    gluSphere(gluNewQuadric(), enemy.radius * 0.6, 15, 15)
    
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(enemy.radius * 0.3, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), enemy.radius * 0.2, 0, enemy.radius * 0.4, 8, 8)
    glPopMatrix()
    glColor3f(0.8, 0.0, 0.8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-enemy.radius * 1.4, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), enemy.radius * 0.5, 0, enemy.radius * 1.8, 10, 10)
    glPopMatrix()
    
    glColor3f(0.6, 0.0, 0.6)
    leg_positions = [
        (0.7, -0.6, -1.0),
        (0.7, 0.6, -1.0),
        (-0.7, -0.6, -1.0),
        (-0.7, 0.6, -1.0)
    ]
    
    for dx, dy, dz in leg_positions:
        glPushMatrix()
        glTranslatef(enemy.radius * dx, enemy.radius * dy, enemy.radius * dz)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), enemy.radius * 0.25, enemy.radius * 0.2, enemy.radius * 1.0, 8, 8)
        glPopMatrix()
    
    draw_enemy_health_bar(enemy)
    glPopMatrix()        

def draw_enemy(enemy):
    if not enemy.alive:
        return
    
    if enemy.type == 0:
        draw_stationary_enemy(enemy)
    elif enemy.type == 1:
        draw_patrolling_enemy(enemy)
    elif enemy.type == 2:
        draw_chasing_enemy(enemy)
###ENEMY SHOOTING STARTS HERE
def update_enemy_shooting():
    global enemy_projectiles
    
    if game_paused or is_dead:
        return
    
    for enemy in enemies:
        if not enemy.alive or enemy.type != 0:
            continue
        
        enemy.shoot_cooldown -= delta_time
        
        if enemy.shoot_cooldown <= 0:
            distance_to_player = distance_2d(enemy.pos, player_pos)
            if distance_to_player < 1500:
                projectile_start = enemy.pos.copy()
                projectile_start[2] = enemy.pos[2] + 90
                
                projectile = EnemyProjectile(projectile_start, player_pos)
                enemy_projectiles.append(projectile)
                
                enemy.shoot_cooldown = enemy.shoot_interval
                
                
def draw_enemy_projectile(projectile):
    if not projectile.alive:
        return
    
    glPushMatrix()
    glTranslatef(projectile.pos[0], projectile.pos[1], projectile.pos[2])
    
    glColor3f(1.0, 0.2, 0.0)
    gluSphere(gluNewQuadric(), projectile.radius, 12, 12)
    
    glColor3f(1.0, 0.6, 0.0)
    gluSphere(gluNewQuadric(), projectile.radius * 0.7, 10, 10)
    
    glColor3f(1.0, 1.0, 0.5)
    gluSphere(gluNewQuadric(), projectile.radius * 0.4, 8, 8)
    
    glPopMatrix()

def update_enemy_projectiles():
    global player_health, is_dead
    
    if game_paused:
        return
    
    for projectile in enemy_projectiles[:]:
        if not projectile.alive:
            enemy_projectiles.remove(projectile)
            continue
        
        projectile.pos[0] += projectile.velocity_x * delta_time
        projectile.pos[1] += projectile.velocity_y * delta_time
        
        projectile.velocity_z -= projectile.gravity * delta_time
        projectile.pos[2] += projectile.velocity_z * delta_time
        
        if projectile.pos[2] <= GROUND_Z:
            projectile.alive = False
            continue
        
        projectile.lifetime += delta_time
        if projectile.lifetime > projectile.max_lifetime:
            projectile.alive = False
            continue
        
        if check_boundary_collision(projectile.pos):
            projectile.alive = False
            continue
        
        if distance_3d(projectile.pos, player_pos) < (projectile.radius + 40):
            player_health -= projectile.damage
            projectile.alive = False
            
            if player_health <= 0:
                is_dead = True
                player_health = 0
            continue

# ==================== GOLDEN KEY DRAWING ====================
def draw_golden_key(key):
    if key.collected:
        return
    
    glPushMatrix()
    glTranslatef(key.pos[0], key.pos[1], key.pos[2] + key.hover_offset)
    
    glRotatef(key.rotation_angle, 0, 0, 1)
    
    glColor3f(1.0, 0.84, 0.0)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 8, 80, 12, 12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 85)
    glutSolidCube(40)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15, 0, -5)
    glutSolidCube(15)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-15, 0, -5)
    glutSolidCube(15)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15, 0, -25)
    glutSolidCube(15)
    glPopMatrix()
    
    glow_size = 1.0 + 0.3 * math.sin(key.glow_pulse)
    glColor3f(1.0, 1.0, 0.5)
    glPushMatrix()
    glScalef(glow_size, glow_size, glow_size)
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 50, 16, 16)
    glPopMatrix()
    
    glPopMatrix()

def update_golden_keys():
    global keys_collected, player_score
    
    if game_paused:
        return
    
    for key in golden_keys:
        if key.collected:
            continue
        
        key.hover_offset = 20 * math.sin(key.hover_speed * time.time())
        key.rotation_angle += 60 * delta_time
        key.rotation_angle = normalize_angle(key.rotation_angle)
        key.glow_pulse += 3 * delta_time
        
        if distance_3d(player_pos, [key.pos[0], key.pos[1], key.pos[2] + key.hover_offset]) < 80:
            key.collected = True
            keys_collected += 1
            player_score += 500

#start from here lapii
# ==================== DIAMOND DRAWING ====================
def draw_diamond(diamond):
    if diamond.collected:
        return
    
    glPushMatrix()
    glTranslatef(diamond.pos[0], diamond.pos[1], diamond.pos[2])
    
    glRotatef(diamond.rotation_angle, 0, 0, 1)
    
    pulse_size = 8.0 * math.sin(diamond.pulse)
    size = diamond.radius + pulse_size
    
    glColor3f(*diamond.color)
    
    glBegin(GL_QUADS)
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
        glVertex3f(0, 0, size)
    
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
        glVertex3f(0, 0, -size)
    glEnd()
    
    glPopMatrix()
#BULLET START FROM HERE 
# ==================== BULLET DRAWING ====================
def draw_bullet(bullet):
    if not bullet.alive:
        return
    
    glPushMatrix()
    glTranslatef(bullet.pos[0], bullet.pos[1], bullet.pos[2])
    
    if bullet.type == 2:
        glColor3f(1.0, 0.3, 0.0)
        gluSphere(gluNewQuadric(), bullet.radius, 16, 16)
        
        glColor3f(1.0, 0.6, 0.0)
        gluSphere(gluNewQuadric(), bullet.radius * 0.7, 12, 12)
        
        glColor3f(1.0, 1.0, 0.5)
        gluSphere(gluNewQuadric(), bullet.radius * 0.4, 10, 10)
        
        glColor3f(1.0, 0.5, 0.0)
        glPushMatrix()
        glRotatef(-bullet.angle, 0, 0, 1)
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), bullet.radius * 0.8, 0, bullet.radius * 2, 8, 8)
        glPopMatrix()
    else:
        glColor3f(*bullet.color)
        gluSphere(gluNewQuadric(), bullet.radius, 10, 10)
    
    glPopMatrix()

#ENVIRONMENT#+++++
# ==================== ENVIRONMENT ====================
def draw_tree(tree):
    glPushMatrix()
    glTranslatef(tree['pos'][0], tree['pos'][1], tree['pos'][2])
    
    glColor3f(*tree['trunk_color'])
    gluCylinder(gluNewQuadric(), tree['trunk_radius'], tree['trunk_radius'] * 0.7, 
                tree['trunk_height'], 12, 12)
    
    glColor3f(*tree['crown_color'])
    glTranslatef(0, 0, tree['trunk_height'])
    
    if tree['type'] == 'pine':
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), tree['crown_radius'], 0, tree['crown_height'], 12, 12)
    elif tree['type'] == 'palm':
        gluSphere(gluNewQuadric(), tree['crown_radius'] * 0.5, 10, 10)
        for i in range(6):
            glPushMatrix()
            glRotatef(i * 60, 0, 0, 1)
            glTranslatef(tree['crown_radius'] * 0.7, 0, 0)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 10, 0, tree['crown_height'] * 0.7, 6, 6)
            glPopMatrix()
    else:
        gluSphere(gluNewQuadric(), tree['crown_radius'], 12, 12)
    
    glPopMatrix()

def draw_rock(rock):
    glPushMatrix()
    glTranslatef(rock['pos'][0], rock['pos'][1], rock['pos'][2])
    glRotatef(rock['rotation'], 0, 1, 0)
    
    glColor3f(*rock['color'])
    
    gluSphere(gluNewQuadric(), rock['size'], 10, 10)
    
    glPushMatrix()
    glTranslatef(rock['size'] * 0.3, rock['size'] * 0.2, rock['size'] * 0.4)
    gluSphere(gluNewQuadric(), rock['size'] * 0.6, 8, 8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-rock['size'] * 0.4, rock['size'] * 0.3, -rock['size'] * 0.3)
    gluSphere(gluNewQuadric(), rock['size'] * 0.5, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_house(house):
    glPushMatrix()
    glTranslatef(house['pos'][0], house['pos'][1], house['pos'][2])
    glRotatef(house['rotation'], 0, 0, 1)
    
    glColor3f(*house['color'])
    glPushMatrix()
    glScalef(house['width'], house['depth'], house['height'])
    glutSolidCube(1)
    glPopMatrix()
    
    glColor3f(*house['roof_color'])
    glPushMatrix()
    glTranslatef(0, 0, house['height'])
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), house['width'] * 0.8, 0, house['height'] * 0.5, 4, 4)
    glPopMatrix()
    
    glColor3f(0.4, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(0, house['depth'] * 0.5 + 1, 0)
    glScalef(0.3, 0.1, 0.5)
    glutSolidCube(house['height'])
    glPopMatrix()
    
    glColor3f(0.9, 0.9, 1.0)
    for i in [-1, 1]:
        for j in [-0.3, 0.3]:
            glPushMatrix()
            glTranslatef(i * house['width'] * 0.3, house['depth'] * 0.5 + 1, j * house['height'] * 0.3)
            glScalef(0.2, 0.1, 0.2)
            glutSolidCube(house['height'])
            glPopMatrix()
    
    glPopMatrix()

#DRAW_GROUND STARTS FROM HERE
def draw_ground():
    glColor3f(0.3, 0.85, 0.4)
    glBegin(GL_QUADS)
    glVertex3f(-BOUNDARY_SIZE, -BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(BOUNDARY_SIZE, -BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(BOUNDARY_SIZE, BOUNDARY_SIZE, GROUND_Z)
    glVertex3f(-BOUNDARY_SIZE, BOUNDARY_SIZE, GROUND_Z)
    glEnd()
    
    glPointSize(4)
    glBegin(GL_POINTS)
    for _ in range(4000):
        x = random.uniform(-BOUNDARY_SIZE, BOUNDARY_SIZE)
        y = random.uniform(-BOUNDARY_SIZE, BOUNDARY_SIZE)
        grass_color = random.choice([
            (0.4, 0.95, 0.3),
            (0.3, 0.9, 0.4),
            (0.35, 0.85, 0.25),
            (0.45, 0.9, 0.35),
            (0.25, 0.8, 0.3),
        ])
        glColor3f(*grass_color)
        glVertex3f(x, y, GROUND_Z + 0.1)
    glEnd()

def draw_boundary_walls():
    """Draw walls that properly connect with sky"""
    wall_height = 800
    wall_thickness = 50
    
    walls = [
        {'pos': [0, BOUNDARY_SIZE, wall_height/2], 'rotation': 0},
        {'pos': [0, -BOUNDARY_SIZE, wall_height/2], 'rotation': 0},
        {'pos': [BOUNDARY_SIZE, 0, wall_height/2], 'rotation': 90},
        {'pos': [-BOUNDARY_SIZE, 0, wall_height/2], 'rotation': 90},
    ]
    
    for wall in walls:
        glPushMatrix()
        glTranslatef(wall['pos'][0], wall['pos'][1], wall['pos'][2])
        glRotatef(wall['rotation'], 0, 0, 1)
        
        glColor3f(0.4, 0.3, 0.2)
        glBegin(GL_QUADS)
        # Front
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        
        # Back
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, -wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        
        # Top
        glVertex3f(-BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(BOUNDARY_SIZE, -wall_thickness/2, wall_height/2)
        glVertex3f(BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        glVertex3f(-BOUNDARY_SIZE, wall_thickness/2, wall_height/2)
        glEnd()
        
        glPopMatrix()




def draw_sky():
    """Draw complete sky background covering entire viewport"""
    sky_distance = BOUNDARY_SIZE * 3
    
    glDisable(GL_DEPTH_TEST)
    
    # Top layer - brightest
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.7, 1.0)
    glVertex3f(-sky_distance, -sky_distance, 3000)
    glVertex3f(sky_distance, -sky_distance, 3000)
    glVertex3f(sky_distance, sky_distance, 3000)
    glVertex3f(-sky_distance, sky_distance, 3000)
    glEnd()
    
    # Upper middle layer
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.8, 1.0)
    glVertex3f(-sky_distance, -sky_distance, 2000)
    glVertex3f(sky_distance, -sky_distance, 2000)
    glColor3f(0.4, 0.7, 1.0)
    glVertex3f(sky_distance, sky_distance, 3000)
    glVertex3f(-sky_distance, sky_distance, 3000)
    glEnd()
    
    # Middle layer
    glBegin(GL_QUADS)
    glColor3f(0.6, 0.85, 1.0)
    glVertex3f(-sky_distance, -sky_distance, 1000)
    glVertex3f(sky_distance, -sky_distance, 1000)
    glColor3f(0.5, 0.8, 1.0)
    glVertex3f(sky_distance, sky_distance, 2000)
    glVertex3f(-sky_distance, sky_distance, 2000)
    glEnd()
    
    # Lower layer - connects to horizon
    glBegin(GL_QUADS)
    glColor3f(0.75, 0.9, 1.0)
    glVertex3f(-sky_distance, -sky_distance, 400)
    glVertex3f(sky_distance, -sky_distance, 400)
    glColor3f(0.6, 0.85, 1.0)
    glVertex3f(sky_distance, sky_distance, 1000)
    glVertex3f(-sky_distance, sky_distance, 1000)
    glEnd()
    
    # Horizon layer - fills gap
    glBegin(GL_QUADS)
    glColor3f(0.85, 0.95, 1.0)
    glVertex3f(-sky_distance, -sky_distance, -100)
    glVertex3f(sky_distance, -sky_distance, -100)
    glColor3f(0.75, 0.9, 1.0)
    glVertex3f(sky_distance, sky_distance, 400)
    glVertex3f(-sky_distance, sky_distance, 400)
    glEnd()
    
    glEnable(GL_DEPTH_TEST)
    
    # Sun
    glPushMatrix()
    glTranslatef(BOUNDARY_SIZE * 0.6, BOUNDARY_SIZE * 0.6, 1800)
    glColor3f(1.0, 0.98, 0.7)
    gluSphere(gluNewQuadric(), 120, 24, 24)
    glPopMatrix()

def create_tree_at(pos, size_factor=1.0):
    tree_height = random.uniform(150, 250) * size_factor
    trunk_height = tree_height * 0.6
    crown_height = tree_height * 0.4
    
    crown_colors = [
        (0.3, 0.9, 0.4),
        (0.2, 0.95, 0.3),
        (0.4, 0.85, 0.3),
        (0.5, 0.9, 0.2),
        (0.3, 0.8, 0.5),
        (0.4, 0.9, 0.3)
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
    house_height = random.uniform(80, 150)
    house_width = random.uniform(60, 100)
    house_depth = random.uniform(60, 100)
    
    house_colors = [
        (0.9, 0.6, 0.5),
        (0.7, 0.8, 0.9),
        (0.8, 0.9, 0.7),
        (0.9, 0.8, 0.6),
        (0.8, 0.7, 0.9),
        (0.6, 0.8, 0.8)
    ]
    
    roof_colors = [
        (0.6, 0.3, 0.2),
        (0.5, 0.2, 0.1),
        (0.3, 0.3, 0.3),
        (0.4, 0.2, 0.1)
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

def create_jungle_environment():
    global trees, rocks, houses
    
    trees.clear()
    rocks.clear()
    houses.clear()
    
    safe_boundary = BOUNDARY_SIZE - 300
    
    trees_per_side = 40
    for i in range(trees_per_side):
        x = -safe_boundary + (i * (2 * safe_boundary) / (trees_per_side - 1))
        y = safe_boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        y = -safe_boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        x = safe_boundary
        y = -safe_boundary + (i * (2 * safe_boundary) / (trees_per_side - 1))
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
        
        x = -safe_boundary
        create_tree_at([x, y, 0], size_factor=random.uniform(1.5, 2.5))
    
    for _ in range(tree_count):
        x = random.randint(-safe_boundary + 100, safe_boundary - 100)
        y = random.randint(-safe_boundary + 100, safe_boundary - 100)
        create_tree_at([x, y, 0], size_factor=random.uniform(0.8, 1.8))
    
    for _ in range(rock_count):
        x = random.randint(-safe_boundary + 100, safe_boundary - 100)
        y = random.randint(-safe_boundary + 100, safe_boundary - 100)
        rock_color = random.choice([
            (0.8, 0.4, 0.2),
            (0.6, 0.3, 0.7),
            (0.3, 0.6, 0.8),
            (0.7, 0.7, 0.3),
            (0.4, 0.8, 0.4),
            (0.9, 0.5, 0.8)
        ])
        rocks.append({
            'pos': [x, y, 0],
            'size': random.uniform(40, 100),
            'color': rock_color,
            'rotation': random.uniform(0, 360)
        })
    
    for _ in range(house_count):
        x = random.randint(-safe_boundary + 200, safe_boundary - 200)
        y = random.randint(-safe_boundary + 200, safe_boundary - 200)
        create_house_at([x, y, 0])


# ==================== UPDATE FUNCTIONS ====================
def update_delta_time():
    global last_frame_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time
    if delta_time > 0.1:
        delta_time = 0.016


def update_dash_mode():    #YASIN
    global dash_timer, dash_mode, dash_cooldown
    
    if dash_timer > 0:
        dash_timer -= delta_time
        if dash_timer <= 0:
            dash_mode = False
            dash_timer = 0
    
    if dash_cooldown > 0:
        dash_cooldown -= delta_time
        if dash_cooldown <= 0:
            dash_cooldown = 0
def update_fire_gun():
    global fire_gun_cooldown, fire_gun_active
    
    if fire_gun_cooldown > 0:
        fire_gun_cooldown -= delta_time
        if fire_gun_cooldown <= 0:
            fire_gun_cooldown = 0
            fire_gun_active = False

def update_player():
    if is_dead or game_paused:
        return
    
    update_dash_mode()
    update_fire_gun()
    
    if check_boundary_collision(player_pos):
        bounce_from_boundary(player_pos)           
           
def update_enemies():
    global enemies_killed_this_level, player_score
    
    if game_paused:
        return
    
    for enemy in enemies[:]:
        if not enemy.alive:
            continue
        
        if enemy.damage_timer > 0:
            enemy.damage_timer -= delta_time
        
        if enemy.type == 1:
            enemy.patrol_angle += enemy.patrol_speed * delta_time
            enemy.patrol_angle = normalize_angle(enemy.patrol_angle)
            
            enemy.pos[0] = enemy.patrol_center[0] + enemy.patrol_radius * math.cos(math.radians(enemy.patrol_angle))
            enemy.pos[1] = enemy.patrol_center[1] + enemy.patrol_radius * math.sin(math.radians(enemy.patrol_angle))
        
        elif enemy.type == 2:
            dx = player_pos[0] - enemy.pos[0]
            dy = player_pos[1] - enemy.pos[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 50:
                enemy.pos[0] += (dx/dist) * enemy.speed * delta_time
                enemy.pos[1] += (dy/dist) * enemy.speed * delta_time
                enemy.angle = math.degrees(math.atan2(dy, dx))
        
        if check_boundary_collision(enemy.pos):
            bounce_from_boundary(enemy.pos)
 
def update_bullets():
    """FIXED: Cannon (type 2) now deals 5 damage - one-shots all enemies!"""
    global player_score, enemies_killed_this_level
    
    if game_paused:
        return
    
    for bullet in bullets[:]:
        if not bullet.alive:
            bullets.remove(bullet)
            continue
        
        move_distance = bullet.speed * delta_time
        bullet.pos[0] += move_distance * (-math.sin(math.radians(bullet.angle)))
        bullet.pos[1] += move_distance * math.cos(math.radians(bullet.angle))
        
        if bullet.type == 2:
            bullet.velocity_z -= bullet.gravity * delta_time
            bullet.pos[2] += bullet.velocity_z * delta_time
            
            if bullet.pos[2] <= GROUND_Z:
                bullet.alive = False
                continue
        
        bullet.distance_traveled += move_distance
        
        if bullet.distance_traveled > bullet.max_distance:
            bullet.alive = False
            continue
        
        if check_boundary_collision(bullet.pos):
            bullet.alive = False
            continue
        
        # FIXED: Use bullet.damage instead of hardcoded 1
        for enemy in enemies:
            if enemy.alive and distance_2d(bullet.pos, enemy.pos) < (bullet.radius + enemy.radius):
                enemy.health -= bullet.damage  # Pistol deals 1, Cannon deals 5
                enemy.damage_timer = enemy.damage_duration
                
                if enemy.health <= 0:
                    enemy.alive = False
                    player_score += enemy.score_value
                    enemies_killed_this_level += 1
                
                bullet.alive = False
                break           


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
    
    
    glutMainLoop()


main()


