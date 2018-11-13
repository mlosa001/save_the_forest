import pygame

# Relative Imports
from src.classes.common.Button import Button
from src.classes.common.Menu import Menu
from src.classes.common.GameMap import GameMap
from src.classes.Shop import Shop

class Game:
    def __init__(self, screen):
        # Initial Game Properties
        self.level = 0
        self.playing = True
        self.screen = screen
        self.menu_open = True
        self.clock = pygame.time.Clock() 
        self.all_players = []
        self.last = pygame.time.get_ticks()
        self.money_cooldown =  2000
        self.coin_sound = pygame.mixer.Sound('./src/assets/music/Coin.ogg') 

    def main(self):
        self.create()
        self.update()

    def create(self):
        pygame.mixer.music.load('./src/assets/music/background_music.ogg')

        color = [22, 160, 133]
        size = (150,50)

        # Creates Map
        img_url = './src/assets/maps/forest1/map02.png'
        self.map = GameMap(img_url)

        # Create the menu for the game
        self.menu = Menu(self.screen, color, size, self.map)
        self.menu.create_menu()

        # Creates Shop
        self.shop = Shop(self.screen)

    def update(self):
        while self.playing:
            # Game FPS (Frame per second)
            self.clock.tick()
            pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

            # All Game Runing Game Events

            # Active state in the game
            self.active_state()
            self.all_event()

            if not self.menu_open:
                """ All Game Logic Goes Here"""
                # Active Shop
                self.shop.render_shop()

                # Get Money Every now and then
                now = pygame.time.get_ticks()
                if now - self.last >= self.money_cooldown:
                    self.shop.time_money(True)
                    self.coin_sound.play()
                    self.last = now

                # All Players moving
                for player in self.all_players:
                    player.shoot_bananas()

            # Update the graphics in the game
            pygame.display.update()

    def game_over(self):
        pass

    def active_state(self):
        if self.menu_open:
            self.menu.active()
        else:
            self.map.render(self.screen)
            
    def level_up(self):
        self.level += 1
        pass

    def menu_state(self):
        if self.menu_open:
            # In Game Music
            pygame.mixer.music.play()
            self.menu_open = False
        else:
            self.menu_open = True

    def all_event(self):
        for event in pygame.event.get():
            # Closes the Game on exit
            if event.type == pygame.QUIT:
                self.playing = False

            if self.menu_open:
                self.menu.start.on_click(event, self.menu_state)

            if not self.menu_open:
                self.shop.shop_event(event, self.all_players)