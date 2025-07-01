
#include "list.h"


#include <stdio.h>
#include <assert.h>

struct tagClock;
typedef void (*ALARM_FUNC)(VOID_PTR param);

typedef struct {
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

typedef struct {
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
 
JIFFY = clock time duration 
TICK  = game logic update
FRAME = video update

in the case of 6502:
JIFFY = 1/60 of a second
*/


//PAL mode
//#define JIFFIES_PER_SECOND    50             // hard-coded 60 to keep it simple (e.g., 6502)
//#define JIFFIES_PER_TICK_16  (16 * 50 / 60)  // tie the ticks with system clock to keep it simple

#define JIFFIES_PER_SECOND    60       // hard-coded 60 to keep it simple (e.g., 6502)
#define JIFFIES_PER_TICK_16  (16 * 1)  // tie the ticks with system clock to keep it simple
#define TICKS_PER_FRAME       1        // video should match game logic to keep it simple

#define TICKS_PER_SECOND_16  (16 * 16 * JIFFIES_PER_SECOND / JIFFIES_PER_TICK_16)
// expected rates
#define FRAMES_PER_SECOND_16 (TICKS_PER_SECOND_16 / TICKS_PER_FRAME)
#define JIFFIES_PER_FRAME_16 (16 * 16 * JIFFIES_PER_SECOND / FRAMES_PER_SECOND_16)


#include <time.h>

//#ifdef __GNUC

typedef unsigned long JTIME;
JTIME Clock_now() {

    static double g_first_s = 0.0;

    long            ms; /* Milliseconds */
    time_t          s;  /* Seconds */
    struct timespec spec;

    clock_gettime(CLOCK_REALTIME, &spec);

    s  = spec.tv_sec;
    ms = spec.tv_nsec / 1000000; /* Convert nanoseconds to milliseconds */
    if (ms > 999) {
        s++;
        ms = 0;
    }

    double seconds = (1.0 * s ) + (1.0 * ms / 1000);

    //make jiffies start at zero
    if ( g_first_s == 0.0 ) {
        g_first_s = seconds;
    }
    seconds -= g_first_s;

    JTIME  jiffies = (int)(seconds * JIFFIES_PER_SECOND);

//    printf("  ====Clock_now====\n");
//    printf("  now seconds = %f\n", seconds);
//    printf("  now jiffies = %d\n", jiffies);
//    printf("  ========\n");

    return jiffies;
}

/* https://stackoverflow.com/questions/1157209/is-there-an-alternative-sleep-function-in-c-to-milliseconds */
#include <errno.h>    

void Clock_sleep(U32 jiffy_duration)
{
    struct timespec ts;
    int res;

    ts.tv_sec = jiffy_duration / JIFFIES_PER_SECOND;
    ts.tv_nsec = (jiffy_duration % JIFFIES_PER_SECOND) * 1000000000 / JIFFIES_PER_SECOND;

    printf("nanosleeping %d jiffies\n", (int) jiffy_duration);
    do {
        res = nanosleep(&ts, &ts);
    } while (res && errno == EINTR);

}

void Clock_wait_until(JTIME until_jiffy_time) {
   
    U32   loop_cnt = 0;
    JTIME start = Clock_now();

    U32   wait_duration = until_jiffy_time - start;
    U32   wait_duration_95pct = 100 * wait_duration / 95;

    if ( wait_duration_95pct > 0) {
        Clock_sleep(wait_duration_95pct);
    }

    JTIME now = Clock_now();
    while ( now < until_jiffy_time && loop_cnt < 100000) {
        loop_cnt++;
        now = Clock_now();
    }
    printf("looped %d times, start=%d now=%d\n", loop_cnt, start, now);

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

//    printf("Alarm_check %p\n", pAlarm);
//    Alarm_dump(pAlarm);

    if ( pAlarm->item.active == TRUE) {
        assert(pAlarm->pClock);

  //      printf("  %d < %d \n", pAlarm->alarm_ticks, pAlarm->pClock->ticks);
        if ( pAlarm->alarm_ticks < pAlarm->pClock->ticks ) {
  //          printf("alarm !!!!\n");
            (*(pAlarm->callback))(pAlarm->param);
            FREE_ITEM(Alarm,pAlarm);
        }
    }
}


void Clock_init(Clock* pClock) {

    printf("&pClock->alarms = %p\n", &pClock->alarms);

    INIT_LIST(Alarm,pClock->alarms,FALSE);

    pClock->ticks       = 0;
    pClock->loop_start  = Clock_now();
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

    printf("======START TICK=====\n");
    U32 actual_total_duration;
    U32 expected_total_duration;
    I32 sleep_duration;

    JTIME now = Clock_now(); 

    printf("pClock->ticks       = %d\n", pClock->ticks);
    printf("pClock->loop_start  = %d\n", pClock->loop_start);
    printf("pClock->extra_sleep = %d\n", pClock->extra_sleep);
    printf("pClock->frame_cnt   = %d\n", pClock->frame_cnt);

    printf("expected FPS        = %d\n", FRAMES_PER_SECOND_16/16);
    printf("pClock->actual_fps  = %d\n", pClock->actual_fps);
    
    actual_total_duration = (now - pClock->frame_start);
    expected_total_duration = pClock->frame_cnt * JIFFIES_PER_FRAME_16/16;
    sleep_duration = expected_total_duration - actual_total_duration;
   
    printf("actual_total_duration   = %d\n", actual_total_duration);
    printf("expected_total_duration = %d\n", expected_total_duration);
    printf("sleep_duration          = %d\n", sleep_duration);

    if ( sleep_duration > 0 ) {
        Clock_sleep(sleep_duration);
    }

    double actual_total_duration_in_seconds = (1.0 * actual_total_duration / JIFFIES_PER_SECOND);
    if ( actual_total_duration_in_seconds > 0 ) {
        pClock->actual_fps  = 1.0 * pClock->frame_cnt / actual_total_duration_in_seconds;
        printf("pClock->frame_cnt          = %d\n", pClock->frame_cnt);
        printf("actual_total_duration      = %d\n", actual_total_duration);
        printf("actual_total_duration_secs = %f\n", actual_total_duration_in_seconds);
        printf("pClock->actual_fps         = %d\n", pClock->actual_fps);
    }

    pClock->ticks++;
    pClock->frame_cnt++;   


    //Clock_sleep(1); 

    printf("======END TICK=======\n");
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


  //  printf("Clock_set_alarm\n");
  //  Alarm_dump(pAlarm);
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

// https://github.com/edrosten/8bit_rng/blob/master/rng-4261412736.c
unsigned char x=1, y=0, z=0, a=1;
unsigned char random_byte() {

	unsigned char t = x ^ (x << 4);
	x=y;
	y=z;
	z=a;
	a = z ^ t ^ ( z >> 1) ^ (t << 1);
    return a;
}

int main() {

    printf("fps=%d\n", FRAMES_PER_SECOND_16/16);
    printf("tps=%d\n", TICKS_PER_SECOND_16/16);
    printf("jps=%d\n", JIFFIES_PER_SECOND);
    printf("jpf=%f\n", 1.0 * JIFFIES_PER_FRAME_16 / 16);

    return 0;

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
        Clock_tick(&myclock);
        Clock_check_alarms(&myclock);

        if ( random_byte() > 180 ) {
            Clock_sleep(2);
        }



        if (myclock.ticks % 40 == 0 ) {
            myclock.frame_start = Clock_now();
            myclock.frame_cnt = 0;
        }
    }
    printf("clock = %d\n", clock());

    printf("Done. clock.ticks=%d\n", myclock.ticks);

}

