
#include <stdio.h>

#include "graphics_api.h"

#include "shape.h"

void main() {

	printf("Hello, World!\n");

	SHAPE_CANVAS arrCanvas;
	arrCanvas.point_cnt = 0;
	arrCanvas.max_point_cnt = MAX_POINTS;



	Shape_line(3, 4, 8, 9, putPixelInArray, &arrCanvas);
	printf("done\n");

}