import random
import pygame

# ==========================================
# PALET WARNA BARU (Level Medium)
# ==========================================
DARK_BROWN = (113, 82, 30)     # #71521e (Teks, Bingkai & Header)
WARM_GOLDEN = (188, 143, 77)   # #bc8f4d (Kartu Tertutup & Menu Bawah)
SAGE_GREEN = (204, 222, 197)   # #ccdec5 (Kartu Terbuka / Match & Banner)
VANILLA_CREAM = (255, 247, 230) # #FFF7E6 (Latar Belakang Utama & Tombol Restart/Menu)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bank Soal Matematika (12 Pasang / 24 Kartu)
all_math_pairs = [
    ("0,5", "50%", "0,5 = 5/10 = 50/100 (sama dengan 50%)"),
    ("0,25", "25%", "0,25 = 25/100 (sama dengan 25%)"),
    ("0,75", "75%", "0,75 = 75/100 (sama dengan 75%)"),
    ("0,1", "10%", "0,1 = 1/10 = 10/100 (sama dengan 10%)"),
    ("0,2", "20%", "0,2 = 2/10 = 20/100 (sama dengan 20%)"),
    ("0,4", "40%", "0,4 = 4/10 = 40/100 (sama dengan 40%)"),
    ("0,6", "60%", "0,6 = 6/10 = 60/100 (sama dengan 60%)"),
    ("0,8", "80%", "0,8 = 8/10 = 80/100 (sama dengan 80%)"),
    ("√4", "2", "√4 = 2 (karena 2 × 2 = 4)"),
    ("√9", "3", "√9 = 3 (karena 3 × 3 = 9)"),
    ("√16", "4", "√16 = 4 (karena 4 × 4 = 16)"),
    ("√25", "5", "√25 = 5 (karena 5 × 5 = 25)"),
    ("√36", "6", "√36 = 6 (karena 6 × 6 = 36)"),
    ("2²", "4", "2² = 2 × 2 = 4"),
    ("3²", "9", "3² = 3 × 3 = 9"),
    ("4²", "16", "4² = 4 × 4 = 16"),
]


class MediumLevel:

  def __init__(self, screen, timer, fps):
    self.screen = screen
    self.timer = timer
    self.fps = fps
    self.screen_width = 600
    self.screen_height = 600

    # Grid Level Medium: 24 Kartu (4 baris x 6 kolom)
    self.rows = 4
    self.cols = 6
    self.card_w = 60
    self.card_h = 60
    self.gap_x = 15
    self.gap_y = 15

    total_w = self.cols * self.card_w + (self.cols - 1) * self.gap_x
    total_h = self.rows * self.card_h + (self.rows - 1) * self.gap_y
    self.start_x = (self.screen_width - total_w) // 2
    self.start_y = 100 + (400 - total_h) // 2

    # Pengaturan Font
    self.title_font = pygame.font.SysFont("segoeui", 28, bold=True)
    self.small_font = pygame.font.SysFont("segoeui", 20)
    self.small_font_bold = pygame.font.SysFont("segoeui", 20, bold=True)
    self.card_font = pygame.font.SysFont("segoeui", 18, bold=True)
    self.info_font = pygame.font.SysFont("segoeui", 14, bold=True)

    self.reset_game()

  def reset_game(self):
    self.correct = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
    self.spaces = []
    self.score = 0
    self.matches = 0
    self.game_over = False
    self.current_explanation = ""
    self.explanation_timer = 0

    self.first_guess = False
    self.second_guess = False
    self.first_guess_num = 0
    self.second_guess_num = 0

    self.start_ticks = pygame.time.get_ticks()
    self.elapsed_time = 0
    self.generate_board()

  def generate_board(self):
    needed_pairs = (self.rows * self.cols) // 2
    selected_pairs = random.sample(all_math_pairs, needed_pairs)

    card_deck = []
    for pair_id in range(len(selected_pairs)):
      val_a, val_b, exp = selected_pairs[pair_id]
      card_deck.append({"text": val_a, "id": pair_id, "exp": exp})
      card_deck.append({"text": val_b, "id": pair_id, "exp": exp})

    random.shuffle(card_deck)
    self.spaces = card_deck

  def get_card_rect(self, col, row):
    x = self.start_x + col * (self.card_w + self.gap_x)
    y = self.start_y + row * (self.card_h + self.gap_y)
    return pygame.Rect(x, y, self.card_w, self.card_h)

  def draw_background(self):
    # 1. Latar Belakang Utama (Vanilla Cream #FFF7E6)
    self.screen.fill(VANILLA_CREAM)

    # 2. Header Atas (Dark Brown)
    pygame.draw.rect(self.screen, DARK_BROWN, (0, 0, self.screen_width, 90))

    # Judul Header Singkat "LEVEL MEDIUM"
    title_text = self.title_font.render("LEVEL MEDIUM", True, WHITE)
    self.screen.blit(title_text, (15, 12))

    # Banner Teks Penjelasan Edukasi saat Cocok
    if self.current_explanation and (
        pygame.time.get_ticks() - self.explanation_timer < 4000
    ):
      pygame.draw.rect(
          self.screen, SAGE_GREEN, (12, 48, self.screen_width - 24, 36), 0, 8
      )
      pygame.draw.rect(
          self.screen, DARK_BROWN, (12, 48, self.screen_width - 24, 36), 2, 8
      )

      info_text = self.info_font.render(
          f"{self.current_explanation}", True, DARK_BROWN
      )
      info_rect = info_text.get_rect(center=(self.screen_width // 2, 66))
      self.screen.blit(info_text, info_rect)

    # 3. Menu Bawah (Warna WARM_GOLDEN + Bingkai DARK_BROWN)
    pygame.draw.rect(
        self.screen, WARM_GOLDEN, (0, 510, self.screen_width, 90)
    )
    pygame.draw.rect(
        self.screen, DARK_BROWN, (0, 510, self.screen_width, 90), 3
    )

    score_text = self.small_font_bold.render(
        f"Turns: {self.score}", True, DARK_BROWN
    )
    self.screen.blit(score_text, (20, 525))

    if not self.game_over:
      self.elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
    time_text = self.small_font_bold.render(
        f"Time: {self.elapsed_time}s", True, DARK_BROWN
    )
    self.screen.blit(time_text, (20, 555))

    # Tombol Restart (Vanilla Cream #FFF7E6 + Teks Bold Dark Brown)
    restart_button = pygame.draw.rect(
        self.screen, VANILLA_CREAM, (self.screen_width - 310, 525, 140, 50), 0, 8
    )
    pygame.draw.rect(
        self.screen, DARK_BROWN, (self.screen_width - 310, 525, 140, 50), 2, 8
    )
    restart_text = self.small_font_bold.render("Restart", True, DARK_BROWN)
    self.screen.blit(restart_text, (self.screen_width - 270, 537))

    # Tombol Kembali ke Menu (Vanilla Cream #FFF7E6 + Teks Bold Dark Brown)
    menu_button = pygame.draw.rect(
        self.screen, VANILLA_CREAM, (self.screen_width - 150, 525, 130, 50), 0, 8
    )
    pygame.draw.rect(
        self.screen, DARK_BROWN, (self.screen_width - 150, 525, 130, 50), 2, 8
    )
    menu_text = self.small_font_bold.render("Menu", True, DARK_BROWN)
    self.screen.blit(menu_text, (self.screen_width - 110, 537))

    # Teks Victory di Kanan Atas
    if self.game_over:
      victory_text = self.title_font.render("VICTORY!", True, SAGE_GREEN)
      self.screen.blit(victory_text, (self.screen_width - 180, 12))

    return restart_button, menu_button

  def draw_board(self):
    board_list = []
    # Kartu Tertutup (Warm Golden)
    for i in range(self.cols):
      for j in range(self.rows):
        rect = self.get_card_rect(i, j)
        piece = pygame.draw.rect(self.screen, WARM_GOLDEN, rect, 0, 8)
        pygame.draw.rect(self.screen, DARK_BROWN, rect, 2, 8)
        board_list.append(piece)

    # Kartu Cocok (Sage Green)
    for c in range(self.cols):
      for r in range(self.rows):
        if self.correct[c][r] == 1:
          rect = self.get_card_rect(c, r)
          idx = c * self.rows + r
          pygame.draw.rect(self.screen, SAGE_GREEN, rect, 0, 8)
          pygame.draw.rect(self.screen, DARK_BROWN, rect, 2, 8)
          piece_text = self.card_font.render(
              f"{self.spaces[idx]['text']}", True, DARK_BROWN
          )
          self.screen.blit(
              piece_text, piece_text.get_rect(center=rect.center)
          )

    return board_list

  def animate_card_flip(self, card_index):
    col = card_index // self.rows
    row = card_index - (col * self.rows)
    target_rect = self.get_card_rect(col, row)
    center_x, center_y = target_rect.center

    for w in range(self.card_w, 0, -8):
      self.draw_background()
      self.draw_board()
      c_rect = pygame.Rect(0, 0, w, self.card_h)
      c_rect.center = (center_x, center_y)
      pygame.draw.rect(self.screen, WARM_GOLDEN, c_rect, 0, 8)
      pygame.draw.rect(self.screen, DARK_BROWN, c_rect, 2, 8)
      pygame.display.flip()
      self.timer.tick(120)

    for w in range(0, self.card_w + 2, 8):
      self.draw_background()
      self.draw_board()
      c_rect = pygame.Rect(0, 0, w, self.card_h)
      c_rect.center = (center_x, center_y)
      pygame.draw.rect(self.screen, SAGE_GREEN, c_rect, 0, 8)
      pygame.draw.rect(self.screen, DARK_BROWN, c_rect, 2, 8)
      if w > 20:
        p_text = self.card_font.render(
            f"{self.spaces[card_index]['text']}", True, DARK_BROWN
        )
        self.screen.blit(p_text, p_text.get_rect(center=(center_x, center_y)))
      pygame.display.flip()
      self.timer.tick(120)

  def check_guesses(self, first, second):
    if self.spaces[first]["id"] == self.spaces[second]["id"]:
      col1 = first // self.rows
      row1 = first - (col1 * self.rows)
      col2 = second // self.rows
      row2 = second - (col2 * self.rows)

      if self.correct[col1][row1] == 0 and self.correct[col2][row2] == 0:
        self.correct[col1][row1] = 1
        self.correct[col2][row2] = 1
        self.matches += 1
        self.current_explanation = self.spaces[first]["exp"]
        self.explanation_timer = pygame.time.get_ticks()
    self.score += 1

  def update_and_draw(self, events):
    restart_btn, menu_btn = self.draw_background()
    board_list = self.draw_board()

    if self.matches == (self.rows * self.cols) // 2:
      self.game_over = True

    for num, is_guess in [
        (self.first_guess_num, self.first_guess),
        (self.second_guess_num, self.second_guess),
    ]:
      if is_guess:
        c = num // self.rows
        r = num - (c * self.rows)
        rect = self.get_card_rect(c, r)
        pygame.draw.rect(self.screen, SAGE_GREEN, rect, 0, 8)
        pygame.draw.rect(self.screen, DARK_BROWN, rect, 2, 8)
        txt = self.card_font.render(
            f"{self.spaces[num]['text']}", True, DARK_BROWN
        )
        self.screen.blit(txt, txt.get_rect(center=rect.center))

    if self.first_guess and self.second_guess:
      self.check_guesses(self.first_guess_num, self.second_guess_num)
      self.draw_background()
      self.draw_board()

      for num in [self.first_guess_num, self.second_guess_num]:
        c = num // self.rows
        r = num - (c * self.rows)
        rect = self.get_card_rect(c, r)
        pygame.draw.rect(self.screen, SAGE_GREEN, rect, 0, 8)
        pygame.draw.rect(self.screen, DARK_BROWN, rect, 2, 8)
        txt = self.card_font.render(
            f"{self.spaces[num]['text']}", True, DARK_BROWN
        )
        self.screen.blit(txt, txt.get_rect(center=rect.center))

      pygame.display.flip()
      pygame.time.delay(1200)
      self.first_guess = False
      self.second_guess = False

    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if restart_btn.collidepoint(event.pos):
          self.reset_game()
        elif menu_btn.collidepoint(event.pos):
          return "MENU"

        for i, button in enumerate(board_list):
          if button.collidepoint(event.pos):
            c = i // self.rows
            r = i - (c * self.rows)
            if self.correct[c][r] == 0:
              if not self.first_guess:
                self.animate_card_flip(i)
                self.first_guess = True
                self.first_guess_num = i
              elif not self.second_guess and i != self.first_guess_num:
                self.animate_card_flip(i)
                self.second_guess = True
                self.second_guess_num = i
    return "MEDIUM"