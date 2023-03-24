import math
from PIL import Image

f = open("log.txt", "w")
class Vec:
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        return Vec(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, v2): # dot product
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def __mul__(self, v2): # cross product 
        return Vec(self.y * v2.z - self.z * v2.y, -(self.x * v2.z - self.z * v2.x), self.x * v2.y - self.y * v2.x)

    def scalar(self, n): # scalar multiplication
        return Vec(self.x * n, self.y * n, self.z * n)

    def __add__(self, v2):
        return Vec(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2):
        return Vec(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __repr__(self):
        return f"Vec({self.x}, {self.y}, {self.z})"

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def normalize(self):
        return Color(self.r / 255, self.g / 255, self.b / 255)

    def denormalize(self):
        return Color(int(self.r * 255), int(self.g * 255), int(self.b * 255))
    
    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"
    
    def __add__(self, c2):
        return Color(min(255, self.r + c2.r), min(255, self.g + c2.g), min(255, self.b + c2.b))

    def __sub__(self, c2):
        return Color(max(0, self.r - c2.r), max(0, self.g - c2.g), max(0, self.b - c2.b))

    def __mul__(self, c2):
        return Color((self.r * c2.r) / 255, (self.g * c2.g) / 255, (self.b * c2.b) / 255)
    
    def __div__(self, c2):
        return Color(self.r / c2.r, self.g / c2.g, self.b / c2.b)


class Ray:

    def __init__(self, origin: Vec, dir: Vec):
        self.origin = origin
        self.dir= dir

class Object:

    def __init__(self, pos: Vec, color):
        self.pos = pos
        self.color = color

    def intersect():
        pass

    def get_normal():
        pass

class Plane(Object):

    def __init__(self, pos: Vec, normal: Vec, color):
        super().__init__(pos, color)
        self.normal = normal
    
    def intersect(self, ray: Ray):
        scalar = self.normal.dot(ray.dir)
        if (scalar < 0):
            return (self.pos - ray.origin).dot(self.normal) / scalar
        else:
            return -1
    
    def get_normal(self, point):
        return self.normal


class Sphere(Object):

    def __init__(self, pos: Vec, radius: float, color):
        super().__init__(pos, color)
        self.radius = radius

    def intersect(self, ray: Ray):
        d = (ray.dir.dot(ray.origin - self.pos))**2 - ((ray.origin - self.pos).magnitude()**2 - self.radius*2)
        if d < 0:
            return -1
        elif d == 0:
            return -(ray.dir.dot(ray.origin - self.pos))
        else:
            return -(ray.dir.dot(ray.origin - self.pos)) - math.sqrt(d)

    def get_normal(self, point):
        print(f"{(point - sphere.pos).normalize()}\t{point}", file=f)
        return (point - sphere.pos).normalize()

class Camera:

    def __init__(self, screen_height, focal_length, origin):
        self.screen_height = screen_height
        self.screen_width = screen_height * ASPECT_RATIO
        self.focal_length = focal_length
        self.origin = origin
        self.horizontal = Vec(self.screen_width,0,0)
        self.vertical = Vec(0,self.screen_height, 0)
        self.lower_left_corner = self.origin - self.horizontal.scalar(0.5) - self.vertical.scalar(0.5) - Vec(0,0,self.focal_length)

class Scene:

    def __init__(self, camera, light, objects=[]):
        self.objects = objects
        self.camera = camera
        self.light = light
    
    def render(self, img):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                u = i / (WIDTH+1)
                v = j / (HEIGHT+1)
                r = Ray(self.camera.origin, (self.camera.lower_left_corner + self.camera.horizontal.scalar(u) + self.camera.vertical.scalar(v) - self.camera.origin).normalize())
                
                closest = None # clostest hit of the ray
                d = float('inf') # distance of the currenlty closest known object
                for o in self.objects:
                    t = o.intersect(r)
                    if t > 0 and t < d:
                        d = t
                        closest = o
                        
                if closest != None:
                    hit = r.dir.scalar(d)
                    normal = closest.get_normal(hit)
                    shadow_ray = Ray(hit, (self.light - hit).normalize())
                    blocked = False
                    for o in self.objects:
                        if o.intersect(shadow_ray) > 0:
                            blocked = True
                            break
                    if not blocked:
                        k = max(0, normal.dot(shadow_ray.dir))
                        img.putpixel((i,HEIGHT-1-j), tuple(int(k * x) for x in closest.color))

    def render_reflection(self, img):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                u = i / (WIDTH+1)
                v = j / (HEIGHT+1)
                r = Ray(self.camera.origin, (self.camera.lower_left_corner + self.camera.horizontal.scalar(u) + self.camera.vertical.scalar(v) - self.camera.origin).normalize())
                
                closest = None # clostest hit of the ray
                d = float('inf') # distance of the currenlty closest known object
                for o in self.objects:
                    t = o.intersect(r)
                    if t > 0 and t < d:
                        d = t
                        closest = o
                        
                if closest != None:
                    hit = r.dir.scalar(d)
                    normal = closest.get_normal(hit)
                    shadow_ray = Ray(hit, (self.light - hit).normalize())
                    blocked = False
                    for o in self.objects:
                        if o.intersect(shadow_ray) > 0:
                            blocked = True
                            break
                    if not blocked:
                        k = max(0, normal.dot(shadow_ray.dir))
                        img.putpixel((i,HEIGHT-1-j), tuple(int(k * x) for x in closest.color))



# image


ASPECT_RATIO = 16 / 9
WIDTH = 800
HEIGHT = int(WIDTH / ASPECT_RATIO)
img = Image.new(mode="RGB", size=(WIDTH, HEIGHT))


# camera
cam = Camera(2.0, 1.0, Vec(0,0,0))

sphere = Sphere(Vec(0, 1, -10), 2, (255, 0, 0))
sphere2 = Sphere(Vec(5, 5, -10), 2, (255, 255, 0))
sphere3 = Sphere(Vec(4, 4, -10), 2, (255, 0, 255))
plane = Plane(Vec(0, -2, 0), Vec(0,1,0), (0, 0, 255))

scene = Scene(
    cam, 
    Vec(0,20,-5), 
    [
        sphere, 
        sphere2, 
        plane
    ]
)

print("starting to render scene...", end="")
scene.render(img)
print("done")

img.save("output.png", format="png")
f.close()