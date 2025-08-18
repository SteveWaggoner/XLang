#include <windows.h>

#include "win_clock_api.h"

LARGE_INTEGER
get1970Offset()
{
    SYSTEMTIME s = { 0 };
    FILETIME f;
    LARGE_INTEGER t = { 0 };

    s.wYear = 1970;
    s.wMonth = 1;
    s.wDay = 1;
    s.wHour = 0;
    s.wMinute = 0;
    s.wSecond = 0;
    s.wMilliseconds = 0;
    SystemTimeToFileTime(&s, &f);
    t.QuadPart = f.dwHighDateTime;
    t.QuadPart <<= 32;
    t.QuadPart |= f.dwLowDateTime;
    return (t);
}

double get_clock_microseconds_win()
{
    LARGE_INTEGER         t = { 0 };
    FILETIME              f;
    double                microseconds;

    static int            initialized = 0;
    static LARGE_INTEGER  offset;
    static double         frequencyToMicroseconds;

    if (!initialized) {
        initialized = 1;      
        offset = get1970Offset();
        frequencyToMicroseconds = 10.;
    }

    GetSystemTimeAsFileTime(&f);
    t.QuadPart = f.dwHighDateTime;
    t.QuadPart <<= 32;
    t.QuadPart |= f.dwLowDateTime;

    t.QuadPart -= offset.QuadPart;
    microseconds = (double)t.QuadPart / frequencyToMicroseconds;
    return microseconds;
}

void sleep_for_microseconds_win(long microseconds) {
    int dwMilliseconds = microseconds / 1000; // Duration of the delay in milliseconds
    SleepEx(dwMilliseconds, 0);
}