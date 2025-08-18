#ifndef GAME_BOARD_H_
#define GAME_BOARD_H_

#include "clock.h"
#include "c6502.h"
#include "object.h"

typedef struct tag_Game_Board {

    Clock clock;

    BOOLEAN game_over;
    BOOLEAN level_over;
    BOOLEAN switching_to_next_level;
    U16     enemy_index;
    U16     level_index;

    U32 score;
    U32 next_city_score;
    U8 extra_cities;

    Object missile[15];
    Object bomb[25];
    Object smartbomb[4];
    Object plane[4];
    Object alien[4];
    Object explosion[15];

    Object land[1];
    Object city[6];
    Object battery[3];
    U8     battery_index;

} Game_Board;

extern Game_Board game_board;

#define GAME_OBJECT_EXPLODED 1


void Game_Board_init(Game_Board* board);
void Game_Board_load_level(Game_Board* board, int level_index);
BOOLEAN Game_Board_launch_missile(Game_Board* board, I16 dest_x, I16 dest_y);

void Game_Board_spawn_enemies(Game_Board* board);
BOOLEAN Game_Board_has_more_enemies_in_flight(Game_Board* board);
BOOLEAN Game_Board_has_clock_alarms(Game_Board* board);
Object* Game_Board_get_random_target(Game_Board* board, Vec2* retPos, U8 off);
void Game_Board_create_explosion(Game_Board* board, Vec2* pos);
void Game_Board_bomb_random_target(Game_Board* board, Object* attacker, U8 off);
void Game_Board_create_attack(Game_Board* board, Object* plane, U8 attack_type);
void Game_Board_score_level(Game_Board* board);
void Game_Board_move_item(Game_Board* board, Object* items, U8 item_count, U8 enable_attack, U8 enable_explode, U8 enable_dodge);
void Game_Board_move_items(Game_Board* board);
void Game_Board_explode_enemy(Game_Board* board, Object* enemy_list, U8 enemy_count, U8 score_points);
void Game_Board_explode_enemies(Game_Board* board);
void Game_Board_explode_friendly(Game_Board* board, Object* bomb_list, U8 bomb_count, Object* friendly_list, U8 friendly_count);
void Game_Board_explode_friendlies(Game_Board* board);
BOOLEAN Game_Board_has_more_enemies_to_launch(Game_Board* board);
BOOLEAN Game_Board_is_level_active(Game_Board* board);
void Game_Board_check_if_level_over(Game_Board* board);
void Game_Board_check_if_game_over(Game_Board* board);
void Game_Board_next_level(Game_Board* board);
void Game_Board_action(Game_Board* board);









#endif
