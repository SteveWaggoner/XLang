
#include "list.h"

#include <stdio.h>
#include <assert.h>

struct tagClock;
typedef void (*ALARM_FUNC)(VOID_PTR param);

typedef struct tagAlarm {
    Item       item;
    struct tagClock* pClock;
    U16        alarm_ticks;
    ALARM_FUNC callback;
    VOID_PTR   param;
} Alarm;


void Alarm_dump(Alarm* pAlarm) {
    assert(pAlarm);
    printf(" pAlarm = %p\n", pAlarm);
    printf(" pAlarm->item.active = %d\n", pAlarm->item.active);
    printf(" pAlarm->alarm_ticks = %d\n", pAlarm->alarm_ticks);
}

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
U32 get_clock() {

    static long long first_clock = 0;
    long long clock = CLOCKS_PER_SECOND * get_clock_microseconds_win() / 1000000;

    if (first_clock == 0) {
        first_clock = clock;
    }

    return clock - first_clock;
}

void sleep_for_duration(U32 duration) {
    return sleep_microseconds_win(1000000 * duration / CLOCKS_PER_SECOND);
}


#define CLOCKS_PER_TICK_16   (1 * 16)  // tie the ticks with system clock to keep it simple
#define TICKS_PER_FRAME       1        // video should match game logic to keep it simple

#define TICKS_PER_SECOND_16  (16 * 16 * CLOCKS_PER_SECOND / CLOCKS_PER_TICK_16)

// expected rates
#define FRAMES_PER_SECOND_16 (TICKS_PER_SECOND_16 / TICKS_PER_FRAME)
#define CLOCKS_PER_FRAME_16 (16 * 16 * CLOCKS_PER_SECOND / FRAMES_PER_SECOND_16)


void wait_until(U32 until_clock) {

    U32 loop_cnt = 0;
    U32 start_clock = get_clock();

    U32 wait_duration = until_clock - start_clock;
    U32 wait_duration_95pct = 100 * wait_duration / 95;

    if (wait_duration_95pct > 0) {
        sleep_for_duration(wait_duration_95pct);
    }

    U32 now_clock = get_clock();
    while (now_clock < until_clock && loop_cnt < 100000) {
        loop_cnt++;
        now_clock = get_clock();
    }
    printf("looped %d times, start=%d now=%d\n", loop_cnt, start_clock, now_clock);

}

//#endif


void Alarm_init(Alarm* pAlarm, Clock* pClock, U16 alarm_ticks, ALARM_FUNC callback, VOID_PTR param) {
    assert(pAlarm);
    assert(pClock);
    assert(alarm_ticks>0);
    assert(callback);

    Item_init(&pAlarm->item);

    pAlarm->pClock = pClock;
    pAlarm->alarm_ticks = alarm_ticks;
    pAlarm->callback = callback;
    pAlarm->param = param;

    printf("Alarm_init %d\n", alarm_ticks);
    Alarm_dump(pAlarm);
}


void Alarm_check(Alarm* pAlarm) {

    assert(pAlarm);

    if ( pAlarm->item.active == TRUE) {
        assert(pAlarm->pClock);
        if ( pAlarm->alarm_ticks < pAlarm->pClock->ticks ) {
            (*(pAlarm->callback))(pAlarm->param);
            FREE_ITEM(Alarm,pAlarm);
        }
    }
}


void Clock_init(Clock* pClock) {

    INIT_LIST(Alarm,pClock->alarms,FALSE);

    pClock->ticks       = 0;
    pClock->loop_start  = get_clock();
    pClock->extra_sleep = 0;

    pClock->frame_cnt   = 0;
    pClock->frame_start = pClock->loop_start;
    pClock->actual_fps  = 0;
}


void Clock_dump(Clock* pClock) {
    List_dump((List*)& pClock->alarms, (ITEM_DUMP_FUNC) Alarm_dump);
    printf("loop_start = %d\n", pClock->loop_start);
}


void Clock_tick(Clock* pClock) {

    U32 actual_total_duration;
    U32 expected_total_duration;
    I32 sleep_duration;

    U32 now_clock = get_clock(); 

    actual_total_duration = (now_clock - pClock->frame_start);
    expected_total_duration = pClock->frame_cnt * CLOCKS_PER_FRAME_16/16;
    sleep_duration = expected_total_duration - actual_total_duration;
   
     if ( sleep_duration > 0 ) {
        sleep_for_duration(sleep_duration);
    }

    double actual_total_duration_in_seconds = (1.0 * actual_total_duration / CLOCKS_PER_SECOND);
    if ( actual_total_duration_in_seconds > 0 ) {
        pClock->actual_fps  = 1.0 * pClock->frame_cnt / actual_total_duration_in_seconds;
     }

    pClock->ticks++;
    pClock->frame_cnt++;   
}



void Clock_reset(Clock* pClock) {
    pClock->ticks = 0;
    CLEAR_LIST(Alarm,pClock->alarms);
}

void Clock_set_alarm(Clock* pClock, U16 wait_seconds, ALARM_FUNC callback, VOID_PTR param) {
    Alarm* pAlarm = ALLOC_ITEM(Alarm, pClock->alarms);
    U16 sleep_until = pClock->ticks + (int)(wait_seconds * TICKS_PER_SECOND_16/16);
    Alarm_init(pAlarm, pClock, sleep_until, callback, param);
    pAlarm->item.active = TRUE;
}

void Clock_check_alarms(Clock* pClock) {
    int i;
    Alarm* pAlarm;
    for (i=0; i < pClock->alarms.list.max_items; i++) {
        pAlarm = List_getItem(&pClock->alarms, i);
        Alarm_check(pAlarm);
    }

}


void print_func(VOID_PTR msg) {
    printf("%s\n", (char*)msg);
}



int clk_main() {

    printf("fps=%d\n", FRAMES_PER_SECOND_16/16);
    printf("tps=%d\n", TICKS_PER_SECOND_16/16);
    printf("jps=%d\n", CLOCKS_PER_SECOND);
    printf("jpf=%f\n", 1.0 * CLOCKS_PER_FRAME_16 / 16);

   // return 0;

    Clock myclock;
    Clock_init(&myclock);

    Clock_dump(&myclock);

    Clock_set_alarm(&myclock, 4, print_func, "Hello");
    Clock_set_alarm(&myclock, 6, print_func, "World");
    Clock_set_alarm(&myclock, 10, print_func, "How");
    Clock_set_alarm(&myclock, 20, print_func, "are");
    Clock_set_alarm(&myclock, 21, print_func, "you?");

    DUMP_LIST(Alarm, myclock.alarms);
    printf("clock = %d\n", clock());

    while (myclock.ticks < 30*60) {

    //    printf(" myclock.ticks = %d\n", myclock.ticks);

        Clock_tick(&myclock);
        Clock_check_alarms(&myclock);

        if ( random_byte() > 180 ) {
            sleep_for_duration(2);
        }


        /*
        if (myclock.ticks % 40 == 0 ) {
            myclock.frame_start = get_clock();
            myclock.frame_cnt = 0;
        }
        */
    }
    printf("clock = %d\n", clock());

    printf("Done. clock.ticks=%d\n", myclock.ticks);
}

