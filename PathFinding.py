# Example file showing a basic pygame "game loop"
import pygame
import math as m
from abc import ABC, abstractmethod
from overrides import overrides
import random

class Canvas(ABC):
  
  def __init__(self, width, height, background):
    self.width = width
    self.height = height
    self.screen = pygame.display.set_mode((width, height))
    self.clock = pygame.time.Clock()
    self.background = background
    self.running = True

  def _init_drawing(self):
    pygame.init()
    self.screen.fill(self.background)
  
  def _update_drawing(self, fps=60):
    pygame.display.flip()
    self.clock.tick(fps)
    for event in pygame.event.get():
      self._handle_event(event)

  def _handle_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False

  def _quit(self):
    pygame.quit()

  def draw_scene(self):
    """needs to be"""
    while self.running:
      self._init_drawing()
      self._draw()
      self._update_drawing()
    self._quit()

  @abstractmethod
  def _draw(self): ...



class Block:
  ROLES = {
        "start": ("green", False),
        "target": ("blue", False),
        "obstacle": ("black", False),
        "checked": ("pink", False),
        "default": ("white", True)
  }

  def __init__(self, x, y, w, role="") -> None:
    self.rect = pygame.Rect(x, y, w, w)
    self._f = 0
    self._g = 0
    self._h = 0
    self.role = role
    self.set_role(role)
    self.row = 0
    self.col = 0
    
  
  def set_role(self, role):
    self.role = role
    self.colour, _ = self.ROLES.get(role, self.ROLES["default"])
    self._is_start = role == "start"
    self._is_target = role == "target"
    self._is_obstacle = role == "obstacle"
    self._is_checked = role == "checked"
    
  def set_cost(self, g=None, h=None):
    self._g = g if g != None else self._g
    self._h = h if h != None else self._h
    self._f = self._g + self._h

class Field(Canvas):
  OBSTICALES = False
  moves = {
          "right": (0, 1),
          "down": (1, 0),
          "up": (-1, 0),
          "left": (0, -1)
      }

  def __init__(self, width:int, height:int, block_width:int , background):
    self._w = block_width
    self._n_rows = width//self._w
    self._n_cols = height//self._w
    self.cur_block_num = 0
    self.h_dist = 0
    self.g_dist = 0

    super().__init__(1 + self._n_cols * (1 + self._w), 1 + self._n_rows * (1 + self._w), background)
    # self.grid = [[Block(1 + col_pos * (1 + self._w), 1 + row_pos * (1 + self._w), self._w) 
    #               for col_pos in range(self._n_cols)] for row_pos in range(self._n_rows)]
    # self.grid[self.cur_block_num // self._n_cols][self.cur_block_num % self._n_cols].set_role("start")
    self.grid = []
    self._paint_grid()

  def get_h(self):
    self.h_dist = self._n_rows+self._n_cols - self.cur_block_num

  def _paint_grid(self):
    for row_pos in range(self._n_rows):
      row = []
      for col_pos in range(self._n_cols):
        new_block = Block(1 + col_pos * (1 + self._w), 1 + row_pos * (1 + self._w), self._w)
        if self.OBSTICALES and random.randint(0,10) == 5 and row_pos+col_pos != 0 and row_pos+col_pos != self._n_rows+self._n_cols:
          new_block.set_role("obstacle")
        row.append(new_block)

      self.grid.append(row)

    self.grid[0][0].set_role("start")
    self.grid[self._n_rows-1][self._n_cols-1].set_role("target")
  
  # def check_surrounding(self):
  #   while True:
  #     useable =self._move(self.grid[self.row][self.col].role)
  #     next_block:Block = self.grid[self.row][self.col]
  #     if useable:

  #       next_block.set_cost()
  #       continue
  #     if next_block._is_target:
  #       print("congrats found")






  def _move(self, role, direction, clear=False):
      self.row, self.col = divmod(self.cur_block_num, self._n_cols)
      
      move = self.moves.get(direction)
      if move is None:
          return False

      new_row = self.row + move[0]
      new_col = self.col + move[1]
      if not (0 <= new_row < self._n_rows and not self.grid[new_row][new_col]._is_obstacle and 0 <= new_col < self._n_cols):
          return False

      if clear:
          self.grid[self.row][self.col].set_role("None")
      else:
          self.grid[self.row][self.col].set_role(role)

      self.grid[new_row][new_col].set_role(role)
      self.cur_block_num = new_row * self._n_cols + new_col
      self.row = new_row
      self.col = new_col
      return True

  @overrides
  def _draw(self):
    for row in self.grid:
      for block in row:
          pygame.draw.rect(self.screen, block.colour, block.rect)

  @overrides
  def _handle_event(self, event):
    super()._handle_event(event)
 
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        self._move("start", "up")
      if event.key == pygame.K_DOWN:
        self._move("start", "down")
      if event.key == pygame.K_RIGHT:
        self._move("start", "right")
      if event.key == pygame.K_LEFT:
        self._move("start", "left")
       


can = Field(800,800,20,"purple")

can.draw_scene()
