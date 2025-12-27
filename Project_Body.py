from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
print("Project_Body module loaded successfully.")
print("yasin thesis ki hbe amader")
print("insahllah")

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
