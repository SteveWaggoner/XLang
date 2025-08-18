
#include "object.h"
#include "list.h"
#include "game_board.h"
#include "game_levels.h"

#include "game_objects.h"

#include <assert.h>

void game_object_explode(Object* obj) {
    Object_spawn(&game_board, GAME_OBJECT_EXPLOSION, &obj->movement.position, 0, 0);
    obj->active = 0;
}

void game_object_inactive(Object* obj) {
    obj->active = 0;
}

AnimationFrame game_animation_plane[] = {
    {set_object_radius, 3, 2},
    {set_object_radius, 6, 2},
    {set_object_radius, 9, 2},
    {set_object_radius, 6, 2}
};

AnimationFrame game_animation_explosion[] = {
    {set_object_radius, 6},
    {set_object_radius, 10},
    {set_object_radius, 20},
    {set_object_radius, 18},
    {set_object_radius, 20},
    {set_object_radius, 18},
    {set_object_radius, 14},
    {set_object_radius, 8},
    {set_object_radius, 4},
    {set_object_inactive}
};

void Enemy_spawn(Game_Board* board, Enemy* enemy) {
    Object* enemy_obj = 0;
    switch (enemy->type) {
    case GAME_ENEMY_BOMB:
    {
        enemy_obj = ALLOC_ITEM(Object, board->bomb);
        break;
    }
    case GAME_ENEMY_SMARTBOMB:
    {
        enemy_obj = ALLOC_ITEM(Object, board->smartbomb);
        break;
    }
    case GAME_ENEMY_PLANE:
    {
        enemy_obj = ALLOC_ITEM(Object, board->plane);
        enemy_obj->animation.frame = game_animation_plane;
        enemy_obj->animation.frame_count = LIST_SIZE(AnimationFrame, game_animation_plane);
        enemy_obj->animation.frame_index = 0;
        enemy_obj->animation.sleep = 0;
        break;
    }
    case GAME_ENEMY_ALIEN:
    {
        enemy_obj = ALLOC_ITEM(Object, board->alien);
        break;
    }

    }
    assert(enemy_obj);
    set_enemy_object(enemy_obj, enemy);
}

void Object_spawn(Game_Board* board, U8 type, Vec2* start, Vec2* destination, U8 speed) {
    Object* obj = 0;
    switch (type) {
    case GAME_OBJECT_MISSILE:
    {
        obj = ALLOC_ITEM(Object, board->missile);
        break;
    }
    case GAME_OBJECT_EXPLOSION:
    {
        obj = ALLOC_ITEM(Object, board->explosion);
        assert(obj);
        obj->animation.frame = game_animation_explosion;
        obj->animation.frame_count = LIST_SIZE(AnimationFrame, game_animation_explosion);
        obj->animation.frame_index = 0;
        obj->animation.sleep = 0;        
        break;
    }

    }

    assert(obj);

    obj->movement.position = *start;
    if (destination) {
        obj->movement.destination = *destination;
        obj->movement.pixels_per_tick = speed;
        update_vectors(&obj->movement);
    }
    else {
        zero_vec2(&obj->movement.velocity);
    }

        
}


void set_object_radius(struct tagObject* obj, struct tagAnimationFrame* frame) {
    obj->shape.radius = frame->param;
}
void set_object_inactive(struct tagObject* obj, struct tagAnimationFrame* frame) {
    obj->active = 0;
}


