# SOME INFORMATION ABOUT THE A* ALGORITHM CODE:
## THIS CODE IS DONE TO FIND THE SHORTEST PATH FROM A STARTING POINT TO END POINT BY A* ALGORITHM.
## AFTER RUNNING THE CODE PRESS LEFT CLICK TO DECIDE THE STARTING AND END POINT AS WELL AS BARRIERS.
## PRESS "SPACE" TO SEE THE SHORTEST PATH . PRESS "c" TO CLEAR THE SCREEN
## AND PRESS "e" TO EXIT FROM THE RUNNING OF THE CODE

import pygame
from spot_class import Spot
from queue import PriorityQueue
import sys


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
WHITE = (255, 255, 255)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

def h(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_position(), end.get_position())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == quit:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def making_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_position(position, rows, width):
	gap_distance = width // rows
	y, x = position

	row = y // gap_distance
	col = x // gap_distance

	return row, col


def main(win, width):
	ROWS = 50
	grid = making_grid(ROWS, width)

	start = None
	stop = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == quit:
				run = False
			#  for LEFT
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != stop:
					start = spot
					start.make_start()

				elif not stop and spot != start:
					stop = spot
					stop.make_end()

				elif spot != stop and spot != start:
					spot.make_barrier_wall()
			# for  RIGHT
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == stop:
					stop = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and stop:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, stop)

				if event.key == pygame.K_c:
					start = None
					stop = None
					grid = making_grid(ROWS, width)
				if event.key==pygame.K_e:
					pygame.quit()
					sys.exit()


main(WIN, WIDTH)
