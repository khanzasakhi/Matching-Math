import pygame

MUSTARD = (255, 220, 94)  # #FFDC5E (Easy)
WINTER_MIST = (214, 233, 237)  # #D6E9ED (Medium Baru)
PASTEL_PINK = (255, 194, 209)  # #FFC2D1 (Hard)
LEMON_CHIFFON = (252, 246, 189)  # #FCF6BD (Background Opening)
HOT_PINK = (255, 105, 180)  # #FF69B4 (Judul Main)
COCOA_ROSE = (104, 79, 72)  # #684F48 (Teks & Bingkai)


# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 40, 80)
GREEN = (0, 200, 0)
ORANGE = (255, 140, 0)
RED = (220, 50, 50)
YELLOW = (255, 215, 0)


class OpeningMenu:

  def __init__(self, screen_width, screen_height):
    self.screen_width = screen_width
    self.screen_height = screen_height

    # Font
    self.title_font = pygame.font.SysFont("segoeui", 32, bold=True)
    self.sub_font = pygame.font.SysFont("segoeui", 20, bold=True)
    self.menu_font = pygame.font.SysFont("segoeui", 22, bold=True)

    # Area Tombol Level
    self.easy_rect = pygame.Rect(175, 260, 250, 50)
    self.medium_rect = pygame.Rect(175, 330, 250, 50)
    self.hard_rect = pygame.Rect(175, 400, 250, 50)

  def draw_polka_dots(self, screen):
    """Fungsi untuk menggambar motif polkadot selang-seling di latar belakang"""
    dot_color = WHITE  # Warna bintik polkadot (Putih)
    radius = 5  # Ukuran lingkaran
    spacing = 30  # Jarak antar lingkaran

    for y in range(15, self.screen_height + spacing, spacing):
      offset = (spacing // 2) if ((y // spacing) % 2 == 1) else 0
      for x in range(
          15 - spacing + offset, self.screen_width + spacing, spacing
      ):
        pygame.draw.circle(screen, dot_color, (x, y), radius)

  def draw_animated_button(
      self, screen, rect, text, button_color, mouse_pos, is_mouse_pressed
  ):
    """Fungsi menggambar tombol dengan efek animasi ditekan (3D press)"""
    is_hover = rect.collidepoint(mouse_pos)
    is_pressed = is_hover and is_mouse_pressed

    # Jika ditekan, tombol turun 4 piksel ke bawah
    offset_y = 4 if is_pressed else 0
    drawn_rect = rect.move(0, offset_y)

    # 1. Gambar Bayangan 3D di Bawah Tombol (Hanya saat tidak ditekan penuh)
    if not is_pressed:
      shadow_rect = rect.move(0, 4)
      pygame.draw.rect(screen, COCOA_ROSE, shadow_rect, 0, 10)

    # 2. Gambar Isian Tombol (Warna penuh saat hover, Putih saat normal)
    fill_color = button_color if is_hover else WHITE
    pygame.draw.rect(screen, fill_color, drawn_rect, 0, 10)

    # 3. Gambar Bingkai Tombol
    pygame.draw.rect(screen, COCOA_ROSE, drawn_rect, 3, 10)

    # 4. Gambar Teks (Mengikuti pergeseran tombol)
    text_surf = self.menu_font.render(text, True, COCOA_ROSE)
    screen.blit(text_surf, text_surf.get_rect(center=drawn_rect.center))

  def draw(self, screen, mouse_pos):
    # Cek status tombol mouse ditekan (klik kiri)
    is_mouse_pressed = pygame.mouse.get_pressed()[0]

  def draw_text_with_outline(
      self,
      screen,
      font,
      text,
      text_color,
      outline_color,
      center_pos,
      thickness=2,
  ):
    """Fungsi khusus untuk menggambar teks dengan garis tepi (outline)"""
    cx, cy = center_pos

    # 1. Gambar outline di sekeliling teks (8 arah)
    outline_surf = font.render(text, True, outline_color)
    for dx in range(-thickness, thickness + 1):
      for dy in range(-thickness, thickness + 1):
        if dx != 0 or dy != 0:
          screen.blit(
              outline_surf, outline_surf.get_rect(center=(cx + dx, cy + dy))
          )

    # 2. Gambar teks utama di bagian depan
    main_surf = font.render(text, True, text_color)
    screen.blit(main_surf, main_surf.get_rect(center=(cx, cy)))

  def draw(self, screen, mouse_pos):
    screen.fill(LEMON_CHIFFON)

    # Gambar Motif Polkadot
    self.draw_polka_dots(screen)

    # Judul & Subjudul dengan Outline Putih
    title_text = "MATCHING MATH"
    sub_text = "Game Edukasi Pencocokan Kartu Matematika"

    # 1. Render Teks Outline (Putih) & Teks Utama
    title_outline = self.title_font.render(title_text, True, WHITE)
    title_surf = self.title_font.render(title_text, True, HOT_PINK)

    sub_outline = self.sub_font.render(sub_text, True, WHITE)
    sub_surf = self.sub_font.render(sub_text, True, COCOA_ROSE)

    # 2. Gambar Outline Putih di Sekeliling Judul (posisi Y=110)
    for dx in [-2, -1, 0, 1, 2]:
      for dy in [-2, -1, 0, 1, 2]:
        if dx != 0 or dy != 0:
          screen.blit(
              title_outline,
              title_outline.get_rect(
                  center=(self.screen_width // 2 + dx, 100 + dy)
              ),
          )
    # Gambar Judul Utama
    screen.blit(
        title_surf, title_surf.get_rect(center=(self.screen_width // 2, 100))
    )

    # 3. Gambar Outline Putih di Sekeliling Subjudul (posisi Y=155)
    for dx in [-2, -1, 0, 1, 2]:
      for dy in [-2, -1, 0, 1, 2]:
        if dx != 0 or dy != 0:
          screen.blit(
              sub_outline,
              sub_outline.get_rect(
                  center=(self.screen_width // 2 + dx, 160 + dy)
              ),
          )
    # Gambar Subjudul Utama
    screen.blit(
        sub_surf, sub_surf.get_rect(center=(self.screen_width // 2, 155))
    )

    # Label Petunjuk
    label_surf = self.menu_font.render("PILIH LEVEL PERMAINAN:", True, COCOA_ROSE)
    screen.blit(
        label_surf, label_surf.get_rect(center=(self.screen_width // 2, 215))
    )

    # Cek status klik kiri mouse
    is_mouse_pressed = pygame.mouse.get_pressed()[0]

    # --- Tombol Easy (Winter Mist) ---
    is_hover_easy = self.easy_rect.collidepoint(mouse_pos)
    is_pressed_easy = is_hover_easy and is_mouse_pressed
    offset_easy = 4 if is_pressed_easy else 0
    drawn_easy = self.easy_rect.move(0, offset_easy)

    if not is_pressed_easy:
      pygame.draw.rect(
          screen, COCOA_ROSE, self.easy_rect.move(0, 4), 0, 10
      )  # Bayangan 3D
    easy_col = WINTER_MIST if is_hover_easy else WHITE
    pygame.draw.rect(screen, easy_col, drawn_easy, 0, 10)
    pygame.draw.rect(screen, COCOA_ROSE, drawn_easy, 3, 10)
    t_easy = self.menu_font.render("EASY (12 Kartu)", True, COCOA_ROSE)
    screen.blit(t_easy, t_easy.get_rect(center=drawn_easy.center))

    # --- Tombol Medium (Mustard) ---
    is_hover_med = self.medium_rect.collidepoint(mouse_pos)
    is_pressed_med = is_hover_med and is_mouse_pressed
    offset_med = 4 if is_pressed_med else 0
    drawn_med = self.medium_rect.move(0, offset_med)

    if not is_pressed_med:
      pygame.draw.rect(
          screen, COCOA_ROSE, self.medium_rect.move(0, 4), 0, 10
      )  # Bayangan 3D
    med_col = MUSTARD if is_hover_med else WHITE
    pygame.draw.rect(screen, med_col, drawn_med, 0, 10)
    pygame.draw.rect(screen, COCOA_ROSE, drawn_med, 3, 10)
    t_med = self.menu_font.render("MEDIUM (24 Kartu)", True, COCOA_ROSE)
    screen.blit(t_med, t_med.get_rect(center=drawn_med.center))

    # --- Tombol Hard (Pastel Pink) ---
    is_hover_hard = self.hard_rect.collidepoint(mouse_pos)
    is_pressed_hard = is_hover_hard and is_mouse_pressed
    offset_hard = 4 if is_pressed_hard else 0
    drawn_hard = self.hard_rect.move(0, offset_hard)

    if not is_pressed_hard:
      pygame.draw.rect(
          screen, COCOA_ROSE, self.hard_rect.move(0, 4), 0, 10
      )  # Bayangan 3D
    hard_col = PASTEL_PINK if is_hover_hard else WHITE
    pygame.draw.rect(screen, hard_col, drawn_hard, 0, 10)
    pygame.draw.rect(screen, COCOA_ROSE, drawn_hard, 3, 10)
    t_hard = self.menu_font.render("HARD (48 Kartu)", True, COCOA_ROSE)
    screen.blit(t_hard, t_hard.get_rect(center=drawn_hard.center))

  def handle_click(self, pos):
    if self.easy_rect.collidepoint(pos):
      return "EASY"
    elif self.medium_rect.collidepoint(pos):
      return "MEDIUM"
    elif self.hard_rect.collidepoint(pos):
      return "HARD"
    return None