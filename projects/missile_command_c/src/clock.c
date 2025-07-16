
#include "list.h"
#include "utils.h"
#include "clock.h"

#include <stdio.h>
#include <assert.h>



#include "win/win_clock_api.h"
#define CLOCKS_PER_SECOND 60
U32 get_clock() {

    static long long first_clock = 0;
    long long clock = (long long) (CLOCKS_PER_SECOND * get_clock_microseconds_win() / 1000000);

    if (first_clock == 0) {
        first_clock = clock;
    }

    return (U32) (clock - first_clock);
}

void sleep_for(U32 duration) {
    sleep_microseconds_win(1000000 * duration / CLOCKS_PER_SECOND);
}



void wait_until(U32 until_clock) {

    U32 loop_cnt = 0;
    U32 start_clock = get_clock();

    U32 wait_duration = until_clock - start_clock;
    U32 wait_duration_95pct = 100 * wait_duration / 95;

    if (wait_duration_95pct > 0) {
        sleep_for(wait_duration_95pct);
    }

    U32 now_clock = get_clock();
    while (now_clock < until_clock && loop_cnt < 100000) {
        loop_cnt++;
        now_clock = get_clock();
    }
    printf("looped %d times, start=%d now=%d\n", loop_cnt, start_clock, now_clock);

}



void Alarm_set(Alarm* pAlarm, Clock* pClock, U16 alarm_ticks, ALARM_FUNC callback, void* param) {
    assert(pAlarm);
    assert(pClock);
    assert(alarm_ticks>0);
    assert(callback);

    pAlarm->pClock = pClock;
    pAlarm->alarm_ticks = alarm_ticks;
    pAlarm->callback = callback;
    pAlarm->param = param;
}


void Alarm_check(Alarm* pAlarm) {

    assert(pAlarm);

    if ( pAlarm->active == TRUE) {
        assert(pAlarm->pClock);
        if ( pAlarm->alarm_ticks < pAlarm->pClock->ticks ) {
            (*(pAlarm->callback))(pAlarm->param);
           FREE_ITEM(pAlarm);
        }
    }
}


void Clock_init(Clock* pClock) {

    SET_ALL_INACTIVE(Alarm,pClock->alarms);

    pClock->ticks       = 0;
    pClock->loop_start  = get_clock();
    pClock->extra_sleep = 0;

    pClock->frame_cnt   = 0;
    pClock->frame_start = pClock->loop_start;
    pClock->actual_fps  = 0;
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
        sleep_for(sleep_duration);
    }

    double actual_total_duration_in_seconds = (1.0 * actual_total_duration / CLOCKS_PER_SECOND);
    if ( actual_total_duration_in_seconds > 0 ) {
        pClock->actual_fps  = (U16) (1.0 * pClock->frame_cnt / actual_total_duration_in_seconds);
     }

    pClock->ticks++;
    pClock->frame_cnt++;   
}



void Clock_reset(Clock* pClock) {
    pClock->ticks = 0;
    SET_ALL_INACTIVE(Alarm,pClock->alarms);
}

void Clock_set_alarm(Clock* pClock, U16 wait_seconds, ALARM_FUNC callback, void* param) {
    Alarm* pAlarm = ALLOC_ITEM(Alarm, pClock->alarms);
    U16 sleep_until = (U16) (pClock->ticks + (int)(wait_seconds * TICKS_PER_SECOND_16/16));
    Alarm_set(pAlarm, pClock, sleep_until, callback, param);
}

void Clock_check_alarms(Clock* pClock) {
    U16 i;
    Alarm* pAlarm;
    for (i=0; i < LIST_SIZE(Alarm, pClock->alarms); i++) {
        pAlarm = GET_ITEM(Alarm, pClock->alarms, i); 
        Alarm_check(pAlarm);
    }
}






