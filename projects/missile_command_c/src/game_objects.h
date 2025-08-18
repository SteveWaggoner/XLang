#ifndef GAME_OBJECTS_H_
#define GAME_OBJECTS_H_

#include "object.h"
#include "game_board.h"

void game_object_explode(Object* obj);
void game_object_inactive(Object* obj);

void Enemy_spawn(Game_Board* board, Enemy* enemy);
void Object_spawn(Game_Board* board, U8 type, Vec2* start, Vec2* destination);

#endif