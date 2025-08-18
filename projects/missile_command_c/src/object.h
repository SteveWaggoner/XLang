#ifndef OBJECT_H_
#define OBJECT_H_

#include "c6502.h"

typedef struct tagVec2 {
	float x;
	float y;
} Vec2;

void zero_vec2(Vec2* v);


struct tagObject;
struct tagAnimationFrame;
typedef void (*ANIMATE_FUNC)(struct tagObject* object, struct tagAnimationFrame* frame);
typedef void (*OBJECT_FUNC)(struct tagObject* object, U8 event_id);

typedef struct tagAnimationFrame {
    ANIMATE_FUNC animate_func;
    U16 param;
    U16 ticks_until;
} AnimationFrame;


void set_object_radius(struct tagObject* obj, struct tagAnimationFrame* frame);
void set_object_inactive(struct tagObject* obj, struct tagAnimationFrame* frame);


typedef struct tagEnemy {
    U8    type;
    U16   launch_time;
    Vec2  start;
    Vec2  destination;
    U8    speed;

    U8   attack_times[8]; 
    U8   attack_types[4];  
    Vec2 route[8];        
} Enemy;

typedef struct tagShape {
    I16  x;
    I16  y;
    U8   width;
    U8   height;
    U8   radius;  // if non-zero, then circle
} Shape;

typedef struct tagAnimation {
    AnimationFrame* frame;
    U8 frame_count;
    U8 frame_index;
    U16 sleep;
} Animation;

typedef struct tagMovement {

    float pixels_per_tick;

    Vec2 position;
    Vec2 velocity;
    Vec2 destination;

    BOOLEAN destroy_at_destination;

    //debug
    U16 move_cnt;
    float distance;
    float last_distance;

} Movement;

typedef struct tagObject {
    BOOLEAN     active;

    Shape       shape;
    Animation   animation;
    U8          param;       //object specific value (e.g., battery ammo count)
    OBJECT_FUNC on_event;

    Movement  movement;
    Enemy*    enemy;
    U8        route_index;
} Object;


void set_shape(Shape* shape, I16 x, I16 y, I16 width, I16 height);
//void set_moving_object_position(Object* obj, Vec2* start, Vec2* dest, float speed, U16 width, U16 height)
void calculate_velocity(Vec2* p1, Vec2* p2, float pixels_per_tick, Vec2* outVel);

void set_enemy_object(Object* enemy_obj, Enemy* enemy);
void get_target_position(Shape* shape, Vec2* retPos);

void Object_move(Object* obj);

#endif
