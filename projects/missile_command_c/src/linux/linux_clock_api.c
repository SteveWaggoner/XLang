
#include "linux_clock_api.h"

#ifdef __GNUC

long linux_clock_microseconds()
{
    static long g_first_s = 0;

    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);

    long microseconds = (spec.tv_sec * 1000000) + (spec.tv_nsec / 1000);  // Convert nanoseconds to microseconds 

    if (g_first_s == 0) {
        g_first_s = microseconds;
    }
    microseconds -= g_first_s;

    return microseconds;
}


// https://stackoverflow.com/questions/1157209/is-there-an-alternative-sleep-function-in-c-to-milliseconds 
#include <errno.h>    

void linux_sleep_microseconds(U32 microseconds)
{
    struct timespec ts;
    int res;

    ts.tv_sec = microseconds / 1000000;
    ts.tv_nsec = (microseconds % 1000000) * 1000;

    do {
        res = nanosleep(&ts, &ts);
    } while (res && errno == EINTR);

}

#endif
