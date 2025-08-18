
#include <stdio.h>
#include <assert.h>

#include "graphics_api.h"

#include "shape.h"
#include "clock.h"
#include "list.h"
#include "utils.h"

#include "object.h"



int main() {

	Object objects[5] = { { 0 } };

	Vec2 start_pos = { 50, 51 };
	Vec2 end_pos = { 50, 50 };

	Vec2	vel = { 0,0 };
	calculate_velocity(&start_pos, &end_pos, 1, &vel);
//	printf("start=%p, end=%p, vel=%s", &start_pos, &end_pos, 1);

	Vec2 vel2 = { 0,0 };	
	calculate_velocity(&start_pos, &end_pos, 2, &vel2);
//	printf("start={start_pos}, end={end_pos}, vel={vel2}");

	Vec2 vel3 = { 0,0 };
	calculate_velocity(&start_pos, &end_pos, 3, &vel3);
//	printf("start={start_pos}, end={end_pos}, vel={vel3}");
}


void print_func(void* param) {
	printf("%s\n", (U8*)param);
}


int qmain() {

	printf("fps=%d\n", FRAMES_PER_SECOND_16 / 16);
	printf("tps=%d\n", TICKS_PER_SECOND_16 / 16);
	printf("jps=%d\n", CLOCKS_PER_SECOND);
	printf("jpf=%f\n", 1.0 * CLOCKS_PER_FRAME_16 / 16);

	// return 0;

	Clock myclock;
	Clock_init(&myclock);

	Clock_set_alarm(&myclock, 4, print_func, "Hello");
	Clock_set_alarm(&myclock, 6, print_func, "World");
	Clock_set_alarm(&myclock, 10, print_func, "How");
	Clock_set_alarm(&myclock, 20, print_func, "are");
	Clock_set_alarm(&myclock, 21, print_func, "you?");


	while (myclock.ticks < 30 * 60) {

		Clock_tick(&myclock);
		Clock_check_alarms(&myclock);

		if (random_byte() > 180) {
			sleep_for(2);
		}

	}

	printf("Done. clock.ticks=%d\n", myclock.ticks);
	return 0;
}

typedef struct Foo {
	BOOLEAN active;
	U8 blah;
	U16 blah2;
} Foo;

void lmain() {
	Foo fooList[6] = {0};

	Foo* foo = ALLOC_ITEM(Foo, fooList);
	Foo* foo2 = ALLOC_ITEM(Foo, fooList);
	Foo* foo3 = ALLOC_ITEM(Foo, fooList);

	FREE_ITEM(foo2);

	Foo* foo4 = ALLOC_ITEM(Foo, fooList);

	void* unknownList = fooList;
	Foo* foo2b = GET_ITEM(Foo, unknownList, 1);

	SET_ALL_INACTIVE(Foo, unknownList); // <--doesn't work
	SET_ALL_INACTIVE(Foo, fooList);

	List_setAll(unknownList, sizeof(Foo), 6, TRUE);


	assert(foo);
	printf("foo -> %d\n", foo->blah);



}


void xmain() {
	
	Clock clock = { 0 };
	
	Clock_init(&clock);
	

	printf("Hello, World!\n");


	App_init("Missile Command", APP_MODE_VGA);

	/*
	Canvas* canvas = App_canvas();
	Canvas_set_color(canvas, 0xFF0490EE, CANVAS_MODE_NORMAL);
	*/
	Rect rect = { 0,0,10,10 };
	//Canvas_filled_rect(canvas, &rect, 0xFF556677);

	/*
	Canvas_draw_line(canvas, -1, 67, 199, 100);
	Canvas_draw_filled_octogon(canvas,-1, 100, 40, 3, 8);
	Canvas_set_color(canvas, 0xFF84A0EE, CANVAS_MODE_NORMAL);
	Canvas_draw_filled_circle(canvas, -1, 80, 25);
	Canvas_draw_circle(canvas, -1, 170, 15);
	Canvas_set_color(canvas, 0xFF84A000, CANVAS_MODE_XOR);
	Canvas_draw_text(canvas, 0, 0, "1234567890123456789012345678901234567890xx");
	*/
	
	/*
	Sprite* ball = App_sprite(24, 21);
	Canvas_set_color(ball->canvas, 0xFF00EE22, CANVAS_MODE_NORMAL);
	Canvas_draw_filled_circle(ball->canvas, 12, 10, 9);

	ball->x = 10;
	ball->y = 10;
*/
	/*
	while (ball->x < 300) {
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
		Clock_tick(&clock);
	}
	*/

	//printf("done fps=%f\n", clock.actual_fps);

}