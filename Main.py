import pygame
import sys
import os
import random
import time
from moviepy.editor import VideoFileClip

# --- INIT ---
pygame.init()
pygame.mixer.init()

# Display
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Eco Runner - Collect Plastic Bags!")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SPRITES_DIR = os.path.join(BASE_DIR, 'sprites')

# --- LOAD ASSETS ---
def load_image(path, size=None):
    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_sound(path):
    return pygame.mixer.Sound(path)

# Menu images
game_logo_image = load_image(os.path.join(IMAGES_DIR, 'game_logo.png'), (300, 280))
bg_image = load_image(os.path.join(IMAGES_DIR, 'City1.png'), (900, 700))
play_button_image = load_image(os.path.join(IMAGES_DIR, 'play.png'), (150, 90))
settings_button_image = load_image(os.path.join(IMAGES_DIR, 'settings.png'), (150, 90))
store_button_image = load_image(os.path.join(IMAGES_DIR, 'leader.png'), (150, 90))
help_button_image = load_image(os.path.join(IMAGES_DIR, 'about.png'), (150, 90))
screen2bg_image = load_image(os.path.join(IMAGES_DIR, 'screen2bg.jpg'), (900, 600))
previous_button_image = load_image(os.path.join(IMAGES_DIR, 'prew.png'), (150, 90))
music_button_image = load_image(os.path.join(IMAGES_DIR, 'sound.png'), (140, 90))
music_off_button_image = load_image(os.path.join(IMAGES_DIR, 'sound_off.png'), (140, 90))
instruction_screen_image = load_image(os.path.join(IMAGES_DIR, 'instruction_screen.jpg'), (900, 600))
setting_screen_image = load_image(os.path.join(IMAGES_DIR, 'setting_screen.jpg'), (900, 600))
story_bg_image = load_image(os.path.join(IMAGES_DIR, 'storybg1.jpg'), (900, 600))
story_bg_image2 = load_image(os.path.join(IMAGES_DIR, 'storybg2.jpg'), (900, 600))
story_bg_image3 = load_image(os.path.join(IMAGES_DIR, 'storybg3.jpg'), (900, 600))
next_button_image = load_image(os.path.join(IMAGES_DIR, 'next.png'), (150, 90))

# Character images for story slides


# Menu fonts
font = pygame.font.Font(os.path.join(FONTS_DIR, 'CreamySugarfont.ttf'), 30)
font1 = pygame.font.Font(os.path.join(FONTS_DIR, 'ShadowRamblefont.otf'), 40)

# Menu sounds
pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'bg.mp3'))
button_click_sound = load_sound(os.path.join(SOUNDS_DIR, 'button.mp3'))
typing_sound = load_sound(os.path.join(SOUNDS_DIR, 'typing.wav'))

music_on = True

# --- MENU STATE VARIABLES ---
screen_state = "main_menu"
active_input = None
username_input = ""
age_input = ""
submit_button = pygame.Rect(370, 300, 150, 50)
previous_button = pygame.Rect(0, 0, 0, 0)
typing_active = False
story_index = 0
story_char_index = 0
story_timer = pygame.time.get_ticks()

def draw_button(image, x, y):
    button_rect = image.get_rect(center=(x, y))
    screen.blit(image, button_rect)
    return button_rect

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

def main_menu():
    global screen_state
    screen.fill(BLACK)
    screen.blit(bg_image, (0, 0))
    current_music_button = music_button_image if music_on else music_off_button_image
    play_button = draw_button(play_button_image, width // 2, 550)
    settings_button = draw_button(settings_button_image, width // 1.1, 50)
    store_button = draw_button(store_button_image, width // 1.45, 550)
    help_button = draw_button(help_button_image, width // 3.2, 550)
    draw_button(game_logo_image, width // 2, 100)
    music_button = draw_button(current_music_button, width // 8, 550)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_click_sound.play()
            if play_button.collidepoint(event.pos):
                screen_state = "login_screen"
                return
            if settings_button.collidepoint(event.pos):
                screen_state = "settings_screen"
                return
            if store_button.collidepoint(event.pos):
                print("Store Button Clicked")
            if help_button.collidepoint(event.pos):
                screen_state = "help_screen"
                return
            if music_button.collidepoint(event.pos):
                toggle_music()
    pygame.display.flip()

def login_screen():
    global active_input, username_input, age_input, screen_state, previous_button
    screen.blit(setting_screen_image, (0, 0))
    draw_text("Enter Username and Age", font1, WHITE, 350, 90)
    pygame.draw.rect(screen, WHITE, (350, 150, 300, 40), 2)
    draw_text("Username:", font, WHITE, 190, 155)
    username_surface = font.render(username_input, True, WHITE)
    screen.blit(username_surface, (360, 155))
    pygame.draw.rect(screen, WHITE, (350, 220, 300, 40), 2)
    draw_text("Age:", font, WHITE, 240, 225)
    age_surface = font.render(age_input, True, WHITE)
    screen.blit(age_surface, (360, 225))
    pygame.draw.rect(screen, (150, 200, 250), submit_button)
    draw_text("Submit", font, WHITE, 400, 310)
    previous_button = draw_button(previous_button_image, width // 10, 50)
    pygame.display.flip()

def story_screen():
    global story_index, story_timer, screen_state, story_char_index
    story_characters = [
    pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "jake.png")).convert_alpha(), (150, 200)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "mia.png")).convert_alpha(), (150, 200)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR, "max.png")).convert_alpha(), (150, 200))
    ]
    slides = [
        {"background": story_bg_image, "heading": "Concrete Jungle Crisis",
         "text": "In the heart of a noisy city, trash piled up\n on the sidewalks, overflowing bins spilled\n into the streets. Jack, a smart kid, noticed\n the mess blocking drains \nand making his home unlivable.\n"},
        {"background": story_bg_image2, "heading": "Sands of Waste",
         "text": "Waves crashed on the shore, carrying\n plastic bottles and wrappers onto the sand.\n Mia, who loved building sandcastles,\n found more trash than seashells."},
        {"background": story_bg_image3, "heading": "Green Gone Gray",
         "text": "The once-green park was covered in\n cans, bags, and food waste.\n Max, who loved to play under the trees,\n saw animals struggling to find clean space."}
    ]
    if story_index >= len(slides):
        screen_state = "game_play"
        return
    slide = slides[story_index]
    screen.blit(slide["background"], (0, 0))
    draw_text(slide["heading"], font1, WHITE, 80, 80)
    screen.blit(story_characters[story_index], (700, 100))
    # Typing effect
    if pygame.time.get_ticks() - story_timer > 50 and story_char_index < len(slide["text"]):
        globals()["story_char_index"] += 1
        story_timer = pygame.time.get_ticks()
        if not typing_sound.get_num_channels():
            typing_sound.play(-1)
    elif story_char_index >= len(slide["text"]):
        typing_sound.stop()
    wrapped_text = []
    line = ""
    for word in slide["text"][:story_char_index].split('\n'):
        test_line = line + word + " "
        if font.size(test_line)[0] < 700:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word + " "
    wrapped_text.append(line)
    y = 150
    for line in wrapped_text:
        draw_text(line.strip(), font, WHITE, 50, y)
        y += 40
    
    next_button = draw_button(next_button_image, width - 80, height - 50)
    back_button = draw_button(previous_button_image, width // 10, 560)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button.collidepoint(event.pos):
                button_click_sound.play()
                typing_sound.stop()
                if story_index < len(slides) - 1:
                    story_index += 1
                    story_char_index = 0
                else:
                    screen_state = "game_play"
                    story_index = 0
                    story_char_index = 0
            if back_button.collidepoint(event.pos):
                button_click_sound.play()
                typing_sound.stop()
                if story_index > 0:
                    story_index -= 1
                else:
                    screen_state = "main_menu"
                story_char_index = 0
    pygame.display.flip()

def help_screen():
    global screen_state
    screen.fill(BLACK)
    screen.blit(instruction_screen_image, (0, 0))
    draw_text("INSTRUCTIONS :)", font1, WHITE, 350, 50)
    draw_text("1. Click Play Button to start the game.", font, WHITE, 100, 150)
    draw_text("2. Settings lets you change sound and controls.", font, WHITE, 100, 200)
    draw_text("3. Enter your name and age to proceed.", font, WHITE, 100, 250)
    draw_text("4. Game has 2 Levels (2 different themes, and characters!!!!).", font, WHITE, 100, 300)
    draw_text("5. Unlock each theme by scoring the required points", font, WHITE, 100, 350)
    draw_text("6. Collect trash and run by avoiding obstacles.", font, WHITE, 100, 400)
    back_button = draw_button(previous_button_image, width // 10, 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                button_click_sound.play()
                screen_state = "main_menu"
    pygame.display.flip()

def settings_screen():
    global screen_state, music_on
    screen.fill(BLACK)
    screen.blit(screen2bg_image, (0, 0))
    draw_text("Settings", font1, WHITE, 400, 50)
    draw_text("Sound: ON" if music_on else "Sound: OFF", font, WHITE, 100, 150)
    current_music_button = music_button_image if music_on else music_off_button_image
    music_toggle_button = draw_button(current_music_button, 150, 250)
    back_button = draw_button(previous_button_image, width // 10, 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                button_click_sound.play()
                screen_state = "main_menu"
            if music_toggle_button.collidepoint(event.pos):
                button_click_sound.play()
                toggle_music()
    pygame.display.flip()

# --- RUNNER GAMEPLAY (with two levels) ---
def game_play():
    def run_level(
        video_filename,
        walk_frame_names,
        bag_goal,
        next_level_callback=None
    ):
        clip = VideoFileClip(os.path.join(BASE_DIR, video_filename))
        runner_screen = pygame.display.set_mode(clip.size)
        pygame.display.set_caption("Eco Runner - Collect Plastic Bags!")
        runner_clock = pygame.time.Clock()
        sprites_path = SPRITES_DIR
        plastic_image_path = os.path.join(sprites_path, "plastic.png")
        jump_sound_path = os.path.join(sprites_path, "jump.wav")
        obstacle_image_path = os.path.join(sprites_path, "obstacle.png")
        # Heart images
        heart_images = [
            pygame.transform.scale(pygame.image.load(os.path.join(sprites_path, "heart1.png")).convert_alpha(), (100, 30)),
            pygame.transform.scale(pygame.image.load(os.path.join(sprites_path, "heart2.png")).convert_alpha(), (100, 30)),
            pygame.transform.scale(pygame.image.load(os.path.join(sprites_path, "heart3.png")).convert_alpha(), (80, 40))
        ]
        def load_image_with_transparency(path):
            return pygame.image.load(path).convert_alpha()
        plastic_bag_image = pygame.transform.scale(load_image_with_transparency(plastic_image_path), (50, 50))
        obstacle_base_image = load_image_with_transparency(obstacle_image_path)
        def load_animation_frames(base_path, frame_names, size):
            return [
                pygame.transform.scale(load_image_with_transparency(os.path.join(base_path, name)), size)
                for name in frame_names
            ]
        character_size = (50, 100)
        walk_frames = load_animation_frames(sprites_path, walk_frame_names, character_size)
        lane_positions = {
            "left": 200,
            "center": clip.size[0] // 2 - 40,
            "right": clip.size[0] - 200
        }
        char_x = lane_positions["center"]
        char_y = clip.size[1] - 150
        gravity = 1
        jump_power = -15
        char_y_velocity = 0
        on_ground = True
        current_lane = "center"
        animation_index = 0
        animation_timer = 0
        animation_speed = 100
        score = 0
        start_time = pygame.time.get_ticks()
        lives_lost = 0
        if not os.path.exists(jump_sound_path):
            print("Missing jump.wav")
            sys.exit()
        jump_sound = pygame.mixer.Sound(jump_sound_path)
        def spawn_plastic_bag():
            lane = random.choice(["left", "center", "right"])
            rect = plastic_bag_image.get_rect()
            rect.x = lane_positions[lane]
            rect.y = clip.size[1] - 150 - random.randint(30, 100)
            return rect
        def spawn_obstacle():
            lane = random.choice(["left", "center", "right"])
            return {
                "lane": lane,
                "spawn_time": time.time(),
                "scale": 0.2
            }
        plastic_bags = [spawn_plastic_bag() for _ in range(5)]
        current_obstacle = None
        obstacle_spawn_interval = 2.0
        running = True
        collision_time = None
        last_obstacle_spawn_time = time.time()
        game_over_time = None
        while running:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
            if elapsed_time > clip.duration:
                start_time = pygame.time.get_ticks()
                elapsed_time = 0
            try:
                frame = clip.get_frame(elapsed_time)
                runner_screen.blit(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (0, 0))
            except Exception as e:
                print(f"Video error: {e}")
            if not current_obstacle and time.time() - last_obstacle_spawn_time > obstacle_spawn_interval:
                current_obstacle = spawn_obstacle()
                last_obstacle_spawn_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and not collision_time:
                    if event.key == pygame.K_LEFT:
                        if current_lane == "center":
                            current_lane = "left"
                        elif current_lane == "right":
                            current_lane = "center"
                    elif event.key == pygame.K_RIGHT:
                        if current_lane == "center":
                            current_lane = "right"
                        elif current_lane == "left":
                            current_lane = "center"
                    elif event.key == pygame.K_UP and on_ground:
                        char_y_velocity = jump_power
                        on_ground = False
                        jump_sound.play()
            char_x = lane_positions[current_lane]
            char_y_velocity += gravity
            char_y += char_y_velocity
            if char_y >= clip.size[1] - 150:
                char_y = clip.size[1] - 150
                char_y_velocity = 0
                on_ground = True
            animation_timer += runner_clock.get_time()
            if animation_timer >= animation_speed:
                animation_index = (animation_index + 1) % len(walk_frames)
                animation_timer = 0
            character_rect = pygame.Rect(char_x, char_y, character_size[0], character_size[1])
            for bag in plastic_bags[:]:
                if character_rect.colliderect(bag):
                    score += 1
                    plastic_bags.remove(bag)
            while len(plastic_bags) < 5:
                plastic_bags.append(spawn_plastic_bag())
            if current_obstacle:
                time_since_spawn = time.time() - current_obstacle["spawn_time"]
                growth_duration = 0.7
                if time_since_spawn < growth_duration:
                    scale = 0.2 + (time_since_spawn / growth_duration) * 0.8
                else:
                    scale = 1.0
                current_obstacle["scale"] = scale
                size = int(50 * scale), int(50 * scale)
                obstacle_scaled = pygame.transform.scale(obstacle_base_image, size)
                obs_x = lane_positions[current_obstacle["lane"]] + 25 - size[0] // 2
                obs_y = clip.size[1] - 150 + 25 - size[1] // 2
                runner_screen.blit(obstacle_scaled, (obs_x, obs_y))
                if scale >= 1.0 and character_rect.colliderect(pygame.Rect(obs_x, obs_y, *size)) and on_ground and not collision_time:
                    lives_lost += 1
                    collision_time = time.time()
                    current_obstacle = None
            if collision_time:
                if time.time() - collision_time < 1.0:
                    runner_screen.blit(walk_frames[animation_index], (char_x, char_y))
                    font_big = pygame.font.Font(None, 74)
                    runner_screen.blit(font_big.render("Ouch!", True, (255, 0, 0)), (clip.size[0] // 2 - 80, clip.size[1] // 3))
                else:
                    collision_time = None
                    if lives_lost >= 3:
                        font_big = pygame.font.Font(None, 74)
                        runner_screen.blit(font_big.render("Game Over", True, (255, 0, 0)), (clip.size[0] // 3, clip.size[1] // 3))
                        pygame.display.update()
                        if not game_over_time:
                            game_over_time = time.time()
                        elif time.time() - game_over_time > 0.2:
                            if next_level_callback:
                                next_level_callback()
                            else:
                                pygame.display.set_mode((width, height))
                            return
                        continue
            else:
                for bag in plastic_bags:
                    runner_screen.blit(plastic_bag_image, bag)
                runner_screen.blit(walk_frames[animation_index], (char_x, char_y))
                font_small = pygame.font.Font(None, 36)
                runner_screen.blit(font_small.render(f"Plastic Bags Collected: {score}", True, (255, 255, 255)), (20, 20))
            # Draw heart image based on lives lost
            if lives_lost < 3:
                runner_screen.blit(heart_images[lives_lost], (clip.size[0] - 120, 10))
            pygame.display.update()
            runner_clock.tick(30)
            # --- LEVEL UP ---
            if score >= 8 and next_level_callback:
                next_level_callback()
                return
            if bag_goal > 8 and score >= bag_goal and next_level_callback is None:
                # For level 2, if you want to end after 15 bags, uncomment below:
                # pygame.display.set_mode((width, height))
                # return
                pass
        pygame.display.set_mode((width, height))

    # --- Level 2 callback ---
    def start_level2():
        run_level(
            video_filename="cv2_level2.mp4",
            walk_frame_names=[f"2walk{i}.png" for i in range(1, 7)],
            bag_goal=15,
            next_level_callback=None
        )

    # --- Start Level 1 ---
    run_level(
        video_filename="cv2.mp4",
        walk_frame_names=["walk1.png", "walk2.png", "walk3.png", "walk4.png"],
        bag_goal=8,
        next_level_callback=start_level2
    )

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if screen_state == "login_screen":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(350, 150, 300, 40).collidepoint(event.pos):
                    active_input = "username"
                elif pygame.Rect(350, 220, 300, 40).collidepoint(event.pos):
                    active_input = "age"
                elif submit_button.collidepoint(event.pos):
                    print("Username:", username_input)
                    print("Age:", age_input)
                    screen_state = "story_screen"
                    story_timer = pygame.time.get_ticks()
                    story_index = 0
                    typing_sound.play(-1)
                elif previous_button.collidepoint(event.pos):
                    button_click_sound.play()
                    screen_state = "main_menu"
                else:
                    active_input = None
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    elif len(username_input) < 20:
                        username_input += event.unicode
                elif active_input == "age":
                    if event.key == pygame.K_BACKSPACE:
                        age_input = age_input[:-1]
                    elif event.unicode.isdigit() and len(age_input) < 3:
                        age_input += event.unicode
    if screen_state == "main_menu":
        main_menu()
    elif screen_state == "login_screen":
        login_screen()
    elif screen_state == "game_play":
        game_play()
        screen_state = "main_menu"  # Return to menu after game
    elif screen_state == "help_screen":
        help_screen()
    elif screen_state == "settings_screen":
        settings_screen()
    elif screen_state == "story_screen":
        story_screen()
    pygame.display.flip()
