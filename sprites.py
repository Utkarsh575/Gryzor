import pygame
from camera import *
from settings import *
from graphics import *
vec = pygame.math.Vector2


all_sprites = pygame.sprite.Group()

# Player States
RIGHT = 0
LEFT = 1
RIGHT_DOWN = 2
RIGHT_UP = 3
LEFT_UP = 4
LEFT_DOWN = 5

class Player(pygame.sprite.Sprite):
	def __init__(self,game):


		pygame.sprite.Sprite.__init__(self)

		# Copy of Game
		self.game = game

		self.image = pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
		self.image.set_colorkey(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.center = (PLAYER_POSX,0)
		self.health = PLAYER_HEALTH

		# Movement
		self.state = RIGHT
		self.up = False
		self.down = False
		self.pos = vec(30,30)
		self.vel = vec(0,0)
		self.acc = vec(0,GRAVITY)
		self.canMove = True
		self.jumping = True
		self.facing = 1

		# Jumping
		self.canJump = False
		self.collisions = True

		# Blinking
		self.blinkTime = BLINK_TIME
		self.canBlink = 1
		self.blinking = False
		self.blinkRetract = BLINK_RETRACT


		self.dead = False
		# Animation
		# Frames hold each frame
		# index determines the current frame to be played
		self.animCounter = ANIM_SPEED

		self.jumpFrames = [PLAYER_JUMP_0,PLAYER_JUMP_1,PLAYER_JUMP_2,PLAYER_JUMP_3]
		self.jumpIndex = 0

		self.rightFrames = [PLAYER_RIGHT_0,PLAYER_RIGHT_1,PLAYER_RIGHT_2,PLAYER_RIGHT_3,PLAYER_RIGHT_4,PLAYER_RIGHT_5]
		self.rightIndex = 0

		self.rightUpFrames = [PLAYER_RIGHT_UP_0,PLAYER_RIGHT_UP_1,PLAYER_RIGHT_UP_2]
		self.rightUpIndex = 0

		self.rightDownFrames =  [PLAYER_RIGHT_DOWN_0,PLAYER_RIGHT_DOWN_1,PLAYER_RIGHT_DOWN_2]
		self.rightDownIndex = 0

		self.deadFrames = [PLAYER_DEAD_0,PLAYER_DEAD_1,PLAYER_DEAD_2,PLAYER_DEAD_3,PLAYER_DEAD_4]
		self.deadIndex = 0

	def update(self):
		self.calcState()
		if self.dead:
			self.kill()
			return
		if self.jumping:
			self.jumpIndex = self.animate(self.jumpFrames,self.jumpIndex,int(PLAYER_HEIGHT/2),PLAYER_WIDTH)

		else:
			self.setImageByState()
			if self.isMoving():
				# Set the animation depending on the state
				if self.state == RIGHT:
					self.rightIndex = self.animate(self.rightFrames,self.rightIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == RIGHT_DOWN:
					self.rightDownIndex = self.animate(self.rightDownFrames,self.rightDownIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == RIGHT_UP:
					self.rightUpIndex = self.animate(self.rightUpFrames,self.rightUpIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == LEFT:
					self.rightIndex = self.animate(self.rightFrames,self.rightIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
				elif self.state == LEFT_DOWN:
					self.rightDownIndex = self.animate(self.rightDownFrames,self.rightDownIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
				elif self.state == LEFT_UP:
					self.rightUpIndex = self.animate(self.rightUpFrames,self.rightUpIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
			else:
				# Else a stationary image
				if self.state == RIGHT:
					self.image = pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == RIGHT_DOWN:
					self.image = pygame.transform.scale(PLAYER_RIGHT_DOWN_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == RIGHT_UP:
					self.image = pygame.transform.scale(PLAYER_RIGHT_UP_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == LEFT:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)
				elif self.state == LEFT_DOWN:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_DOWN_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)
				elif self.state == LEFT_UP:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_UP_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)

		# Blinking and Motion are Disjoint. All others can occur simultaneously
		if self.blinking:
			self.acc = vec(0,0)
			self.vel.y = 0
			self.vel.x = self.facing * BLINK_SPEED
			self.blinkTime -= 1
			self.blinkRetract -= 1
			if self.blinkTime == 0:
				self.blinking = False
				self.blinkTime = BLINK_TIME
				self.blinkRetract = BLINK_RETRACT
		else:
			self.acc = vec(0,GRAVITY)
			if self.blinkRetract == 0 :
				pass
			else:
				self.blinkRetract -= 1
		keystate = pygame.key.get_pressed()
		mousestate = pygame.mouse.get_pressed()
		if keystate[pygame.K_a]:
			self.acc.x = -PLAYER_ACC
			self.facing = -1
		if keystate[pygame.K_d]:
			self.acc.x = PLAYER_ACC
			self.facing = 1
		if keystate[pygame.K_x]:
			self.acc = vec(0,GRAVITY)
			self.vel = vec(0,0)
		if keystate[pygame.K_s]:
			self.drop()
		if mousestate[2]:   # RMB
			if self.canBlink:
				self.blink()
		if not self.pos.x < -LEFT_BOUND and not self.pos.x > -RIGHT_BOUND:
			self.acc.x += self.vel.x * PLAYER_FRC
			self.vel += self.acc
			self.pos += self.vel + 0.5*self.acc
		else:
			if self.pos.x <= -LEFT_BOUND:
				self.pos.x += 1
			else:
				self.pos.x -= 1
		self.rect.bottom = self.pos.y
		self.image.set_colorkey(YELLOW)