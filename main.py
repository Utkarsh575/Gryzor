import os
import pygame

class Game:
    	def __init__(self):
		# Initialize
		size = width, height = 600, 480
		if "-f" in sys.argv[1:]:
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		else:
			self.screen = screen
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True
		self.soldierTimer = SOLDIER_SPAWN_TIMER
		self.reinit()

        def new(self):
                self.reinit()
            self.run()

        def run(self):
            self.playing = True
            while self.playing:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()

        def draw(self):
    		# Draw sprites and background on the screen
		self.screen.fill(GREEN)
		self.grounds.draw(self.screen)
		self.bg_sprite.draw(self.screen)
		self.player_sprite.draw(self.screen)
		self.snipers.draw(self.screen)
		self.soldiers.draw(self.screen)
		self.enemy_bullets.draw(self.screen)
		self.bullets.draw(self.screen)
		self.tanks.draw(self.screen)
		self.bosses.draw(self.screen)
		self.powerups.draw(self.screen)
		pygame.draw.rect(self.screen,SEA_BLUE,(0,437,6767,100))
		self.death_anims.draw(self.screen)
		pygame.display.update()

        def draw_text(self, text, size, x, y):
            font_name = pygame.font.match_font('Times')
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text,True, RED)
            text_rect = text_surface.get_rect()
            text_rect.center = (x,y)
            self.screen.blit(text_surface,text_rect)
            pygame.display.update()

        def show_start_screen(self):


		waiting_for_start = True
		while waiting_for_start:
			self.screen.blit(ss_background,ss_background.get_rect())
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting_for_start = False
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						waiting_for_start = False

# init game
g = Game()


g.show_start_screen()