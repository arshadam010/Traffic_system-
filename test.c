
#include <stdio.h>
#include "signal.h"

int main()
{
    double queue_length;

    printf("Bengaluru SmartSignal\n");
    printf("---------------------\n");

    printf("Enter estimated queue length (metres): ");

    if (scanf("%lf", &queue_length) != 1)
    {
        printf("Invalid input!\n");
        return 1;
    }

    int zone = classify_queue(queue_length);

    if (zone == -1)
    {
        printf("Invalid queue length!\n");
        return 1;
    }

    int green_time = calculate_green_time(queue_length);

    printf("\nQueue length: %.2f metres\n", queue_length);
    printf("Traffic zone: %d\n", zone);
    printf("Recommended green time: %d seconds\n", green_time);

    return 0;
}
