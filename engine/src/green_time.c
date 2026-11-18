#include "green_time.h"

int classify_queue(double queue_length)
{
    if (queue_length < 0)
    {
        return -1;
    }

    if (queue_length <= 30)
    {
        return 1;
    }
    else if (queue_length <= 50)
    {
        return 2;
    }
    else if (queue_length <= 70)
    {
        return 3;
    }
    else
    {
        return 4;
    }
}

int green_time_for_zone(int zone)
{
    switch (zone)
    {
        case 1:
            return 15;
        case 2:
            return 25;
        case 3:
            return 35;
        case 4:
            return 45;
        default:
            return -1;
    }
}

int calculate_green_time(double queue_length)
{
    return green_time_for_zone(classify_queue(queue_length));
}
