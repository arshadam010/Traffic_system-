
#ifndef GREEN_TIME_H
#define GREEN_TIME_H

int classify_queue(double queue_length);

int calculate_green_time(double queue_length);

/* Green seconds for zone 1-4 (-1 if the zone is invalid). */
int green_time_for_zone(int zone);

#endif
