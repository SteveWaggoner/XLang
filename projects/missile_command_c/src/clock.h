#ifndef CLOCK_H_
#define CLOCK_H_

#include "list.h"

struct tagClock;
typedef void (*ALARM_FUNC)(void* param);

typedef struct tagAlarm {
    Item       item;
    struct tagClock* pClock;
    U16        alarm_ticks;
    ALARM_FUNC callback;
    void* param;
} Alarm;


void Alarm_dump(Alarm* pAlarm);

typedef struct tagAlarmList {
    List list;
    Alarm alarm[6];
} AlarmList;

typedef struct tagClock {
    List      list;
    AlarmList alarms;

    U32 ticks;
    U32 loop_start;
    U16 extra_sleep;
    U16 frame_cnt;
    U32 frame_start;
    U16 actual_fps;

} Clock;

/*

CLOCK = clock time duration
TICK  = game logic update
FRAME = video update

in the case of 6502:
CLOCK = 1/60 of a second
*/



#include "win/win_clock_api.h"
#define CLOCKS_PER_SECOND 60

U32  get_clock();
void sleep_for_duration(U32 duration);
void wait_until(U32 until_clock);


#define CLOCKS_PER_TICK_16   (1 * 16)  // tie the ticks with system clock to keep it simple
#define TICKS_PER_FRAME       1        // video should match game logic to keep it simple

#define TICKS_PER_SECOND_16  (16 * 16 * CLOCKS_PER_SECOND / CLOCKS_PER_TICK_16)

// expected rates
#define FRAMES_PER_SECOND_16 (TICKS_PER_SECOND_16 / TICKS_PER_FRAME)
#define CLOCKS_PER_FRAME_16 (16 * 16 * CLOCKS_PER_SECOND / FRAMES_PER_SECOND_16)


void Alarm_init(Alarm* pAlarm, Clock* pClock, U16 alarm_ticks, ALARM_FUNC callback, void* param);
void Alarm_check(Alarm* pAlarm);

void Clock_init(Clock* pClock);
void Clock_dump(Clock* pClock);
void Clock_tick(Clock* pClock);
void Clock_reset(Clock* pClock);
void Clock_set_alarm(Clock* pClock, U16 wait_seconds, ALARM_FUNC callback, void* param);
void Clock_check_alarms(Clock* pClock);

#endif