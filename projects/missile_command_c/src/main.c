
#include <stdio.h>

#include "graphics_api.h"

#include "shape.h"
#include "clock.h"

void main() {

	printf("Hello, World!\n");


	App_init("Missile Command", APP_MODE_VGA);


	Canvas* canvas = App_canvas();
	Canvas_set_color(canvas, 0xFF0490EE, CANVAS_MODE_NORMAL);

	Rect rect = { 0,0,10,10 };
	Canvas_filled_rect(canvas, &rect, 0xFF556677);


	Canvas_draw_line(canvas, -1, 67, 199, 100);
	Canvas_draw_filled_octogon(canvas,-1, 100, 40, 3, 8);
	Canvas_set_color(canvas, 0xFF84A0EE, CANVAS_MODE_NORMAL);
	Canvas_draw_filled_circle(canvas, -1, 80, 25);
	Canvas_draw_circle(canvas, -1, 170, 15);
	Canvas_set_color(canvas, 0xFF84A000, CANVAS_MODE_XOR);
	Canvas_draw_text(canvas, 0, 0, "1234567890123456789012345678901234567890xx");

	Sprite* ball = App_sprite(24, 21);
	Canvas_set_color(ball->canvas, 0xFF00EE22, CANVAS_MODE_NORMAL);
	Canvas_draw_filled_circle(ball->canvas, 12, 10, 9);


//	Canvas_draw_image(canvas, ball->canvas, 160, 160);

	ball->x = 10;
	ball->y = 10;


	while (1) {
		App_finish_draw();
		App_poll_events();
		I16 key = App_check_key();
		if (key) {
			printf("key = %d\n", key);
		}
		MouseClick* mouse = App_check_mouse();
		if (mouse) {
			Canvas_draw_pixel(canvas, mouse->x, mouse->y);
		}

		ball->x++;
		ball->y++;


		printf(".");
		sleep_for_duration(1);
	}

	printf("done\n");

}