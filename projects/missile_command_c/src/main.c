
#include <stdio.h>

#include "graphics_api.h"

#include "shape.h"
#include "clock.h"

void main() {

	printf("Hello, World!\n");

	SHAPE_CANVAS arrCanvas;
	arrCanvas.point_cnt = 0;
	arrCanvas.max_point_cnt = MAX_POINTS;

	App_init("Missile Command", APP_MODE_VGA);


	Canvas* canvas = App_canvas();
	Canvas_set_color(canvas, 0xFF0490EE, CANVAS_MODE_NORMAL);

	Rect rect = { 0,0,10,10 };
	Canvas_filled_rect(canvas, &rect, 0xFF556677);

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


		printf(".");
		sleep_for_duration(1);
	}



	Shape_line(3, 4, 8, 9, putPixelInArray, &arrCanvas);
	printf("done\n");

}