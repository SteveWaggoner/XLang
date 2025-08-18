
#include "game_levels.h"

#include "list.h"




Enemy game_enemy_easy[] = { 
        //type, launch_time, start, destination, speed, attack_times, attack_types, route
        {GAME_ENEMY_SMARTBOMB, 1, {180,0}, {255,180}, 25 },
        {GAME_ENEMY_ALIEN,     3, {0,110}, {0,0}, 25, {5,10}, {GAME_ATTACK_BOMB}, {{50,90},{100,50},{150,90},{320,50}} },

        {GAME_ENEMY_PLANE,     5, {320,90}, {0,90}, 25, {3,4,32,90,92,120,121}, {GAME_ATTACK_BOMB,GAME_ATTACK_MULTIBOMB}, {{50,90},{100,50},{150,90},{320,50}} },

        {GAME_ENEMY_BOMB,      10, {10,0},  {55, 200}, 15 },
        {GAME_ENEMY_BOMB,      12, {50,0},  {150,200}, 15 },
        {GAME_ENEMY_BOMB,      16, {70,0},  {230,200}, 15 },
        {GAME_ENEMY_BOMB,      19, {210,0}, {255,200}, 15 }
    };


Level game_levels[] = {
    //score_multiplier, color, speed, randomseed, enemy_list, enemy_list_count
    { GAME_SCORE_EASY, GAME_COLOR_BLUE, GAME_SPEED_EASY, GAME_SEED_A, game_enemy_easy, LIST_SIZE(Enemy,game_enemy_easy)},
    { GAME_SCORE_EASY, GAME_COLOR_BLUE, GAME_SPEED_EASY, GAME_SEED_A },
    { GAME_SCORE_EASY, GAME_COLOR_BLUE, GAME_SPEED_EASY, GAME_SEED_A },
    { GAME_SCORE_EASY, GAME_COLOR_BLUE, GAME_SPEED_EASY, GAME_SEED_A }
};

