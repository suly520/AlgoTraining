import pygame
from abc import ABC, abstractmethod

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
  
  def _update_drawing(self, fps=5):
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