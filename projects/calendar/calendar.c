// C program to print the month by month 
// calendar for the given year 

#include <stdio.h> 

#define BYTE unsigned char
#define WORD unsigned short

extern BYTE _dayNumberFast(BYTE day, BYTE month, WORD year);

/*
// Function that returns the index of the 
// day for date DD/MM/YYYY 
BYTE dayNumber(BYTE day, BYTE month, WORD year) 
{ 

    static BYTE t[] = { 0, 3, 2, 5, 0, 3, 
                    5, 1, 4, 6, 2, 4 }; 
    year -= month < 3; 
    return (year + year / 4 
            - year / 100 
            + year / 400 
            + t[month - 1] + day) 
        % 7; 
} 
*/

/*
BYTE dayNumberC(BYTE day, BYTE month, WORD year)
{
    static WORD tmp = 0;
    static BYTE t[] = { 0, 3, 2, 5, 0, 3, 
                        5, 1, 4, 6, 2, 4 }; 
    printf("day=%d\n", day);
    printf("month=%d\n", month);
    printf("year=%d\n", year);
    printf("dmy=%d/%d/%d\n", day, month, year);

    year -= month < 3;

    tmp = year;
    tmp = tmp + year / 4;
    tmp = tmp - year / 100;
    tmp = tmp + year / 400;
    tmp = tmp + t[month - 1];
    tmp = tmp + day;

    return tmp % 7;
}
*/

// Function that returns the name of the 
// month for the given month Number 
// January - 0, February - 1 and so on 
char* getMonthName(int monthNumber) 
{ 
    char* month; 

    switch (monthNumber) { 
    case 0: 
        month = "January"; 
        break; 
    case 1: 
        month = "February"; 
        break; 
    case 2: 
        month = "March"; 
        break; 
    case 3: 
        month = "April"; 
        break; 
    case 4: 
        month = "May"; 
        break; 
    case 5: 
        month = "June"; 
        break; 
    case 6: 
        month = "July"; 
        break; 
    case 7: 
        month = "August"; 
        break; 
    case 8: 
        month = "September"; 
        break; 
    case 9: 
        month = "October"; 
        break; 
    case 10: 
        month = "November"; 
        break; 
    case 11: 
        month = "December"; 
        break; 
    default:
        month = "Invalid"; // Warning: Improper usage of function can lead to undefined behavior.
        break;

    } 
    return month; 
} 

// Function to return the number of days 
// in a month 
int numberOfDays(int monthNumber, int year) 
{ 
    // January 
    if (monthNumber == 0) 
        return (31); 

    // February 
    if (monthNumber == 1) { 
        // If the year is leap then Feb 
        // has 29 days 
        if (year % 400 == 0 
            || (year % 4 == 0 
                && year % 100 != 0)) 
            return (29); 
        else
            return (28); 
    } 

    // March 
    if (monthNumber == 2) 
        return (31); 

    // April 
    if (monthNumber == 3) 
        return (30); 

    // May 
    if (monthNumber == 4) 
        return (31); 

    // June 
    if (monthNumber == 5) 
        return (30); 

    // July 
    if (monthNumber == 6) 
        return (31); 

    // August 
    if (monthNumber == 7) 
        return (31); 

    // September 
    if (monthNumber == 8) 
        return (30); 

    // October 
    if (monthNumber == 9) 
        return (31); 

    // November 
    if (monthNumber == 10) 
        return (30); 

    // December 
    if (monthNumber == 11) 
        return (31);
} 

// Function to print the calendar of 
// the given year 
void printCalendar(int year) 
{
    int i, k, j, days, current;
    printf("     Calendar - %d\n\n", year); 

    // Index of the day from 0 to 6 
    current = _dayNumberFast(1, 1, year); 

    // i for Iterate through months 
    // j for Iterate through days 
    // of the month - i 
    for (i = 0; i < 2; i++) { 
        days = numberOfDays(i, year); 

        // Print the current month name 
        printf("\n ------------%s-------------\n", 
            getMonthName(i)); 

        // Print the columns 
        printf(" Sun Mon Tue Wed Thu Fri Sat\n"); 

        // Print appropriate spaces 
        for (k = 0; k < current; k++) 
            printf("     "); 

        for (j = 1; j <= days; j++) { 
            printf("%5d", j); 

            if (++k > 6) { 
                k = 0; 
                printf("\n"); 
            } 
        } 

        if (k) 
            printf("\n"); 

        current = k; 
    } 

    return; 
} 

