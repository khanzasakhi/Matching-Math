import sys
import pygame
from easy import EasyLevel
from hard import HardLevel
from medium import MediumLevel
from opening import OpeningMenu

# 1. Inisialisasi Pygame & Layar Utama
pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Matching Math - Game Edukasi Matematika")

fps = 60
timer = pygame.time.Clock()

# 2. Inisialisasi Objek Menu & Level
opening_menu = OpeningMenu(screen_width, screen_height)
easy_level = EasyLevel(screen, timer, fps)
medium_level = MediumLevel(screen, timer, fps)
hard_level = HardLevel(screen, timer, fps)

# Mode Awal Permainan
game_state = "MENU"

# 3. Game Loop Utama
running = True
while running:
  timer.tick(fps)
  events = pygame.event.get()

  # Memeriksa Tombol Keluar (X)
  for event in events:
    if event.type == pygame.QUIT:
      running = False

  # A. Tampilan Opening Menu
  if game_state == "MENU":
    mouse_pos = pygame.mouse.get_pos()
    opening_menu.draw(screen, mouse_pos)

    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        selected = opening_menu.handle_click(event.pos)
        if selected == "EASY":
          easy_level.reset_game()
          game_state = "EASY"
        elif selected == "MEDIUM":
          medium_level.reset_game()
          game_state = "MEDIUM"
        elif selected == "HARD":
          hard_level.reset_game()
          game_state = "HARD"

  # B. Tampilan Level Easy
  elif game_state == "EASY":
    game_state = easy_level.update_and_draw(events)

  # C. Tampilan Level Medium
  elif game_state == "MEDIUM":
    game_state = medium_level.update_and_draw(events)

  # D. Tampilan Level Hard
  elif game_state == "HARD":
    game_state = hard_level.update_and_draw(events)

  pygame.display.flip()

pygame.quit()
sys.exit()