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




