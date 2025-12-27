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





