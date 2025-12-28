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




