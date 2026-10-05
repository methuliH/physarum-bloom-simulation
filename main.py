import pygame
import numpy as np
import sys
import time
from scipy.ndimage import uniform_filter

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radial Bloom")

clock = pygame.time.Clock()

N = 5000
SPEED = 1.5

x = np.random.uniform(0, WIDTH, N)
y = np.random.uniform(0, HEIGHT, N)
angle = np.random.uniform(0, 2 * np.pi, N)

trail = np.zeros((WIDTH, HEIGHT), dtype=np.float32)
age   = np.zeros((WIDTH, HEIGHT), dtype=np.float32)

DEPOSIT_AMOUNT = 15.0
DECAY = 0.97
AGE_INCREMENT = 6.0
AGE_DECAY = 0.995
AGE_MAX = 100.0

PALETTE = np.array([
    [181,  51,  36],   # youngest 
    [229, 166,  87],   # young-mid 
    [223, 188, 148],   # mid-old 
    [245, 226, 206],   # oldest 
], dtype=np.float32)

SENSOR_DIST = 15.0
SENSOR_ANGLE = 0.5
TURN_SPEED = 0.1

# radial bloom parameters
CENTER_X, CENTER_Y = WIDTH / 2, HEIGHT / 2
RADIAL_STRENGTH = 0.02   # how strongly agents get pulled toward radiating outward

font = pygame.font.SysFont("monospace", 16)

gamma = 1.0
radial_strength = RADIAL_STRENGTH
paused = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gamma = round(gamma + 0.1, 1)
            elif event.key == pygame.K_DOWN:
                gamma = round(gamma - 0.1, 1)
            elif event.key == pygame.K_RIGHT:
                radial_strength = round(radial_strength + 0.005, 3)
            elif event.key == pygame.K_LEFT:
                radial_strength = max(0.0, round(radial_strength - 0.005, 3))
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                x = np.random.uniform(0, WIDTH, N)
                y = np.random.uniform(0, HEIGHT, N)
                angle = np.random.uniform(0, 2 * np.pi, N)
                trail[:] = 0
                age[:] = 0
            elif event.key == pygame.K_s:
                pygame.image.save(screen, f"bloom_{time.strftime('%Y%m%d_%H%M%S')}.png")

    if paused:
        screen.blit(font.render("PAUSED", True, (200, 200, 200)), (10, 30))
        pygame.display.flip()
        clock.tick(60)
        continue

    center_angle = angle
    left_angle = angle + SENSOR_ANGLE
    right_angle = angle - SENSOR_ANGLE

    center_x_s = x + np.cos(center_angle) * SENSOR_DIST
    center_y_s = y + np.sin(center_angle) * SENSOR_DIST

    left_x = x + np.cos(left_angle) * SENSOR_DIST
    left_y = y + np.sin(left_angle) * SENSOR_DIST

    right_x = x + np.cos(right_angle) * SENSOR_DIST
    right_y = y + np.sin(right_angle) * SENSOR_DIST

    center_x_s = np.mod(center_x_s, WIDTH).astype(np.int32)
    center_y_s = np.mod(center_y_s, HEIGHT).astype(np.int32)
    left_x = np.mod(left_x, WIDTH).astype(np.int32)
    left_y = np.mod(left_y, HEIGHT).astype(np.int32)
    right_x = np.mod(right_x, WIDTH).astype(np.int32)
    right_y = np.mod(right_y, HEIGHT).astype(np.int32)

    center_val = trail[center_x_s, center_y_s]
    left_val = trail[left_x, left_y]
    right_val = trail[right_x, right_y]

    turn = np.zeros(N, dtype=np.float32)
    turn_left_mask = (left_val > center_val) & (left_val > right_val)
    turn[turn_left_mask] = -TURN_SPEED
    turn_right_mask = (right_val > center_val) & (right_val > left_val)
    turn[turn_right_mask] = TURN_SPEED

    wiggle = np.random.uniform(-0.1, 0.1, N)

    # compute the angle pointing outward from center through each agent
    dx = x - CENTER_X
    dy = y - CENTER_Y
    outward_angle = np.arctan2(dy, dx)

    # shortest angular difference between current heading and outward angle
    diff = outward_angle - angle
    diff = (diff + np.pi) % (2 * np.pi) - np.pi

    # nudge angle a small fraction of the way toward outward_angle each frame
    radial_bias = diff * radial_strength

    angle = angle + turn + wiggle + radial_bias

    x += np.cos(angle) * SPEED
    y += np.sin(angle) * SPEED
    x = np.mod(x, WIDTH)
    y = np.mod(y, HEIGHT)

    xi = x.astype(np.int32)
    yi = y.astype(np.int32)
    np.add.at(trail, (xi, yi), DEPOSIT_AMOUNT)
    np.add.at(age,   (xi, yi), AGE_INCREMENT)

    trail *= DECAY
    trail = uniform_filter(trail, size=3)
    np.clip(trail, 0, 255, out=trail)

    age *= AGE_DECAY
    age = uniform_filter(age, size=3)
    np.clip(age, 0, AGE_MAX, out=age)

    t = (trail / 255.0) ** gamma

    a = age / AGE_MAX
    seg = np.clip((a * 3).astype(np.int32), 0, 2)
    local_t = (a * 3) - seg
    c0 = PALETTE[seg]
    c1 = PALETTE[np.minimum(seg + 1, 3)]
    hue = c0 + (c1 - c0) * local_t[..., np.newaxis]

    rgb_array = (hue * t[..., np.newaxis]).astype(np.uint8)
    pygame.surfarray.blit_array(screen, rgb_array)

    label = font.render(f"gamma: {gamma:.1f}  radial: {radial_strength:.3f}", True, (200, 200, 200))
    screen.blit(label, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()