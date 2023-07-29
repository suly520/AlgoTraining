import pygame

class Block:
  neighbors = {
    "up":None,
    "down":None,
    "left":None,
    "right":None
  }
  ROLES = {
    "current": "yellow",
    "start":"green",
    "target": "blue",
    "obstacle": "grey",
    "road": "yellow",
    "default": "white"
  }

  def __init__(self, x, y, w, role="") -> None:
    self.rect = pygame.Rect(x, y, w, w)
    self.f = 0
    self.g = 0
    self.h = 0
    self.role = role
    self._is_checked = False
    self._is_target = False
    self._is_start = False
    self.set_role(role)
    
  def set_role(self, role):
    if self._is_target or self._is_start:
      return
    self.role = role
    self.colour = self.ROLES.get(role, self.ROLES["default"])
    self._is_obstacle = role == "obstacle"
    self._is_road = role == "road"
  
  def set_start(self):
    self.colour = self.ROLES.get("start")
    self._is_start = True
  
  def set_target(self):
    self.colour = self.ROLES.get("target")
    self._is_target = True