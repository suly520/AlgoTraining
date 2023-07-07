# Example file showing a basic pygame "game loop"
import pygame
import math as m
from abc import ABC, abstractmethod
from overrides import overrides


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
        "default": ("white", True)
  }

  def __init__(self, x, y, w, role="") -> None:
    self.rect = pygame.Rect(x, y, w, w)
    self._g = None
    self._h = None
    self.set_role(role)
    
  
  def set_role(self, role):
    self.colour, _ = self.ROLES.get(role, self.ROLES["default"])
    self._is_start = role == "start"
    self._is_target = role == "target"
    self._is_obstacle = role == "obstacle"

  def set_parameter(self, g=None, h=None):
    if g != None:
      self._g = g
    if h != None:
      self._h = h

class Field(Canvas):

  def __init__(self, width:int, height:int, block_width:int , background):
    self._w = block_width
    self._n_rows = width//self._w
    self._n_cols = height//self._w
    self.current = 0
    super().__init__(1 + self._n_cols * (1 + self._w), 1 + self._n_rows * (1 + self._w), background)
    self.grid = [[Block(1 + col_pos * (1 + self._w), 1 + row_pos * (1 + self._w), self._w)
                      for col_pos in range(self._n_cols)] for row_pos in range(self._n_rows)]
    self.grid[self.current // self._n_cols][self.current % self._n_cols].set_role("start")
    self.key_heald = False

  @overrides
  def _draw(self):
    for row in self.grid:
      for block in row:
          pygame.draw.rect(self.screen, block.colour, block.rect)

  @overrides
  def _handle_event(self, event):
    super()._handle_event(event)
    
    if event.type == pygame.KEYDOWN:
      self.key_heald = True
    if event.type == pygame.KEYUP:
      self.key_heald = False
    
    # print(self.key_heald)
    if self.key_heald:
      row = self.current // self._n_cols
      col = self.current % self._n_cols
      if event.key == pygame.K_DOWN and row < self._n_rows - 1:
        self.grid[row][col].set_role("None")
        self.current += self._n_cols
        self.grid[row + 1][col].set_role("start")
      if event.key == pygame.K_UP and row > 0:
        self.grid[row][col].set_role("None")
        self.current -= self._n_cols
        self.grid[row - 1][col].set_role("start")
      if event.key == pygame.K_RIGHT and col < self._n_cols - 1:
        self.grid[row][col].set_role("None")
        self.current += 1
        self.grid[row][col + 1].set_role("start")
      if event.key == pygame.K_LEFT and col > 0:
        self.grid[row][col].set_role("None")
        self.current -= 1
        self.grid[row][col - 1].set_role("start")




can = Field(400,400,20,"purple")

can.draw_scene()
