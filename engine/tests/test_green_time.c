#include <assert.h>
#include <stdio.h>
#include "green_time.h"

int main(void)
{
    assert(classify_queue(-1) == -1);
    assert(classify_queue(0) == 1);
    assert(classify_queue(30) == 1);
    assert(classify_queue(30.01) == 2);
    assert(classify_queue(50) == 2);
    assert(classify_queue(70) == 3);
    assert(classify_queue(70.01) == 4);
    assert(calculate_green_time(10) == 15);
    assert(calculate_green_time(40) == 25);
    assert(calculate_green_time(60) == 35);
    assert(calculate_green_time(100) == 45);
    assert(calculate_green_time(-5) == -1);
    assert(green_time_for_zone(1) == 15);
    assert(green_time_for_zone(4) == 45);
    assert(green_time_for_zone(0) == -1);
    assert(green_time_for_zone(5) == -1);
    printf("All green_time tests passed\n");
    return 0;
}
