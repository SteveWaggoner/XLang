#ifndef WIN_CLOCK_API_H_
#define WIN_CLOCK_API_H_

#define CLOCKS_PER_SECOND 60

double get_clock_microseconds_win();
void sleep_for_microseconds_win(long microseconds);

#endif
