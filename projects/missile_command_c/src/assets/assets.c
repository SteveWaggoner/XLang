#include "assets.h"

const unsigned char game_sprites__plane_right_width = 18;
const unsigned char game_sprites__plane_right_height = 11;
const unsigned char game_sprites__plane_right_centerx = 8;
const unsigned char game_sprites__plane_right_centery = 4;
const unsigned char game_sprites__plane_right_pixels_len = 198;
const unsigned char game_sprites__plane_right_palette[4] = {0, 1, 2, 3};
const unsigned char game_sprites__plane_right_pixels[198] = {0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
const unsigned char game_sprites__plane_right_palette_len = 4;

const unsigned char game_sprites__plane_left_width = 18;
const unsigned char game_sprites__plane_left_height = 11;
const unsigned char game_sprites__plane_left_centerx = 9;
const unsigned char game_sprites__plane_left_centery = 4;
const unsigned char game_sprites__plane_left_pixels_len = 198;
const unsigned char game_sprites__plane_left_palette[4] = {0, 3, 2, 1};
const unsigned char game_sprites__plane_left_pixels[198] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 1, 2, 3, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 0};
const unsigned char game_sprites__plane_left_palette_len = 4;

const unsigned char game_sprites__alien_width = 14;
const unsigned char game_sprites__alien_height = 13;
const unsigned char game_sprites__alien_centerx = 7;
const unsigned char game_sprites__alien_centery = 6;
const unsigned char game_sprites__alien_pixels_len = 182;
const unsigned char game_sprites__alien_palette[7] = {1, 4, 0, 3, 2, 5, 6};
const unsigned char game_sprites__alien_pixels[182] = {0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 2, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 0, 3, 2, 2, 2, 0, 3, 2, 0, 4, 4, 3, 2, 0, 3, 2, 2, 2, 2, 2, 0, 4, 4, 4, 4, 4, 4, 3, 2, 2, 2, 2, 2, 2, 0, 4, 4, 4, 4, 4, 4, 3, 2, 2, 2, 2, 2, 0, 3, 5, 6, 4, 3, 5, 6, 4, 3, 2, 2, 2, 2, 0, 3, 5, 6, 4, 3, 5, 6, 4, 3, 2, 2, 2, 2, 0, 3, 5, 6, 4, 3, 5, 6, 4, 3, 2, 2, 2, 2, 2, 0, 4, 4, 4, 4, 4, 4, 3, 2, 2, 2, 2, 2, 2, 0, 4, 4, 4, 4, 4, 4, 3, 2, 2, 2, 2, 2, 0, 3, 2, 0, 4, 4, 3, 2, 0, 3, 2, 2, 2, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 0, 3, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1};
const unsigned char game_sprites__alien_palette_len = 7;

const unsigned long game_sprites__global_palette[7] = {0, 0xff000000, 0xff0717ff, 0xff0001fd, 0xff00a6ff, 0xffad0000, 0xffd50c05};
const unsigned char game_sprites__global_palette_len = 7;
