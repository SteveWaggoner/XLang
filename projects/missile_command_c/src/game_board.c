
#include "game_board.h"
#include "game_levels.h"
#include "game_objects.h"


#include "clock.h"
#include "c6502.h"
#include "object.h"
#include "list.h"
#include "utils.h"

Game_Board game_board;

void Game_Board_init(Game_Board* board) {

    SET_ALL_ACTIVE(Object, board->city);
    I16 city_x[] = { 46,78,108,172,210,246 };
    U8 i;
    for (i = 0;i < 6; i++) {
        set_shape(&board->city[i].shape, city_x[i], 180, 20, 5);
    }

    //setup the batteries
    SET_ALL_ACTIVE(Object, board->battery);
    I16 battery_x[] = { 12,140,280 };
    for (i = 0;i < 3; i++) {
        set_shape(&board->battery[i].shape, battery_x[i], 176, 28, 10);
    }

    //setup the land
    SET_ALL_ACTIVE(Object, board->land);
    set_shape(&board->land[0].shape, 0, 185, 320, 15);
}



void Game_Board_load_level(Game_Board* board, int level_index) {

    //setup the batteries
    U8 i;
    for (i = 0;i < 3; i++) {
        board->battery[i].param = 10; //10 missiles
    }
    board->battery_index = 1;

    //remove moveable object
    SET_ALL_INACTIVE(Object, board->missile);
    SET_ALL_INACTIVE(Object, board->bomb);
    SET_ALL_INACTIVE(Object, board->smartbomb);
    SET_ALL_INACTIVE(Object, board->plane);
    SET_ALL_INACTIVE(Object, board->alien);
    SET_ALL_INACTIVE(Object, board->explosion);

    // reset the level
    Clock_reset(&board->clock);

    board->enemy_index = 0;
    board->level_index = level_index;

    Level* level = &game_levels[level_index];

    //#level has deterministic actions by enemy
    random_byte(&level->random_seed);
}

BOOLEAN Game_Board_launch_missile(Game_Board* board, I16 dest_x, I16 dest_y) {
    Object* battery = & board->battery[board->battery_index];
    if (battery->shape.y < dest_y) {
        return 0;
    }
    //num_missiles
    if (battery->param < 1) {
        return 0;
    }

    Vec2 start = { (float) battery->shape.x + (battery->shape.width/2), (float) battery->shape.y };
    Vec2 destination = { dest_x, dest_y };
    Object_spawn(board, GAME_OBJECT_MISSILE, &start, &destination);

    battery->param--; //num_missiles
    return 1;
}


void Game_Board_spawn_enemies(Game_Board* board) {

    Level* level = &game_levels[board->level_index];
    if (board->enemy_index < level->enemy_count) {
        Enemy* enemy = &level->enemy[board->enemy_index];
        if (enemy->launch_time < board->clock.ticks) {
            Enemy_spawn(board, enemy);
            board->enemy_index++;
        }
    }
}

BOOLEAN Game_Board_has_more_enemies_in_flight(Game_Board* board) {
    return ANY_ACTIVE(Object, board->missile) 
        || ANY_ACTIVE(Object, board->explosion) 
        || ANY_ACTIVE(Object, board->bomb) 
        || ANY_ACTIVE(Object, board->plane) 
        || ANY_ACTIVE(Object, board->alien) 
        || ANY_ACTIVE(Object, board->smartbomb);
}

BOOLEAN Game_Board_has_clock_alarms(Game_Board* board) {
    return ANY_ACTIVE(Alarm, board->clock.alarms);
}

Object* Game_Board_get_random_target(Game_Board* board, Vec2* retPos, U8 off) {
    U8* targets[32] = { 0 };
    U8 battery_cnt = GET_ACTIVE(Object, board->battery, &targets[0]);
    U8 city_cnt = GET_ACTIVE(Object, board->city, &targets[battery_cnt]);

    U8 choice = random_number(battery_cnt + city_cnt);
    Object* obj = (Object*)targets[choice];

    if (obj && retPos) {
        get_target_position(&obj->shape, retPos);
        retPos->x += off; //so we don't random pick the exact same coord (make sure each bomb is visible and not obscured)
        retPos->y += off;
    }
    return obj;
}

void Game_Board_create_explosion(Game_Board* board, Vec2* pos) {
    Object_spawn(board, GAME_OBJECT_EXPLOSION, pos, 0);
}

void Game_Board_bomb_random_target(Game_Board* board, Object* attacker, U8 off) {
    Vec2 target = { 0 };
    Game_Board_get_random_target(board, &target, off);
    Object_spawn(board, GAME_ENEMY_BOMB, &attacker->movement.position, &target);
}

void Game_Board_create_attack(Game_Board* board, Object* plane, U8 attack_type) {
    switch (attack_type) {
    case GAME_ATTACK_BOMB:
    {
        Game_Board_bomb_random_target(board, plane, 0);
        break;
    }
    case GAME_ATTACK_MULTIBOMB:
    {
        U8 i;
        for (i = 0; i < 3; i++) {
            Game_Board_bomb_random_target(board, plane, i);
        }
        break;
    }
    }
}

void Game_Board_score_level(Game_Board* board) {
    U8 i;
    // 5 points per unused missile
    for (i = 0; i < LIST_SIZE(Object, board->battery); i++) {
        Object* battery = & board->battery[i];
        board->score += (5 * battery->param);
    }
    // 100 points per saved city
    for (i = 0; i < LIST_SIZE(Object, board->city); i++) {
        Object* city = &board->city[i];
        if (!city->param) {
            board->score += 100;
        }
    }
    while (board->score >= board->next_city_score) {
        board->extra_cities += 1;
        board->next_city_score += 10000;
    }
}

/*
void Game_Board_dodge_nearby_explosions(Game_Board* board, MovingObject* enemy) {

    for (int i = 0; i < LIST_SIZE(board->explosion); i++) {
        MovingObject* explosion = &board->explosion[i];
        if (explosion->active) {
            if (distance(explosion->movement.position) < 90 && enemy->last_dodge + 5 < board->clock.ticks) {
                enemy->last_dodge = board->clock.ticks;
                if (enemy->route) {
                    enemy->route.insert(
                }

            }

        }
    }
}
*/


void Game_Board_move_item(Game_Board* board, Object* items, U8 item_count, U8 enable_attack, U8 enable_explode, U8 enable_dodge) {

    for (int i = 0; i < item_count; i++) {
        Object* item = &items[i];
        if (item->active) {
            Object_move(item);

            if (enable_attack) {
                U8 attack_type = Enemy_get_attack_type(board, item);
                Game_Board_create_attack(board, item, attack_type);
            }

            BOOLEAN at_dest = item->movement.distance < 50 && item->movement.last_distance != -1 && item->movement.distance > item->movement.last_distance;
            if (at_dest) {

                Enemy_goto_next_destination(item);

                if (enable_explode) {
                    Game_Board_create_explosion(board, &item->movement.position);
                    item->active = 0;
                }
            }
            if (enable_dodge) {
                Game_Board_dodge_nearby_explosions(board, item);
            }
        }
    }
}
 
void Game_Board_move_items(Game_Board* board) {
    Game_Board_move_item(board, board->bomb, LIST_SIZE(Object,board->bomb), 0, 0, 0);
    Game_Board_move_item(board, board->smartbomb, LIST_SIZE(Object, board->smartbomb), 0, 0, 1);
    Game_Board_move_item(board, board->plane, LIST_SIZE(Object, board->plane), 1, 0, 0);
    Game_Board_move_item(board, board->alien, LIST_SIZE(Object, board->alien), 1, 0, 0);
    Game_Board_move_item(board, board->missile, LIST_SIZE(Object, board->missile), 0, 1, 0);
}

void Game_Board_explode_enemy(Game_Board* board, Object* enemy_list, U8 enemy_count, U8 score_points) {

    for (int i = 0; i < LIST_SIZE(Object, board->explosion); i++) {
        Object* explosion = &board->explosion[i];
        if (explosion->active) {
            for (int j = 0; j < enemy_count; j++) {
                Object* enemy = & enemy_list[j];
                if (enemy->active) {

                    if (circle_hit(explosion->shape, enemy->shape)) {
                        board->score += score_points;
                        enemy->active = 0;
                        if (enemy->on_event) {
                            (*enemy->on_event)(enemy, GAME_OBJECT_EXPLODED);
                        }
                    }
                }
            }
        }
    }
}

void Game_Board_explode_enemies(Game_Board* board) {
    Game_Board_explode_enemy(board, board->bomb, LIST_SIZE(Object, board->bomb), 25);
    Game_Board_explode_enemy(board, board->plane, LIST_SIZE(Object, board->plane), 100);
    Game_Board_explode_enemy(board, board->alien, LIST_SIZE(Object, board->alien), 100);
    Game_Board_explode_enemy(board, board->smartbomb, LIST_SIZE(Object, board->smartbomb), 125);
}


void Game_Board_explode_friendly(Game_Board* board, Object* bomb_list, U8 bomb_count, Object* friendly_list, U8 friendly_count) {
    for (int i = 0; i < bomb_count;i++) {
        Object* bomb = &bomb_list[i];
        if (bomb->active) {
            for (int j = 0; j < friendly_count; j++) {
                Object* friendly = &friendly_list[j];
                if (friendly->active) {

                    if (point_in_rectangle(bomb->shape, friendly->shape)) {
                        bomb->active = 0;
                        friendly->active = 0;

                        if (friendly->on_event) {
                            (*friendly->on_event)(friendly, GAME_OBJECT_EXPLODED);
                        }
                    }
                }
            }

        }
    }
}

void Game_Board_explode_friendlies(Game_Board* board) {
    Game_Board_explode_friendly(board, board->bomb, LIST_SIZE(Object, board->bomb), board->city, LIST_SIZE(Object, board->city));
    Game_Board_explode_friendly(board, board->smartbomb, LIST_SIZE(Object, board->smartbomb), board->city, LIST_SIZE(Object, board->city));
}

BOOLEAN Game_Board_has_more_enemies_to_launch(Game_Board* board) {
    Level* level = &game_levels[board->level_index];
    return level->enemy[level->enemy_count - 1].launch_time > board->clock.ticks;
}



BOOLEAN Game_Board_is_level_active(Game_Board* board) {
    return Game_Board_has_more_enemies_to_launch(board) || Game_Board_has_more_enemies_in_flight(board);
}


void Game_Board_check_if_level_over(Game_Board* board) {
    if (board->game_over == FALSE) {
        if (Game_Board_is_level_active(board)) {
            sleep_for(2);
            Game_Board_score_level(board);
            sleep_for(2);
            Game_Board_next_level(board);
            sleep_for(2);
        }
    }
}

void Game_Board_check_if_game_over(Game_Board* board) {
    U8 valid_cities = 0;
    for (int i = 0; i < LIST_SIZE(Object, board->city); i++) {
        if (board->city[i].active) {
            valid_cities+=1;
        }
    }
    if (valid_cities == 0) {
        board->game_over = TRUE;
    }
}

void Game_Board_next_level(Game_Board* board) {
    board->level_index+=1;
}

void Game_Board_action(Game_Board* board) {

    Game_Board_check_if_level_over(board);
    Game_Board_check_if_game_over(board);

    Game_Board_spawn_enemies(board);
    Game_Board_move_items(board);
    Game_Board_explode_enemies(board);
    Game_Board_explode_friendlies(board);

    Clock_tick(&board->clock);
    Clock_check_alarms(&board->clock);
}
