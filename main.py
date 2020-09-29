import pygame as pg
import pymunk.pygame_util
from random import randrange
from pymunk.vec2d import Vec2d

NUMBER_OF_BALLS = 30
SIZE = WIDTH, HEIGHT = 1000, 600
FPS = 60

pymunk.pygame_util.positive_y_is_up = False
pg.init()

space = pymunk.Space()
space.gravity = 0, 0

surface = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)


def draw_ball():
    ball_radius = randrange(10, 50, 1)
    ball_mass = randrange(1, 3)
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(ball_radius, WIDTH - ball_radius), randrange(ball_radius, HEIGHT - ball_radius)
    ball_body.apply_impulse_at_local_point(randrange(200, 500) * Vec2d([randrange(-1, 1) for _ in range(2)]))
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 1
    ball_shape.friction = 0.1
    ball_shape.color = [randrange(256) for _ in range(4)]
    space.add(ball_body, ball_shape)


def draw_border():
    border_bottom = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5)
    border_top = pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5)
    border_left = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5)
    border_right = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5)
    border_bottom.elasticity = border_top.elasticity = border_left.elasticity = border_right.elasticity = 1
    border_bottom.friction = border_top.friction = border_left.friction = border_right.friction = 0.1
    space.add(border_bottom, border_top, border_left, border_right)


if __name__ == '__main__':
    draw_border()

    for item in range(NUMBER_OF_BALLS):
        draw_ball()

    while True:
        surface.fill(pg.Color('#000000'))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        space.step(1 / FPS)
        space.debug_draw(draw_options)

        pg.display.flip()
        clock.tick(FPS)
