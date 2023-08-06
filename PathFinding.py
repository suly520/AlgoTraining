# Example file showing a basic pygame "game loop"
import pygame
import math as m
from Canvas import Canvas
from overrides import overrides
import random
from Block import Block


class PathFinder(Canvas):
  OBSTICALES = True
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
    self.start_row = 0
    self.start_col = 0
    self.start_block = None
    self.cur_block_num = self.start_row * self._n_cols + self.start_col
    self.cur_block = None
    self.target_row = self._n_rows-1
    self.target_col = self._n_cols-1-5
    self.target_block = None
    self.auto = False

    super().__init__(1 + self._n_cols * (1 + self._w), 1 + self._n_rows * (1 + self._w), background)
    self.grid = []
    self._paint_grid()

  def _calculate_h(self, row, col):
    return m.sqrt((self.target_row- row)**2 + (self.target_col- col)**2)


  def _get_min_direction(self, blocks, its_a_trap=False):
    if not blocks:
      raise ValueError("min() arg is an empty sequence")
    
    current_min = float("inf")
    for key in blocks.keys():
      if not (blocks[key].h <= current_min):
        # current distance is smaller than prev and if we are in a trap, block is a road or checked
        continue
      if its_a_trap:
        if not (blocks[key]._is_road or blocks[key]._is_checked):
          # not a road or checked blocked while in a trap
          continue
      elif blocks[key]._is_road or blocks[key]._is_checked:
        continue
      current_min = blocks[key].h
      direction = key
    return direction

  def _get_min_direction_new(self, blocks, its_a_trap=False):
    if not blocks:
        raise ValueError("min() arg is an empty sequence")

    # Define a function for the key parameter of min()
    def key_func(block_key):
        block = blocks[block_key]
        # If we're in a trap, consider only road or checked blocks
        if its_a_trap:
            return float('inf') if not (block._is_road or block._is_checked) else block.h
        # Otherwise, consider blocks that are not road or checked
        else:
            return float('inf') if (block._is_road or block._is_checked) else block.h

    # Find the key with the minimum value according to key_func
    return min(blocks, key=key_func)

  def _paint_grid(self):
    self.grid.clear()
    self.cur_block_num = self.start_row * self._n_cols + self.start_col
    for row_pos in range(self._n_rows):
      row = []
      for col_pos in range(self._n_cols):
        new_block = Block(1 + col_pos * (1 + self._w), 1 + row_pos * (1 + self._w), self._w)
        if self.OBSTICALES and random.randint(0,10) == 5 and row_pos+col_pos != 0 and row_pos+col_pos != self._n_rows+self._n_cols:
          new_block.set_role("obstacle")
        row.append(new_block)
      self.grid.append(row)

    self.start_block = self.grid[self.start_row][self.start_col]
    self.start_block.set_start()
    self.cur_block = self.start_block
    self.target_block = self.grid[self.target_row][self.target_col]
    self.target_block.set_target()
  
  def move_to_best(self):
    self.cur_block.neighbors.clear()
    self._move("up", check=True),
    self._move("down", check=True),
    self._move("right", check=True),
    self._move("left", check=True)
  
    neigh = self.cur_block.neighbors

    min_h_direction = self._get_min_direction(neigh)
    self._move(min_h_direction, role="road")
    if self.cur_block._is_target:
      self._paint_grid()


  def _move(self, direction, role="current", check=False):
      self.row, self.col = divmod(self.cur_block_num, self._n_cols)
      move = self.moves.get(direction)
      if move is None:
        # wrong direction input
        return False

      new_row = self.row + move[0]
      new_col = self.col + move[1]
      if not (0 <= new_row < self._n_rows and 0 <= new_col < self._n_cols):
        # outside the grid
        return False
      
      next_block = self.grid[new_row][new_col]
      next_pos = new_row * self._n_cols + new_col

      if next_block._is_obstacle and not check:
        # block is obsticale
        return False
  
      if check:
        if next_block._is_obstacle:
          return False
        if next_block._is_start:
          # skip start block as best path option
          return False
        else:
          next_block._is_checked = True
          next_block.h = self._calculate_h(new_row, new_col)
          self.cur_block.neighbors[direction] = next_block 
          return True

      self.cur_block_num = next_pos
      self.cur_block = next_block
      self.row = new_row
      self.col = new_col
      self.cur_block.g = self.cur_block.g+1
      self.cur_block.set_role(role)
      return True


  @overrides
  def _draw(self):
    if self.auto:
      self.move_to_best()
    for row in self.grid:
      for block in row:
          pygame.draw.rect(self.screen, block.colour, block.rect)
    
    

  @overrides
  def _handle_event(self, event):
    super()._handle_event(event)
 
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        self._move("up")
      if event.key == pygame.K_DOWN:
        self._move("down")
      if event.key == pygame.K_RIGHT:
        self._move("right")
      if event.key == pygame.K_LEFT:
        self._move("left")
      if event.key == pygame.K_RETURN:
        self.move_to_best()
      if event.key == pygame.K_BACKSPACE:
        self._paint_grid()
      if event.key == pygame.K_HASH:
        self.auto = not self.auto
       

if __name__ == "__main__":
  can = PathFinder(800,800,10,"purple")
  can.draw_scene()
