import math
from PIL import Image

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

    def scalar(self, n):
        return Vec(self.x * n, self.y * n, self.z * n)

    def __add__(self, v2):
        return Vec(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2):
        return Vec(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __repr__(self):
        return f"Vec({self.x}, {self.y}, {self.z})"


class Ray:

    def __init__(self, origin: Vec, dir: Vec):
        self.origin = origin
        self.dir= dir


class Plane:

    def __init__(self, pos: Vec, normal: Vec):
        self.pos = pos
        self.normal = normal
    
    def intersect(self, ray: Ray):
        scalar = self.normal.dot(ray.dir)
        if (scalar > 0):
            return (self.pos- ray.origin).dot(self.normal) / scalar
        else:
            return 0


class Sphere:

    def __init__(self, center: Vec, radius: float):
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray):
        d = (ray.dir.dot(ray.origin - self.center))**2 - ((ray.origin - self.center).magnitude()**2 - self.radius*2)
        if d < 0:
            return -1
        elif d == 0:
            return -(ray.dir.dot(ray.origin - self.center))
        else:
            return -(ray.dir.dot(ray.origin - self.center)) - math.sqrt(d)

# image

ASPECT_RATIO = 16 / 9
WIDTH = 800
HEIGHT = int(WIDTH / ASPECT_RATIO)
img = Image.new(mode="RGB", size=(WIDTH, HEIGHT))


# camera

screen_height = 2.0
screen_width = screen_height * ASPECT_RATIO
focal_length = 1

origin = Vec(0,1,0)
horizontal = Vec(screen_width,0,0)
vertical = Vec(0,screen_height,0)
lower_left_corner = origin - horizontal.scalar(0.5) - vertical.scalar(0.5) - Vec(0,0,focal_length)

# rendering

sphere = Sphere(Vec(0, 1,-10), 2)
plane = Plane(Vec(0, 0, 0), Vec(0,1,0))
light = Vec(5,10,0)

print("starting...\n")

for j in range(HEIGHT-1, -1, -1):
    for i in range(0, WIDTH):
        u = i / (WIDTH - 1)
        v = j / (HEIGHT - 1)
        r = Ray(origin, (lower_left_corner + horizontal.scalar(u) + vertical.scalar(v) - origin).normalize())

        d = sphere.intersect(r)
        if d > 0:
            hit = r.dir.scalar(d)
            k = (hit - sphere.center).normalize().dot((hit - light).normalize())
            if k > 0:
                img.putpixel((i, j), (int(255 * k), int(255 * k), int(255 * k)))
            else:
                img.putpixel((i, j), (0, 0, 0))
        elif -plane.intersect(r) > 0:
            hit = r.dir.scalar(-plane.intersect(r))
            r = Ray(hit, (hit - light).normalize())
            if sphere.intersect(r) > 0:
                img.putpixel((i, j), (0, 0, 0))
            else:
                img.putpixel((i,j), (0,0,255))
            
        

print("done")

img.save("output.png", format="png")