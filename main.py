# V1.0
# ---CHANGELOG---
# on boundary collision you loop around
# added new sprites and music
#
# ---ISSUES---
# 1. ammo and food can intersect theoretically
# 2. if the screen were to fill up completely with snake blocks the while loops preventing intersection could crash the game
# 3. theres one weird error with the bullet colision logic
# 4. I saw a bullet go through 2 blocks once?
# 5. Game crashed when I pressed space once after a lot of repeated games
#
# ---TODO---
# 1. Reorganize code to work with pygbag (async functions etc)
# 2. Add Health pickups
# 3. Add Sound effects
# 4. Better sprites 
#
# IMPORT MODULES
#import asyncio
import sys
import os
import pygame
import time
import random

# IMPORT CLASSES
from button import Button

# Pyinstaller function
def resource_path(relative_path):
	try:
	# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

# asset urls
wasd_img_url = resource_path('assets/sprites/wasd.png')
spacebar_img_url = resource_path('assets/sprites/spacebar.png')
p_img_url = resource_path('assets/sprites/p.png')
heart_img_url = resource_path('assets/sprites/heart.png')
ammo_img_url = resource_path('assets/sprites/ammo.png')
food_img_url = resource_path('assets/sprites/apple.png')
font_url = resource_path('assets/fonts/SuperMagic.ttf')
happy_beat_url = resource_path('assets/music/Happy_beat.mp3')
ricky_type_beat_url = resource_path('assets/music/ricky_type_beat.mp3')
play_rect_url = resource_path('assets/sprites/Play Rect.png')
options_rect_url = resource_path('assets/sprites/Options Rect.png')
quit_rect_url = resource_path('assets/sprites/Quit Rect.png')


# INITIALIZE VARIABLES

# Pygame
pygame.init()

# Colors
snake_color = (0, 128, 0)
food_color = (250, 112, 112)
ammo_color = (0, 0, 0)
background_color = (90, 133, 172)
white = (255, 255, 255)
black = (0, 0, 0)

# Display from client
infoObject = pygame.display.Info()

dis_width, dis_height = infoObject.current_w, infoObject.current_h

dis = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
pygame.display.set_caption('Super Snake')

# Controls Sprites
wasd_img = pygame.transform.scale(pygame.image.load(wasd_img_url).convert_alpha(), (400, 400))
spacebar_img = pygame.transform.scale(pygame.image.load(spacebar_img_url).convert_alpha(), (400, 400))
p_img = pygame.transform.scale(pygame.image.load(p_img_url).convert_alpha(), (200, 200))

# Show hearts, ammo, food
heart_img = pygame.transform.scale(pygame.image.load(heart_img_url).convert_alpha(), (25, 25))
ammo_img = pygame.transform.scale(pygame.image.load(ammo_img_url).convert_alpha(), (20, 20))
food_img = pygame.transform.scale(pygame.image.load(food_img_url).convert_alpha(), (20, 20))

# Clock object to keep track of time
clock = pygame.time.Clock()

# Player size and speed
snake_block, snake_speed = 20, 3

# Health
health = 3

# Food num to keep on screen
food_stock = 5

# Ammo num to keep on screen
ammo_stock = 5

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Scores
high_score = 0


# DISPLAY FUNCTIONS
# need to update display to show on screen
def get_font(size): # Returns font in the desired size
	return pygame.font.Font(font_url, size)

def display_score(score):
	value = score_font.render("SCORE: " + str(score), True, black)
	dis.blit(value, [0, 0])

def display_ammo_num(ammo):
	value = score_font.render("AMMO: " + str(ammo), True, black)
	dis.blit(value, [150, 0])

def display_high_score(high_score):
	value = score_font.render("HIGH SCORE: " + str(high_score), True, black)
	dis.blit(value, [dis_width - 250, 0])

def display_health(health):
	x = 300
	for i in range(health):
		dis.blit(heart_img, [x, 0])
		x += 25

def display_snake(snake_block, snake_List):
	for x in snake_List:
		pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block], border_radius=1)

def display_message(msg, color, x, y):
	mesg = font_style.render(msg, True, color)
	dis.blit(mesg, [x, y])

def display_explosion(x, y):
	pygame.draw.rect(dis, white, [x, y, snake_block, snake_block], border_radius=10)
	#time.sleep(0.2)

def display_bullet(x, y):
	pygame.draw.rect(dis, food_color, [x, y, snake_block, snake_block], border_radius=10)

def create_bullet(bullet_x, bullet_y, bullet_x_change, bullet_y_change, bullet_List):
	bullet = [bullet_x, bullet_y, bullet_x_change, bullet_y_change, 0]
	bullet_List.append(bullet)

def delete_snake_block(x, y, snake_List):
	if [x, y] in snake_List:
		snake_List.remove([x, y])

# ANIMATION FUNCTIONS       
# will show on screen when called and return
def animate_game_over():
	# Stop music
	pygame.mixer.music.stop()
	for _ in range(5):
		dis.fill(food_color)
		pygame.display.update()
		time.sleep(0.1)
		dis.fill(background_color)
		pygame.display.update()
		time.sleep(0.1)

def animate_damage():
	dis.fill(food_color)
	pygame.display.update()
	time.sleep(0.1)

# GAME STATE FUNCTIONS
# Options Menu
def options_screen():
	while True:
		# get mouse pos
		options_mouse_pos = pygame.mouse.get_pos()
		# fill display
		dis.fill("white")

		# display menu txt
		options_txt = get_font(45).render("This is the OPTIONS screen.", True, "Black")
		options_rect = options_txt.get_rect(center=(dis_width/2, dis_height/10))
		dis.blit(options_txt, options_rect)

		# display back button
		options_back = Button(image=None, pos=(dis_width/2, (dis_height/10)*3), 
							text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
		options_back.changeColor(options_mouse_pos)
		options_back.update(dis)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if options_back.checkForInput(options_mouse_pos):
					start_screen()

		pygame.display.update()


# Start menu state
def start_screen():
	# Load Music
	pygame.mixer.music.load(happy_beat_url)
	pygame.mixer.music.play(loops=-1)
	while True:
		# fill background of display
		dis.fill(background_color)

		# get mouse pos
		menu_mouse_pos = pygame.mouse.get_pos()

		# Display Menu title
		menu_txt = get_font(200).render("SUPER SNAKE", True, "#54bc46")
		menu_rect = menu_txt.get_rect(center=(dis_width/2, dis_height/10))
		dis.blit(menu_txt, menu_rect)

		# Make buttons
		play_button = Button(image=pygame.image.load(play_rect_url), pos=(dis_width/2, (dis_height/10)*4), 
							text_input="PLAY", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
		options_button = Button(image=pygame.image.load(options_rect_url), pos=(dis_width/2, (dis_height/10)*6), 
							text_input="OPTIONS", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
		quit_button = Button(image=pygame.image.load(quit_rect_url), pos=(dis_width/2, (dis_height/10)*8), 
							text_input="QUIT", font=get_font(100), base_color="#d7fcd4", hovering_color="White")

		for button in [play_button, options_button, quit_button]:
			button.changeColor(menu_mouse_pos)
			button.update(dis)

		#display_message("Press C to Start or Q to Quit", white)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					# Load Music
					pygame.mixer.music.stop()
					pygame.mixer.music.load(ricky_type_beat_url)
					# Start Music
					pygame.mixer.music.play(loops=-1)
					gameLoop()
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if play_button.checkForInput(menu_mouse_pos):
					# Load Music
					pygame.mixer.music.stop()
					pygame.mixer.music.load(ricky_type_beat_url)
					# Start Music
					pygame.mixer.music.play(loops=-1)
					#return
					gameLoop()
				if options_button.checkForInput(menu_mouse_pos):
					options_screen()
				if quit_button.checkForInput(menu_mouse_pos):
					pygame.quit()
					sys.exit()

# Main Game State
def gameLoop():
	#start_screen()

	global high_score
	global snake_speed


	x1, y1 = dis_width / 2, dis_height / 2
	x1_change, y1_change = 0, 0

	snake_List = []
	length_of_snake = 1

	# Food
	food_List = []
	for x in range(food_stock):
		r = random.random()
		random.seed(r)
		foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
		foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
		food_List.append([foodx, foody])

	#foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
	#foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

	# Ammo
	ammo_List = []
	for x in range(ammo_stock):
		r = random.random()
		random.seed(r)
		ammox = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
		ammoy = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
		ammo_List.append([ammox, ammoy])
	ammo_num = 0
	#print(ammo_List)

	score = 0
	health = 3

	dis.fill(background_color)
	paused = True   

	bullet_List = []
	bullet = []
	bullet_fired = False
	bullets_triggered = False
	bullet_direction = [0, 0]
	bullet_x = 0
	bullet_y = 0

	explosion_triggered = False

	snake_Head = [0, 0]

	# Pause screen
	while True:
		while paused:
			display_message("PAUSE", white, (dis_width/2)-(dis_width/32), (dis_height/10))
			dis.blit(p_img, ((dis_width/2)-100, (dis_height/10)*2))

			display_message("MOVE", white, (dis_width/5)-(dis_width/42), (dis_height/10))
			dis.blit(wasd_img, ((dis_width/10), (dis_height/10)))

			display_message("FIRE", white, ((dis_width/5)*4)-(dis_width/38), (dis_height/10))
			dis.blit(spacebar_img, (((dis_width/10)*8)-200, (dis_height/10)))

			pause_mouse_pos = pygame.mouse.get_pos()

			# display back button
			pause_back = Button(image=pygame.image.load(quit_rect_url), pos=(dis_width/2, (dis_height/10)*5), 
							text_input="PLAY", font=get_font(100), base_color="Black", hovering_color="Green")
			pause_back.changeColor(pause_mouse_pos)
			pause_back.update(dis)

			# display quit button
			menu_button = Button(image=pygame.image.load(quit_rect_url), pos=(dis_width/2, (dis_height/10)*8), 
							text_input="QUIT GAME", font=get_font(100), base_color="Black", hovering_color="White")
			menu_button.changeColor(pause_mouse_pos)
			menu_button.update(dis)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
					paused = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if pause_back.checkForInput(pause_mouse_pos):
						paused = False
					if menu_button.checkForInput(pause_mouse_pos):
						paused = False
						snake_List = []
						x1, y1 = dis_width / 2, dis_height / 2
						x1_change, y1_change = 0, 0
						length_of_snake = 1
						bullet_fired = False
						score = 0
						ammo_num = 0
						health = 3
						snake_speed = 3
						bullet_List = []
						start_screen()
						
			pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# --TODO-- 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					# should turn bullet into a class later
					#if bullet_fired:
					#	explosion_triggered = True
					#	bullet_fired = False
					#print("bullet_fired: " + str(bullet_fired))
					if ammo_num > 0:
						bullet_fired = True
						bullets_triggered = False
						bullet_x_change, bullet_y_change = x1_change*2, y1_change*2
						#print("snek head: " + str(snake_Head))
						bullet_x = snake_Head[0] + x1_change
						bullet_y = snake_Head[1] + y1_change
						create_bullet(bullet_x, bullet_y, bullet_x_change, bullet_y_change, bullet_List)
						ammo_num -= 1
				# Left				
				if event.key == pygame.K_a and x1_change == 0:
					x1_change = -snake_block
					y1_change = 0
				# Right
				elif event.key == pygame.K_d and x1_change == 0:
					x1_change = snake_block
					y1_change = 0
				# Up
				elif event.key == pygame.K_w and y1_change == 0:
					x1_change = 0
					y1_change = -snake_block
				# Down
				elif event.key == pygame.K_s and y1_change == 0:
					x1_change = 0
					y1_change = snake_block
				elif event.key == pygame.K_p:
					paused = True
				elif event.key == pygame.K_LSHIFT:
					if not bullets_triggered:
						bullets_triggered = True
				

		# Boundary collision
		if (x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0):
			if health == 1:
				snake_List = []
				x1, y1 = dis_width / 2, dis_height / 2
				x1_change, y1_change = 0, 0
				length_of_snake = 1
				bullet_fired = False
				score = 0
				ammo_num = 0
				health = 3
				snake_speed = 3
				bullet_List = []
				animate_game_over()
				start_screen()
			# Don't insta kill player on boundary collision
			elif health > 1:
				animate_damage()
				health -= 1
				
				if x1 >= dis_width:
					x1 = 0
				elif x1 < 0:
					x1 = dis_width
				elif y1 >= dis_height:
					y1 = 0
				elif y1 < 0:
					y1 = dis_height

		x1 += x1_change
		y1 += y1_change

		
		

		dis.fill(background_color)

		for food in food_List:
			#pygame.draw.rect(dis, food_color, [food[0], food[1], snake_block, snake_block], border_radius = 4)
			dis.blit(food_img, [food[0], food[1]])

		for ammo in ammo_List:
			#pygame.draw.rect(dis, ammo_color, [ammo[0], ammo[1], snake_block, snake_block], border_radius = 4)
			dis.blit(ammo_img, [ammo[0], ammo[1]])
		
		# Conditional i added to keep snake list from ballooning with duplicates
		if x1_change or y1_change != 0:
			snake_Head = [x1, y1]
			snake_List.append(snake_Head)
			#print("snake list = " + str(snake_List))
		
		# Keeps snake from trailing blocks
		# if len(snake_List) > length_of_snake:
			#del snake_List[0]

		# THIS NO LONGER BREAKS IT
		# Self collisions
		close_call_explosion = []
		for x in snake_List[:-1]:
			if x == snake_Head and not bullet_fired and health > 1:
				animate_damage()
				health -= 1
			elif x == snake_Head and not bullet_fired and health == 1:
				snake_List = []
				x1, y1 = dis_width / 2, dis_height / 2
				x1_change, y1_change = 0, 0
				length_of_snake = 1
				bullet_fired = False
				score = 0
				ammo_num = 0
				snake_speed = 3
				health = 3
				bullet_List = []
				animate_game_over()
				start_screen()
			elif x == snake_Head and bullet_fired and len(bullet_List) > 0:
				bullet_List.pop()
				close_call_explosion = x
		bullet_fired = False


		# ---BULLET LOGIC ORIGINAL SPOT in case theres a hiding bug somewhere---
		# ---BULLET LOGIC---
		# Reset bullet fired
		#bullet_fired = False
		#just_fired = False
		# make snake able to shoot through its trailing blocks chargeup?
		#print(bullet_List)
		for b in bullet_List:
			already_found_target = []
			# only true on the first 2 loops
			frame = b[4]
			if frame < 3:
				just_fired = True
				b[4] += 1
			else:
				just_fired = False

			blocks_to_delete = []
			b[0] += b[2]
			b[1] += b[3]
				
			display_bullet(b[0], b[1])
			#print("b x change: " + str(bullet_x_change))
			#print("b y change: " + str(bullet_y_change))
			#print("bullet: [" + str(bullet_x) + ", " + str(bullet_y) + "]" )
			#print("list: " + str(snake_List))
			# Boundary collision
			if b[0] >= dis_width or b[0] < 0 or b[1] >= dis_height or b[1] < 0:
				bullet_List.remove(b)
			else:
				# logic to catch collision if bullet is moving too fast
				# by checking one block ahead
				# todo only check around the bullet instead of the entire list of snake blocks
				#---TODO--- improve colision logic so snake can turn and shoot (speed makes bullet skip blocks)
				for x in snake_List:
					# if its the first frame and the bullet lands after a snake block and is going in the x direction
					if (b[2] != 0) and (x[0] == b[0] - snake_block and x[1] == b[1]) and just_fired and [x[0] + snake_block, x[1]] != snake_Head and [x[0], x[1]] != snake_Head:
						if already_found_target != []:
							bullet_prior_x = b[0] - b[2]
							# old target is closer
							if abs(bullet_prior_x - already_found_target[0]) < abs(bullet_prior_x - x[0]):
								blocks_to_delete.append([already_found_target[0], already_found_target[1]])
							else:
								blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
								blocks_to_delete.append([x[0], x[1]])
						else:
							blocks_to_delete.append([x[0], x[1]])
							already_found_target = [x[0], x[1]]

						#print("snake head: " + str(snake_Head))
						print("first frame x - " + "snake x: " + str(x[0]) + " y: " + str(x[1]))
						#print("bullet x: " + str(b[0]) + " bullet y: " + str(b[1]))
						explosion_triggered = True
						#blocks_to_delete.append([x[0], x[1]])
						#already_found_target = [x[0], x[1]]						
					# if its the first frame and the bullet lands after a snake block and is going in the y direction
					elif (b[3] != 0) and (x[0] == b[0] and x[1] == b[1] - snake_block) and just_fired and [x[0], x[1] + snake_block] != snake_Head and [x[0], x[1]] != snake_Head:
						if already_found_target != []:
							bullet_prior_y = b[1] - b[3]
							# old target is closer
							if abs(bullet_prior_y - already_found_target[1]) < abs(bullet_prior_y - x[1]):
								blocks_to_delete.append([already_found_target[0], already_found_target[1]])
							else:
								blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
								blocks_to_delete.append([x[0], x[1]])
						else:
							blocks_to_delete.append([x[0], x[1]])
							already_found_target = [x[0], x[1]]

						#print("snake head: " + str(snake_Head))
						print("first frame y - " + "snake x: " + str(x[0]) + " y: " + str(x[1]))
						#print("bullet x: " + str(b[0]) + " bullet y: " + str(b[1]))
						explosion_triggered = True
						#blocks_to_delete.append([x[0], x[1]])
						#already_found_target = [x[0], x[1]]
					# if the bullet lands on a snake block
					elif (x[0] == b[0] and x[1] == b[1]) and [x[0], x[1]] != snake_Head: #or (x[0] + snake_block == bullet_x and x[1] == bullet_y) or (x[0] + snake_block == bullet_x and x[1] == bullet_y):
						if already_found_target != []:
							# bullet moving in x dir
							if b[2] != 0:
								bullet_prior_x = b[0] - b[2]
								# old target is closer
								if abs(bullet_prior_x - already_found_target[0]) < abs(bullet_prior_x - x[0]):
									blocks_to_delete.append([already_found_target[0], already_found_target[1]])
								# new target is closer
								else:
									blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
									blocks_to_delete.append([x[0], x[1]])
							else:
								bullet_prior_y = b[1] - b[3]
								# old target is closer
								if abs(bullet_prior_y - already_found_target[1]) < abs(bullet_prior_y - x[1]):
									blocks_to_delete.append([already_found_target[0], already_found_target[1]])
								else:
									blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
									blocks_to_delete.append([x[0], x[1]])
						else:
							blocks_to_delete.append([x[0], x[1]])
							already_found_target = [x[0], x[1]]

						#print("snake head: " + str(snake_Head))
						print("on - " + "snake x: " + str(x[0]) + " y: " + str(x[1]))
						#print("bullet x: " + str(b[0]) + " bullet y: " + str(b[1]))
						explosion_triggered = True
						#blocks_to_delete.append([x[0], x[1]])
						#already_found_target = [x[0], x[1]]
						#print("1 del: " + str(block_to_delete))
					# if the bullet lands before a snake block and is going in the x direction
					elif (b[2] != 0) and (x[0] == b[0] + snake_block and x[1] == b[1]) and [x[0] - snake_block, x[1]] != snake_Head and [x[0], x[1]] != snake_Head:
						if already_found_target != []:
							bullet_prior_x = b[0] - b[2]
							# old target is closer
							if abs(bullet_prior_x - already_found_target[0]) < abs(bullet_prior_x - x[0]):
								blocks_to_delete.append([already_found_target[0], already_found_target[1]])
							else:
								# Added to fix weird error: list.remove(x): x not in list -- need to add to other parts of bullet collision logic
								if [already_found_target[0], already_found_target[1]] in blocks_to_delete:
									blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
								blocks_to_delete.append([x[0], x[1]])
						else:
							blocks_to_delete.append([x[0], x[1]])
							already_found_target = [x[0], x[1]]

						#print("snake head: " + str(snake_Head))
						print("before: x - " + "snake x: " + str(x[0]) + " y: " + str(x[1]))
						#print("bullet x: " + str(b[0]) + " bullet y: " + str(b[1]))
						explosion_triggered = True
						#blocks_to_delete.append([x[0], x[1]])
						#already_found_target = [x[0], x[1]]
						#print("2 del: " + str(block_to_delete))
					# if the bullet lands before a snake block and is going in the y direction
					elif (b[3] != 0) and (x[0] == b[0] and x[1] == b[1] + snake_block) and [x[0], x[1] - snake_block] != snake_Head and [x[0], x[1]] != snake_Head:
						if already_found_target != []:
							bullet_prior_y = b[1] - b[3]
							# old target is closer
							if abs(bullet_prior_y - already_found_target[1]) < abs(bullet_prior_y - x[1]):
								blocks_to_delete.append([already_found_target[0], already_found_target[1]])
							else:
								blocks_to_delete.remove([already_found_target[0], already_found_target[1]])
								blocks_to_delete.append([x[0], x[1]])
						else:
							blocks_to_delete.append([x[0], x[1]])
							already_found_target = [x[0], x[1]]

						#print("snake head: " + str(snake_Head))
						print("before: y - " + "snake x: " + str(x[0]) + " y: " + str(x[1]))
						#print("bullet x: " + str(b[0]) + " bullet y: " + str(b[1]))
						explosion_triggered = True
						#blocks_to_delete.append([x[0], x[1]])
						#already_found_target = [x[0], x[1]]
						#print("3 del: " + str(block_to_delete))

					# if the bullet has been triggered to explode
					elif bullets_triggered:
						# block on left of bullet
						if x[0] + snake_block == b[0] and x[1] == b[1]:
							explosion_triggered = True
							blocks_to_delete.append([x[0], x[1]])
						# block on right of bullet
						if x[0] - snake_block == b[0] and x[1] == b[1]:
							explosion_triggered = True
							blocks_to_delete.append([x[0], x[1]])
						# above bullet
						if x[0] == b[0] and x[1] + snake_block == b[1]:
							explosion_triggered = True
							blocks_to_delete.append([x[0], x[1]])
						# below bullet
						if x[0] == b[0] and x[1] - snake_block == b[1]:
							explosion_triggered = True
							blocks_to_delete.append([x[0], x[1]])
				
				bullets_triggered = False

			if explosion_triggered:
				display_explosion(b[0], b[1])
				bullet_List.remove(b)

				# list of blocks to loop through to delete
				for block in blocks_to_delete:
					delete_snake_block(block[0], block[1], snake_List)
				explosion_triggered = False
				#bullets_triggered = False

		display_snake(snake_block, snake_List)
		if close_call_explosion != []:
			display_explosion(close_call_explosion[0], close_call_explosion[1])

		display_score(score)
		display_high_score(high_score)
		display_ammo_num(ammo_num)
		display_health(health)

		pygame.display.update()
		

		for f in food_List:
			if x1 == f[0] and y1 == f[1]:
				food_List.remove(f)
				intersecting_snake = True
				while intersecting_snake:
					foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
					foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
					if [foodx, foody] not in snake_List:
						food_List.append([foodx, foody])
						intersecting_snake = False
				#length_of_snake +=1
				score += 10
				# max out snake speed at 8
				if (snake_speed <= 10) and (score % 20 == 0):
					snake_speed += 1
				
				if score > high_score:
					high_score = score

		for a in ammo_List:
			if x1 == a[0] and y1 == a[1]:
				ammo_num += 4
				ammo_List.remove(a)
				intersecting_snake = True
				while intersecting_snake:
					ammox = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
					ammoy = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
					if [ammox, ammoy] not in snake_List:
						ammo_List.append([ammox, ammoy])
						intersecting_snake = False

		clock.tick(snake_speed)

start_screen()
#gameLoop()

