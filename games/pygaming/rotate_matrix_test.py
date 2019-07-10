import numpy as np
from math import sin, cos, radians
import pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 720, 480
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def crop(array, background=(0, 0, 0)):
    rows, cols, _ = array.shape
    left, right, top, bottom = 0, cols, 0, rows

    for row in range(rows):
        if not np.all(array[row] == background):
            top = row
            break
    for row in range(rows - 1, top, -1):
        if not np.all(array[row] == background):
            bottom = row
            break

    np.transpose(array, axes=(1, 0, 2))

    for col in range(cols):
        if not np.all(array[col] == background):
            left = col
            break
    for col in range(cols - 1, left, -1):
        if not np.all(array[col] == background):
            right = col
            break

    np.transpose(array, axes=(1, 0, 2))

    return array[top:bottom+1, left:right+1]


def rotate(surface, angle):
    rect = surface.get_rect()
    width, height = surface.get_size()
    image_array = pygame.surfarray.array3d(surface)

    angle = radians(angle)

    # Rotation matrix: https://en.wikipedia.org/wiki/Rotation_matrix
    rotation = np.array(
        ((cos(angle), -sin(angle)),
         (sin(angle), cos(angle))
         ), dtype=np.float16
    )

    # Rotates the corners of the image because the distance between 2 opposite corners will always be the furthest
    # distance. This helps us calculate the new width and height of our new rotated image.
    y_list, x_list = zip(*(
        (position @ rotation) for position in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright)
    ))
    min_x, min_y = min(x_list), min(y_list)
    new_width = int(abs(min_x - max(x_list))) + 1
    new_height = int(abs(min_y - max(y_list))) + 1

    # Since we're rotating the image at the topleft corner and not in the center it'll be moved. By adding the offset
    # we just move it back in place.
    offset = -int(min_y), -int(min_x)

    rotated_image_array = np.zeros(shape=(new_height, new_width, 3), dtype=np.uint8)

    for row in range(height):  # Not the newly calculated height, but the original image's height.
        for col in range(width):
            y, x = (row, col) @ rotation + offset
            rotated_image_array[int(y), int(x)] = image_array[row, col]

    rotated_image_array = crop(rotated_image_array)

    return pygame.surfarray.make_surface(rotated_image_array)


def main():
    running = True
    original_image = pygame.Surface((200, 200))
    original_image.fill(pygame.Color('red'))
    image = original_image
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    print('Reset image.')
                    image = original_image
                if event.key == pygame.K_2:
                    print('Starting rotating.')
                    time = pygame.time.get_ticks()
                    image = rotate(image, 5)
                    time = pygame.time.get_ticks() - time
                    print('Finished rotating in {:.4E} s.'.format(time / 1000))

        screen.fill((255, 255, 255))
        screen.blit(image, image.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.update()


if __name__ == '__main__':
    main()
