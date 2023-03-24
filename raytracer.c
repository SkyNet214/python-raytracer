#include <stdlib.h>
#include <math.h>

typedef struct Vec3 {
    float x;
    float y;
    float z;
} Vec;

typedef struct Ray {
    Vec origin;
    Vec dir;
} Ray;

typedef struct Plane {
    Vec pos;
    Vec normal;
} Plane;

typedef struct Sphere {
    Vec center;
    float radius;
} Sphere;


float magnitude(Vec v) {
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

Vec normalize(Vec v) {
    float mag = magnitude(v);
    Vec r = {v.x / mag, v.y / mag, v.z / mag};
    return r;
}

float dot(Vec a, Vec b) {
    return (a.x * b.x + a.y * b.y + a.z * b.z); 
}

Vec scalar(Vec v, float k) {
    Vec r = {v.x * k, v.y * k, v.z * k};
    return r;
}

Vec add(Vec a, Vec b) {
    Vec r = {a.x + b.x, a.y + b.y, a.z + b.z};
    return r;
}

Vec sub(Vec a, Vec b) {
    Vec r = {a.x - b.x, a.y - b.y, a.z - b.z};
    return r;
}

void print_vec(Vec v) {
    printf("Vec(%f, %f, %f)\n", v.x, v.y, v.z);
}

float intersect_plane(Plane p, Ray r) {
    float scalar = dot(p.normal, r.dir);
    if (scalar >= 0) {
        return dot((sub(p.pos,r.origin)), p.normal) / scalar;
    } else {
        return 0;
    }
}

float intersect_sphere(Sphere s, Ray r) {
    float d = pow(dot(r.dir, sub(r.origin, s.center)), 2) - (pow(magnitude(sub(r.origin, s.center)), 2) - pow(s.radius, 2));
    if (d < 0){
        return -1;
    } else if (d == 0) {
        return dot(r.dir, sub(r.origin, s.center));
    } else {
        return dot(r.dir, sub(r.origin, s.center)) - sqrt(d);
    } 
}


