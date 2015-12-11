"""
Project: Asteroids
Author: Vu Tran
Website: http://vu-tran.com/

Events:
 - draw (DrawEvent)
 - click (ClickEvent)
 - keydown (KeyEvent)
 - keyup (KeyEvent)
 - count (TimerEvent)

"""

# import modules
import simplegui, math, random

# configurations
WINDOW_SIZE = (800, 600)
NUM_LIVES = 3

# create cache stores for static assets
CACHE_STORE = {}

# define Event objects
class DrawEvent:
    def __init__(self, canvas, frame):
        self.canvas = canvas
        self.frame = frame

class KeyEvent:
    def __init__(self, key):
        self.key = key

class ClickEvent:
    def __init__(self, position):
        self.position = position

class TimerEvent:
    def __init__(self, time):
        self.time = time

class Dispatcher:
    def __init__(self):
        self.events = []
    def add(self, event_name, handler):
        """
        Registers a new event handler
        """
        data = {
            "name": event_name,
            "handler": handler
        }
        self.events.append(data)
    def run(self, name, args):
        """
        Runs all events that matches the given name
        """
        # iterate through all events
        for e in self.events:
            # if it's of the draw type
            if e['name'] == name:
                # call the given handler
                e['handler'](args)

class Frame:
    def __init__(self, frame, size):
        self.frame = frame
        self.size = size
    def get_size(self):
        """
        Returns the size of the frame
        """
        return self.size
    def get_width(self):
        """
        Returns the width of the frame
        """
        return self.size[0]
    def get_height(self):
        """
        Returns the height of the frame
        """
        return self.size[1]
    def get(self):
        """
        Returns the frame object
        """
        return self.frame
    def start(self):
        """
        Starts the frame
        """
        self.get().start()
    def add_button(self, label, handler):
        """
        Adds a new button to the frame
        """
        self.get().add_button(label, handler)
    def set_draw_handler(self, handler):
        self.get().set_draw_handler(handler)
    def set_mouseclick_handler(self, handler):
        self.get().set_mouseclick_handler(handler)
    def set_keydown_handler(self, handler):
        self.get().set_keydown_handler(handler)
    def set_keyup_handler(self, handler):
        self.get().set_keyup_handler(handler)

class Timer:
    def __init__(self, delay):
        # sets the initial time to 0
        self.time = 0
        # sets the delay
        self.delay = delay
        # creates a timer
        self.timer = simplegui.create_timer(delay, self.count)
    def get_timer(self):
        return self.timer
    def get_time(self):
        return self.time
    def count(self):
        self.time += self.delay
        timer_event = TimerEvent(self.get_time())
        dispatcher.run('count', timer_event)
    def start(self):
        self.get_timer().start()

class Image:
    def __init__(self, url, size, center = None):
        # sets the url
        self.url = url
        # loads the image
        if CACHE_STORE.has_key(url):
            self.image = CACHE_STORE[url]
        else:
            self.image = simplegui.load_image(url)
            CACHE_STORE[url] = self.image
        # sets the dimensions of the image
        self.set_size(size)
        # if the center is not set
        if center is None:
            self.set_center((size[0] / 2, size[1] / 2))
        else:
            self.set_center(center)
    def set_size(self, size):
        self.size = size
    def get_size(self):
        return self.size
    def set_center(self, center):
        self.center = center
    def get_center(self):
        return self.center
    def get_image(self):
        return self.image
    def draw_at(self, canvas, center_dest, size_dest, rotation = 0):
        """
        Draws the image into the canvas at the given
        center destination and size
        """
        canvas.draw_image(self.get_image(), self.get_center(), self.get_size(), center_dest, size_dest, rotation)

class Sound:
    def __init__(self, url):
        self.url = url
        if CACHE_STORE.has_key(url):
            self.sound = CACHE_STORE[url]
        else:
            self.sound = simplegui.load_sound(url)
            CACHE_STORE[url] = self.sound
    def get_sound(self):
        return self.sound
    def play(self):
        self.sound.play()
    def pause(self):
        self.sound.pause()
    def rewind(self):
        self.sound.rewind()

class Score:
    def __init__(self, lives):
        self.lives = lives
        self.score = 0
        dispatcher.add('draw', self.draw)
    def get_lives(self):
        return self.lives
    def get_score(self):
        return self.score
    def draw(self, draw_event):
        # set the gutter size
        gutter_size = 15
        # set the font style
        font_size = 15
        font_color = 'white'
        # create the text
        lives_text = 'Lives: ' + str(self.get_lives())
        score_text = 'Score: ' + str(self.get_score())
        # calculate text width
        lives_text_width = draw_event.frame.get().get_canvas_textwidth(lives_text, font_size)
        score_text_width = draw_event.frame.get().get_canvas_textwidth(score_text, font_size)
        draw_event.canvas.draw_text(lives_text, (gutter_size, gutter_size + (font_size / 2)), font_size, font_color)
        draw_event.canvas.draw_text(score_text, (draw_event.frame.get_width() - score_text_width - gutter_size, gutter_size + (font_size / 2)), font_size, font_color)

class Game:
    def __init__(self, size):
        """
        Creates a new game window

        <tuple> size
        """
        # sets the window's size
        self.set_window_size(size)
        # creates the Frame
        self.frame = self.create_frame()
        # creates a Timer
        self.timer = self.create_timer()
    def set_window_size(self, size):
        """
        Sets the game window's size
        <tuple> size
        """
        self.window_size = size
    def get_window_size(self):
        """
        Gets the game window's size
        """
        return self.window_size
    def get_size(self):
        """
        Alias of self.get_window_size()
        """
        return self.get_window_size()
    def get_window_width(self):
        return self.get_window_size()[0]
    def get_window_height(self):
        return self.get_window_size()[1]
    def get_center(self):
        """
        Retrieves the center of the window
        """
        return (self.get_window_width() / 2, self.get_window_height() / 2)
    def create_frame(self):
        """
        Creates and returns a new Frame instance and set's the draw handler
        """
        sg_frame = simplegui.create_frame("Game", self.get_window_width(), self.get_window_height())
        # create a new Frame instance
        frame = Frame(sg_frame, self.get_window_size())
        # sets the draw handler
        frame.set_draw_handler(self.draw)
        # sets the mouse click handler
        frame.set_mouseclick_handler(self.onclick)
        # sets the keydown handler
        frame.set_keydown_handler(self.onkeydown)
        # sets the keyup handler
        frame.set_keyup_handler(self.onkeyup)
        # return the Frame instance
        return frame
    def get_frame(self):
        """
        Retrieve the Frame instance
        """
        return self.frame
    def create_timer(self):
        """
        Creates and returns a new Timer instance
        """
        # creates a timer (calls each 25ms)
        timer = Timer(25)
        return timer
    def get_timer(self):
        """
        Returns the Timer instance
        """
        return self.timer
    def start(self):
        """
        Starts the game (opens the game frame)
        """
        # starts timer
        self.get_timer().start()
        # starts frame
        self.get_frame().get().start()
    def draw(self, canvas):
        """
        Draw handler
        """
        # create a DrawEvent
        draw_event = DrawEvent(canvas, self.get_frame())
        dispatcher.run('draw', draw_event)
    def onclick(self, position):
        """
        Mouseclick handler
        """
        click_event = ClickEvent(position)
        dispatcher.run('click', click_event)
    def onkeydown(self, key):
        """
        Keydown handler
        """
        key_event = KeyEvent(key)
        dispatcher.run('keydown', key_event)
    def onkeyup(self, key):
        """
        Keyup handler
        """
        key_event = KeyEvent(key)
        dispatcher.run('keyup', key_event)

class AsteroidsGame(Game):
    def __init__(self, size, lives):
        # calls the parent constructor
        Game.__init__(self, size)
        # create the Background layer
        self.create_background()
        # creates the Player layer
        self.create_player()
        # spawn rocks every second (1000ms)
        self.spawn_rocks_delay = 1000
        self.rocks = []
        # creates a new Score layer
        self.score = self.create_score(lives)
        dispatcher.add('count', self.spawn_rocks)
    def create_background(self):
        # creates the Space layer
        self.space = Space(self.get_size())
        # creates the Debris layer
        self.debris = Debris(self.get_size(), self.get_timer())
    def create_player(self):
        # creates the player spaceship
        self.player = PlayerSpaceship((90, 90), self.get_center())
    def spawn_rocks(self, timer_event):
        if timer_event.time % self.spawn_rocks_delay is 0:
            # create a rock
            rock = self.create_rock()
            # clear list and add new one
            self.rocks = []
            self.rocks.append(rock)
    def create_rock(self):
        # generate a random position
        position = (random.randrange(0, self.get_window_width()), random.randrange(0, self.get_window_height()))
        # generate a random velocity
        velocity = (random.choice([-1, 1]) * random.randint(1, 3), random.choice([-1, 1]) * random.randint(1, 3))
        # generate a random rotation velocity
        rotation_velocity = random.choice([-1, 1]) * random.random() * 0.05
        # generate a random acceleration
        acceleration = random.random() / 5
        # create a new rock
        rock = Rock((90, 90), position, velocity, 0, rotation_velocity)
        rock.set_acceleration(acceleration)
        return rock
    def create_score(self, lives):
        score = Score(lives)
        return score
    def draw(self, canvas):
        # calls parent method
        Game.draw(self, canvas)
        if len(self.rocks):
            for rock in self.rocks:
                draw_event = DrawEvent(canvas, self.get_frame())
                rock.draw(draw_event)

class Space:
    def __init__(self, size):
        """
        Creates the space background image

        <tuple> size        The size of the window
        """
        # sets the size of the background
        self.size = size
        # loads the image
        self.image = Image('https://www.dropbox.com/s/gkz1ng5b5f911tk/nebula_blue.f2014.png?dl=1', (800, 600))
        # registers the draw handler
        dispatcher.add('draw', self.draw)
    def set_size(self, size):
        self.size = size
    def get_size(self):
        return self.size
    def draw(self, draw_event):
        size = self.get_size()
        # calculate the center destination
        center_dest = (size[0] / 2, size[1] / 2)
        # draws the background into the canvas
        self.image.draw_at(draw_event.canvas, center_dest, self.size)

class Debris:
    def __init__(self, size, timer):
        """
        Creates the debris animation

        <tuple> size        The size of the window
        <Timer> timer       The timer instance
        """
        self.size = size
        self.timer = timer
        # loads the image
        self.image = Image('https://www.dropbox.com/s/xcygcu51maw8bam/debris2_blue.png?dl=1', (640, 480))
        dispatcher.add('draw', self.draw)
    def set_size(self, size):
        self.size = size
    def get_size(self):
        return self.size
    def draw(self, draw_event):
        size = self.get_size()
        # calc the center destination
        delta = (self.timer.get_time() / 50) % size[0]
        center_dest1 = (delta - size[0] / 2, size[1] / 2)
        center_dest2 = (delta + size[0] / 2, size[1] / 2)
        # draws the background into the canvas
        self.image.draw_at(draw_event.canvas, center_dest1, size)
        self.image.draw_at(draw_event.canvas, center_dest2, size)

class Sprite:
    def __init__(self, size, position, velocity = (0, 0), rotation = 0, rotation_velocity = 0, lifetime = 0):
        """
        Creates a new movable object. Set the velocity vector
        to make the object move by default.

        <tuple> size                The size of the sprite
        <tuple> position            The position of the sprite
        <tuple> velocity            The velocity of the sprite
        <int> rotation              The rotation/angle of the sprite (in radians)
        <int> rotation_velocity     The rotation/angle of the velocity (in radians)
        <int> lifetime              An integer representing when the item can live in ms
        """
        # sets the initial size
        self.size = size
        # sets the image's center position
        self.set_center((self.size[0] / 2, self.size[1] / 2))
        # sets the initial position
        self.set_position(position)
        # sets the initial velocity
        self.set_velocity(velocity)
        # set the rotation direction flag (enum: None, "left', or "right")
        self.set_rotation_dir(None)
        # set the initial rotation (radians)
        self.set_rotation(rotation)
        # set the initial rotation velocity (radians)
        self.set_rotation_velocity(rotation_velocity)
        # sets the initial acceleration
        self.set_acceleration(0.1)
        # sets the intial friction (small constant)
        self.set_friction(0.02)
        # sets the age/lifetime
        self.age = 0
        self.lifetime = lifetime
        # sets the initial accelerating flag
        self.accelerating = False
    def set_size(self, size):
        self.size = size
    def get_size(self):
        return self.size
    def set_center(self, center):
        self.center = center
    def get_center(self):
        return self.center
    def get_radius(self):
        return self.size[0] / 2
    def set_position(self, position):
        self.position = position
    def get_position(self):
        return self.position
    def set_velocity(self, velocity):
        self.velocity = velocity
    def get_velocity(self):
        return self.velocity
    def set_rotation_dir(self, rotation_dir):
        self.rotation_dir = rotation_dir
    def get_rotation_dir(self):
        return self.rotation_dir
    def set_rotation(self, rotation):
        self.rotation = rotation
    def get_rotation(self):
        return self.rotation
    def set_rotation_velocity(self, rotation_velocity):
        self.rotation_velocity = rotation_velocity
    def get_rotation_velocity(self):
        return self.rotation_velocity
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    def get_acceleration(self):
        return self.acceleration
    def set_friction(self, friction):
        self.friction = friction
    def get_friction(self):
        return self.friction
    def get_forward_vector(self):
        """
        Calculates the forward vector based on the sprite's
        rotation/angle (radians), acceleration, and friction
        """
        rotation = self.get_rotation()
        return (math.cos(rotation), math.sin(rotation))
    def apply_rotation(self, rotation_velocity):
        """
        Given the current rotation (in radians), applies the rotation velocity (in radians)
        """
        new_rotation = self.get_rotation() + rotation_velocity
        self.set_rotation(new_rotation)
    def apply_velocity(self, velocity, screen_bounds):
        """
        Given the current position, applies the specified velocity vector

        <tuple> screen_bounds
        """
        current_pos = self.get_position()
        new_pos = ((current_pos[0] + velocity[0]) % screen_bounds[0], (current_pos[1] + velocity[1]) % screen_bounds[1])
        # sets the new position
        self.set_position(new_pos)
    def apply_forward_vector(self, forward, acceleration):
        """
        Given the current velocity, applies the specified forward vector, and acceleration
        """
        current_vel = self.get_velocity()
        new_vel = (
            current_vel[0] + (forward[0] * acceleration),
            current_vel[1] + (forward[1] * acceleration)
        )
        self.set_velocity(new_vel)
    def apply_friction(self, friction):
        """
        Given the current velocity, applies the specified friction constant
        """
        if friction > 0:
            current_vel = self.get_velocity()
            new_vel = (current_vel[0] * (1 - friction), current_vel[1] * (1 - friction))
            # sets the new velocity
            self.set_velocity(new_vel)
    def is_accelerating(self):
        """
        Returns a boolean indicating if the object is accelerating
        """
        return self.accelerating
    def update(self, draw_event):
        """
        Updates the position of the current sprite based on the the velocity and rotation.
        """
        # applies the rotation velocity to the rotation
        self.apply_rotation(self.get_rotation_velocity())
        # applies the current velocity vector
        self.apply_velocity(self.get_velocity(), draw_event.frame.get_size())
        # if currently accelerating
        if self.is_accelerating():
            # retrieve the forward vector
            forward_vector = self.get_forward_vector()
            # retrieve the accleration
            acceleration = self.get_acceleration()
            # applies the forward vector, and acceleration to the current velocity
            self.apply_forward_vector(forward_vector, acceleration)
        # applies the friction constant
        self.apply_friction(self.get_friction())
    def draw(self, draw_event):
        """
        Draws the spaceship into the canvas
        """
        # increment age
        self.age += 1
        # flag to draw or not
        should_draw = True
        # draw if not yet expired
        if self.lifetime > 0 and self.age > self.lifetime:
            should_draw = False
        if should_draw:
            # updates the positions, and rotations
            self.update(draw_event)
            # draws the spaceship into the canvas
            self.image.draw_at(draw_event.canvas, self.get_position(), self.get_size(), self.get_rotation())

class Rock(Sprite):
    def __init__(self, size, position, velocity = (0, 0), rotation = 0, rotation_velocity = 0):
        """
        Creates a new rock
        """
        # calls parent method
        Sprite.__init__(self, size, position, velocity, rotation, rotation_velocity)
        # clears friction
        self.set_friction(0)
        # loads the image
        self.image = Image('https://www.dropbox.com/s/ackzcnknlaz56f0/asteroid_blue.png?dl=1', self.size, self.center)

class Missle(Sprite):
    def __init__(self, size, position, velocity = (0, 0), rotation = 0, rotation_velocity = 0, lifetime = 100):
        """
        Creates a new missle
        """
        # calls parent method
        Sprite.__init__(self, size, position, velocity, rotation, rotation_velocity, lifetime)
        # clears friction
        self.set_friction(0)
        # loads the image
        self.image = Image('https://www.dropbox.com/s/9fbouyq1q1j2gcj/shot2.png?dl=1', self.size, self.center)
        # loads the sound
        self.sound = Sound('https://www.dropbox.com/s/h0s1tbm70nd8gc1/missile.mp3?dl=1')
        # plays the sound
        self.sound.play()

class Spaceship(Sprite):
    def __init__(self, size, position, velocity = (0, 0), rotation = 0, rotation_velocity = 0):
        # calls parent method
        Sprite.__init__(self, size, position, velocity, rotation, rotation_velocity)
        # load the image
        self.image = Image('https://www.dropbox.com/s/y2oopsybnllxl3c/double_ship.png?dl=1', self.get_size(), self.get_rest_center())
        # load the sound
        self.sound = Sound('https://www.dropbox.com/s/mmk6t1kzsbz4pju/thrust.mp3?dl=1')
        dispatcher.add('draw', self.draw)
    def get_rest_center(self):
        return (45, 45)
    def get_thrust_center(self):
        return (135, 45)
    def rotate(self, direction):
        self.set_rotation_dir(direction)
    def rotate_left(self):
        self.set_rotation(self.get_rotation() - 0.05)
    def rotate_right(self):
        self.set_rotation(self.get_rotation() + 0.05)
    def rotate_end(self):
        self.set_rotation_dir(None)
    def thrust_start(self):
        self.accelerating = True
        self.image.set_center(self.get_thrust_center())
        # play sound
        self.sound.rewind()
        self.sound.play()
    def thrust_stop(self):
        self.accelerating = False
        self.image.set_center(self.get_rest_center())
        # stop sound
        if self.sound:
            self.sound.pause()
    def shoot_start(self):
        size = (10, 10)
        position = self.get_position()
        velocity = self.get_velocity()
        rotation = self.get_rotation()
        radius = self.get_radius()
        forward_vector = self.get_forward_vector()
        # calculate the missle position
        missle_position = (position[0] + (forward_vector[0] * radius), position[1] + (forward_vector[1] * radius))
        # missle acceleration constant
        missle_acceleration = 5
        # calculate the missle velocity
        missle_velocity = (velocity[0] + missle_acceleration * forward_vector[0], velocity[1] + missle_acceleration * forward_vector[1])
        # create a new missle
        missle = Missle(size, missle_position, missle_velocity, rotation, 0)
        # draw missle
        dispatcher.add('draw', missle.draw)
    def update(self, draw_event):
        # if currently rotating
        if self.get_rotation_dir() is "left":
            self.rotate_left()
        elif self.get_rotation_dir() is "right":
            self.rotate_right()
        # calls the parent method
        Sprite.update(self, draw_event)

class PlayerSpaceship(Spaceship):
    def __init__(self, size, position, velocity = (0, 0), rotation = 0, rotation_velocity = 0):
        # calls parent constructor
        Spaceship.__init__(self, size, position, velocity, rotation, rotation_velocity)
        dispatcher.add('keyup', self.onkeyup)
        dispatcher.add('keydown', self.onkeydown)
    def onkeyup(self, key_event):
        if key_event.key is simplegui.KEY_MAP['left']: # left
            # stops rotating
            self.rotate_end()
        elif key_event.key is simplegui.KEY_MAP['right']: # right
            # stops rotating
            self.rotate_end()
        elif key_event.key is simplegui.KEY_MAP['up']: # up
            self.thrust_stop()
    def onkeydown(self, key_event):
        if key_event.key is simplegui.KEY_MAP['left']: # left
            # begins rotating left
            self.rotate('left')
        elif key_event.key is simplegui.KEY_MAP['right']: # right
            # begins rotating right
            self.rotate('right')
        elif key_event.key is simplegui.KEY_MAP['up']: # up
            # begins thrusting
            self.thrust_start()
        elif key_event.key is simplegui.KEY_MAP['space']: # space
            # begins shooting!
            self.shoot_start()



# creates a new dispatcher instance
dispatcher = Dispatcher()

# creates a new game
game = AsteroidsGame(WINDOW_SIZE, NUM_LIVES)
game.start()




# DEBUGGING
class Debugger:
    def __init__(self, game):
        self.game = game
        dispatcher.add('draw', self.draw)
    def draw(self, draw_event):
        # position
        pos = self.game.player.get_position()
        pos_text = "Position: %0.2f, %0.2f" % (pos[0], pos[1])
        pos_text_width = draw_event.frame.get().get_canvas_textwidth(pos_text, 12)
        pos_position = (15, draw_event.frame.get_height() - 15)
        draw_event.canvas.draw_text(pos_text, pos_position, 12, 'white')
        # velocity
        vel = self.game.player.get_velocity()
        vel_text = 'Velocity: %0.2f, %0.2f' % (vel[0], vel[1])
        vel_text_width = draw_event.frame.get().get_canvas_textwidth(vel_text, 12)
        vel_position = (pos_position[0] + pos_text_width + 50, pos_position[1])
        draw_event.canvas.draw_text(vel_text, vel_position, 12, 'white')
        # rotation/angle
        rotation = self.game.player.get_rotation()
        rotation_text = 'Rotation: %0.2f' % rotation
        rotation_text_width = draw_event.frame.get().get_canvas_textwidth(rotation_text, 12)
        rotation_position = (vel_position[0] + vel_text_width + 50, pos_position[1])
        draw_event.canvas.draw_text(rotation_text, rotation_position, 12, 'white')
        # rotation/angle velocity
        rotation_velocity = self.game.player.get_forward_vector()
        rotation_velocity_text = 'Rotation Vector: %0.2f, %0.2f' % (rotation_velocity[0], rotation_velocity[1])
        rotation_velocity_text_width = draw_event.frame.get().get_canvas_textwidth(rotation_velocity_text, 12)
        rotation_velocity_position = (rotation_position[0] + rotation_text_width + 50, pos_position[1])
        draw_event.canvas.draw_text(rotation_velocity_text, rotation_velocity_position, 12, 'white')
        # missle velocity
        forward_vector = self.game.player.get_forward_vector()
        missle_vel = (vel[0] + 5 * forward_vector[0], vel[1] + 5 * forward_vector[1])
        missle_vel_text = 'Missle Velocity: %0.2f, %0.2f' % (missle_vel[0], missle_vel[1])
        missle_vel_text_width = draw_event.frame.get().get_canvas_textwidth(missle_vel_text, 12)
        missle_vel_position = (rotation_velocity_position[0] + rotation_velocity_text_width + 50, pos_position[1])
        draw_event.canvas.draw_text(missle_vel_text, missle_vel_position, 12, 'white')


debugger = Debugger(game)