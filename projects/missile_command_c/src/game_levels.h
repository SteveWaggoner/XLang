#ifndef GAME_LEVELS_H_
#define GAME_LEVELS_H_

#include "c6502.h"
#include "object.h"


#define GAME_ENEMY_BOMB 1
#define GAME_ENEMY_SMARTBOMB 2
#define GAME_ENEMY_PLANE 3
#define GAME_ENEMY_ALIEN 4

#define GAME_OBJECT_MISSILE 5
#define GAME_OBJECT_EXPLOSION 6

#define GAME_COLOR_RED 1


#define GAME_SCORE_EASY 1
#define GAME_COLOR_BLUE 1
#define GAME_SPEED_EASY 1
#define GAME_SEED_A 1
#define GAME_ENEMY_EASY 1


#define GAME_ATTACK_BOMB 1
#define GAME_ATTACK_MULTIBOMB 2



typedef struct tagLevel {
    U8     score_multiplier;
    U8     color;
    U8     speed;
    U8     random_seed;

    Enemy* enemy; 
    U8     enemy_count;
} Level;


extern Level game_levels[];

#endif
