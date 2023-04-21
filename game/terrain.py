# import random
# import pygame
# import noise

# def generate_terrain(length):
#     terrain_scale = 50  # Adjust this to control the terrain roughness
#     terrain_octaves = 6  # Adjust this to control the terrain complexity
#     terrain_persistence = 0.5  # Adjust this to control the terrain contrast

#     terrain = []
#     for i in range(length):
#         sample_x = i / length * terrain_scale
#         sample_y = 0  # Use 0 as the y-coordinate for 1D Perlin noise
#         sample = noise.pnoise1(sample_x, octaves=terrain_octaves, persistence=terrain_persistence)
#         terrain.append(int((sample + 1) / 2 * 200 + 100))  # Scale the sample to fit within the screen and add a base height of 100

#     terrain_surface = pygame.Surface((length, max(terrain)))
#     terrain_surface.fill((150, 150, 150))  # Gray color for the terrain

#     # Draw the terrain polygon
#     terrain_points = [(i, terrain[i]) for i in range(length)]
#     terrain_points.append((length-1, max(terrain)))
#     terrain_points.append((0, max(terrain)))
#     pygame.draw.polygon(terrain_surface, (100, 100, 100), terrain_points)

#     return terrain_surface
