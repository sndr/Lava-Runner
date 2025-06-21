import pygame
import random
import sys
import os
from game.player import Player
from game.platform import Platform
from game.background import Background
from game.initial_platform import InitialPlatform

class Game:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer
        self.window = pygame.display.set_mode((800, 400))  # WIN_WIDTH, WIN_HEIGHT
        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 40)
        self.entities: list = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.start_time = 0
        self.game_over = False
        self.last_platform_x = 800
        self.last_platform_y = 300
        self.selected_option = 0
        self.game_over_selected_option = 0
        self.initial_platform_active = True
        self.initial_platform_disappear_time = None
        # Load audio files
        try:
            self.menu_music = pygame.mixer.Sound("assets/menu_music.mp3")
        except FileNotFoundError:
            print("Warning: assets/menu_music.wav not found")
            self.menu_music = None
        try:
            self.game_music = pygame.mixer.Sound("assets/game_music.mp3")
        except FileNotFoundError:
            print("Warning: assets/game_music.wav not found")
            self.game_music = None
        try:
            self.jump_sound = pygame.mixer.Sound("assets/jump_music.mp3")
        except FileNotFoundError:
            print("Warning: assets/jump_sound.wav not found")
            self.jump_sound = None

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self, score):
        with open("high_score.txt", "w") as f:
            f.write(str(score))

    def draw_text_with_shadow(self, text: str, font, color: tuple, pos: tuple, shadow_offset: int = 2):
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=pos)
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.window.blit(shadow_surf, shadow_rect)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        self.window.blit(text_surf, text_rect)

    def show_menu(self):
        try:
            menu_bg = pygame.image.load("assets/menu_background.jpg").convert()
            menu_bg = pygame.transform.scale(menu_bg, (800, 400))
        except FileNotFoundError:
            menu_bg = pygame.Surface((800, 400))
            menu_bg.fill((0, 0, 50))

        # Play menu music
        if self.menu_music:
            self.menu_music.play(loops=-1)

        options = ["Start", "Score", "Exit"]

        while True:
            self.window.blit(menu_bg, (0, 0))
            self.draw_text_with_shadow("Lava Runner", self.title_font, (255, 255, 255), (400, 100))
            for i, option in enumerate(options):
                color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
                self.draw_text_with_shadow(option, self.option_font, color, (400, 200 + i * 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.menu_music:
                        self.menu_music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(options)
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(options)
                    if event.key == pygame.K_RETURN:
                        if self.menu_music:
                            self.menu_music.stop()
                        if self.selected_option == 0:
                            return True
                        elif self.selected_option == 1:
                            self.show_score_screen(menu_bg)
                        elif self.selected_option == 2:
                            pygame.quit()
                            sys.exit()

    def show_score_screen(self, menu_bg):
        # Play menu music
        if self.menu_music:
            self.menu_music.play(loops=-1)

        while True:
            self.window.blit(menu_bg, (0, 0))
            self.draw_text_with_shadow("High Score", self.title_font, (255, 255, 255), (400, 150))
            self.draw_text_with_shadow(f"Score: {self.high_score}", self.option_font, (255, 255, 255), (400, 200))
            self.draw_text_with_shadow("Back (B)", self.option_font, (255, 255, 255), (400, 250))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.menu_music:
                        self.menu_music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if self.menu_music:
                            self.menu_music.stop()
                        return

    def show_game_over(self):
        options = ["Restart", "Quit"]

        while True:
            self.window.fill((0, 0, 0))
            self.draw_text_with_shadow("Game Over!", self.title_font, (255, 0, 0), (400, 100))
            self.draw_text_with_shadow(f"Score: {self.score}", self.option_font, (255, 255, 255), (400, 150))
            self.draw_text_with_shadow(f"High Score: {self.high_score}", self.option_font, (255, 255, 255), (400, 200))
            for i, option in enumerate(options):
                color = (255, 255, 0) if i == self.game_over_selected_option else (255, 255, 255)
                self.draw_text_with_shadow(option, self.option_font, color, (400, 250 + i * 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game_over_selected_option = (self.game_over_selected_option - 1) % len(options)
                    if event.key == pygame.K_DOWN:
                        self.game_over_selected_option = (self.game_over_selected_option + 1) % len(options)
                    if event.key == pygame.K_RETURN:
                        if self.game_over_selected_option == 0:
                            return Game().run()
                        elif self.game_over_selected_option == 1:
                            pygame.quit()
                            sys.exit()

    def run(self):
        if not self.show_menu():
            return

        self.entities = []
        bg1 = Background(0)
        bg2 = Background(800)
        self.entities.extend([bg1, bg2])
        self.player = Player(400)  # Ajustado para cima do chão inicial
        self.entities.append(self.player)
        initial_platform = InitialPlatform()
        self.entities.append(initial_platform)
        self.initial_platform_active = True
        self.initial_platform_disappear_time = pygame.time.get_ticks() + 2000
        self.start_time = pygame.time.get_ticks()

        # Play game music
        if self.game_music:
            self.game_music.play(loops=-1)

        # Cria a primeira plataforma normal imediatamente
        base_speed = -5 - (self.score // 70)
        first_platform = Platform(x=400, y=300, speed_x=base_speed)
        self.entities.append(first_platform)
        self.last_platform_x = 400 + 150  # Ajustado para largura
        self.last_platform_y = 300
        pygame.time.set_timer(pygame.USEREVENT + 1, 800)  # Inicia spawn imediatamente

        while not self.game_over:
            pygame.time.Clock().tick(60)
            current_time = pygame.time.get_ticks()

            # Verifica se o chão inicial deve sumir
            if self.initial_platform_active and current_time >= self.initial_platform_disappear_time:
                self.initial_platform_active = False
                self.entities = [ent for ent in self.entities if ent.name != "InitialPlatform"]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.game_music:
                        self.game_music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                        if self.jump_sound:
                            self.jump_sound.play()
                if event.type == pygame.USEREVENT + 1:
                    base_speed = -5 - (self.score // 70)
                    gap = random.randint(80, 150)
                    new_x = self.last_platform_x + gap
                    new_platform = Platform(x=new_x, prev_y=self.last_platform_y, speed_x=base_speed)
                    self.entities.append(new_platform)
                    self.last_platform_x = new_x + 150  # Ajustado para largura
                    self.last_platform_y = new_platform.rect.bottom
                    print(f"Nova plataforma com speed_x={base_speed}")

            # Atualiza velocidade de plataformas e fundo
            base_speed = -5 - (self.score // 70)
            for ent in self.entities:
                if ent.name in ["Platform", "Background"]:
                    ent.speed_x = base_speed

            # Move plataformas e fundo antes do jogador
            for ent in self.entities:
                if not self.game_over and ent.name != "Player" and ent.name != "InitialPlatform":
                    ent.move()
                    if ent.name == "Background" and ent.rect.right <= 0:
                        ent.rect.x += 800 * 2  # Mantém continuidade do fundo

            # Move o jogador
            for ent in self.entities:
                if ent.name == "Player" and not self.game_over:
                    if not ent.move():
                        self.game_over = True

            # Desenha todas as entidades
            for ent in self.entities:
                self.window.blit(ent.surf, ent.rect)

            # Verifica colisões
            self.player.on_platform = False
            for ent in self.entities:
                if (ent.name in ["Platform", "InitialPlatform"] and
                        self.player.rect.colliderect(ent.rect)):
                    # Verifica pouso na parte superior
                    if (self.player.speed_y >= 0 and
                            ent.rect.top - 5 <= self.player.rect.bottom <= ent.rect.top + 5):
                        self.player.speed_y = 0
                        self.player.rect.bottom = ent.rect.top
                        self.player.is_jumping = False
                        self.player.on_platform = True
                        self.player.jump_count = 2
                        print(f"Pouso na plataforma {ent.name} em y={ent.rect.top}, player.bottom={self.player.rect.bottom}")
                    # Verifica se o jogador está dentro da plataforma (tunelamento)
                    elif (self.player.rect.top < ent.rect.bottom and
                          self.player.rect.bottom > ent.rect.top and
                          self.player.speed_y > 0):
                        self.player.speed_y = 0
                        self.player.rect.bottom = ent.rect.top
                        self.player.is_jumping = False
                        self.player.on_platform = True
                        self.player.jump_count = 2
                        print(f"Correção de tunelamento na plataforma {ent.name} em y={ent.rect.top}, player.bottom={self.player.rect.bottom}")
                    else:
                        print(f"Colisão ignorada com {ent.name}: speed_y={self.player.speed_y}, player.bottom={self.player.rect.bottom}, platform.top={ent.rect.top}")

            self.entities = [ent for ent in self.entities if ent.name != "Platform" or ent.rect.right > 0]

            self.score = (pygame.time.get_ticks() - self.start_time) // 1000
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score(self.high_score)

            self.draw_text_with_shadow(f"Score: {self.score}", self.option_font, (255, 255, 255), (85, 20), 1)
            self.draw_text_with_shadow(f"Jumps: {self.player.jump_count}", self.option_font, (255, 255, 255), (85, 60), 1)
            pygame.display.flip()

        if self.game_music:
            self.game_music.stop()
        return self.show_game_over()