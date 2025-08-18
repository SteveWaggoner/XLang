#include "object.h"
#include "clock.h"

#include <math.h>
#include <assert.h>
#include <stdio.h>

#define MAX(A,B)  A > B ? A : B;
#define ABS(A) A < 0 ? (-A) : A


float manhattan_distance(Vec2* p1, Vec2* p2) {
    return ABS(p1->x - p2->x) + ABS(p1->y - p2->y);
}
float chebyshev_distance(Vec2* p1, Vec2* p2) {
    return MAX(ABS(p1->x - p2->x), ABS(p1->y - p2->y));
}
float true_distance(Vec2* p1, Vec2* p2) {
    return (float) sqrt(((p1->x - p2->x) * (p1->x - p2->x)) + ((p1->y - p2->y) * (p1->y - p2->y)));
}

float distance(Vec2* p1, Vec2* p2) {
//    return manhattan_distance(p1, p2);
    return true_distance(p1, p2);
}

void calculate_velocity(Vec2* p1, Vec2* p2, float pixels_per_tick, Vec2* outVel) {

    float rough_distance_in_pixels = distance(p1, p2);

    float delta_x = (p2->x - p1->x);
    float delta_y = (p2->y - p1->y);

    float ticks_until_dest = rough_distance_in_pixels / pixels_per_tick;

    if (pixels_per_tick == 0 || ticks_until_dest==0) {
        printf("cannot calculate velocity\n");
        outVel->x = 0;
        outVel->y = 0;
        return;
    }

    float delta_x_per_tick = (delta_x / ticks_until_dest);
    float delta_y_per_tick = (delta_y / ticks_until_dest);

    outVel->x = delta_x_per_tick;
    outVel->y = delta_y_per_tick;
}


//
// for object collision detection
//
BOOLEAN circle_hit(Shape* circle1, Shape* circle2) {
    U16 diff_x = abs(circle1->x - circle2->x);
    if (diff_x < circle1->radius + circle2->radius) {
        U16 diff_y = abs(circle1->y - circle2->y);
        if (diff_y < circle1->radius + circle2->radius) {
            return TRUE;
        }
    }
    return FALSE;
}

BOOLEAN point_in_rectangle(Vec2* pnt, Shape* rect) {
    if (pnt->x > rect->x && pnt->y > rect->y) {
        if (pnt->x < rect->x + rect->width && pnt->y < rect->y + rect->height) {
            return TRUE;
        }
    }
    return FALSE;
}

void update_vectors(Object* obj) {
    assert(obj);
    calculate_velocity(&obj->movement.position, &obj->movement.destination, obj->movement.pixels_per_tick, &obj->movement.velocity);
}


void set_enemy_object(Object* enemy_obj, Enemy* enemy) {
    enemy_obj->enemy = enemy;
    enemy_obj->movement.position = enemy->start;
    enemy_obj->route_index = 0;

    enemy_obj->movement.move_cnt = 0;
}

void set_shape(Shape* shape, I16 x, I16 y, I16 width, I16 height) {
    shape->x = x;
    shape->y = y;
    shape->width = width;
    shape->height = height;
}



/*
void set_object_position(MovingObject* obj, Vec2* start, Vec2* dest, float speed, U16 width, U16 height) {

    //
    // for object motion
    //
    obj->position = *start;
    obj->width = width;
    obj->height = height;

    if (dest) {
        obj->destination = *dest;
        obj->pixels_per_tick = (speed / TICKS_PER_SECOND);  // speed is converted from pixels_per_second to pixels_per_tick
        update_vectors(obj);
    }

    //debug
    obj->move_cnt = 0;
    obj->distance = 0;
    obj->last_distance = 0;
}
*/
//
// for object targeting
//
void get_target_position(Shape* shape, Vec2* retPos) {
    // get center mass of object ("pos" is anchor top upper corner for rectangles so more to center bottom)
    if (shape->width > 0) {
        retPos->x = shape->x + (1.0f * shape->width / 2);
        retPos->y = shape->y + (1.0f * shape->height / 2);
    }
    else {
        retPos->x = shape->x;
        retPos->y = shape->y;
    }
}


void animate_object_tick(Object* obj) {
    Animation* animation = &obj->animation;
    if (animation->sleep > 0) {
        animation->sleep--;
    }
    else {
        // loop so immediately run next action if zero duration
        while (animation->sleep == 0) {

            assert(animation->frame_index < animation->frame_count);

            AnimationFrame* frame = &animation->frame[animation->frame_index];
            (*frame->animate_func)(obj, frame);
            animation->frame_index = (animation->frame_index + 1) % animation->frame_count;
            animation->sleep = frame->ticks_until;
        }

    }

}

void zero_vec2(Vec2* v) {
    v->x = 0;
    v->y = 0;
}

/*
void animate_set_radius(struct tagObject* obj, struct tagAnimationFrame* frame) {
    obj->radius = frame->param;
}

void animate_destroy(struct tagObject* obj, struct tagAnimationFrame* frame) {
    obj->active = FALSE;
}
*/


void Object_move(Object* obj) {
    assert(obj);
    obj->movement.move_cnt += 1;
    obj->movement.position.x += obj->movement.velocity.x;
    obj->movement.position.y += obj->movement.velocity.y;
    obj->movement.last_distance = obj->movement.distance;
    obj->movement.distance = distance(&obj->movement.position, &obj->movement.destination);
}

