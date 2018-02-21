//This file was generated from UPPAAL 4.0.2 (rev. 2491), August 2006

/*

*/
//E<> sats[0].memory >= HIGH_MEMORY

/*

*/
//E<> orbit_time[0] >= 30 && runnable[0] && runnable[1]

/*

*/
//E<> Processor(0).Block

/*

*/
//E<> t_time >= SCHEDULE_LENGHT && sats[0].memory >= 50

/*

*/
E<> t_time == 75 && runs[1][0] > 0

/*

*/
//E<> sats[1].suggested_task == 0

/*

*/
//E<> Processor(1).Occupied && Processor(1).task == 0

/*

*/
//E<> sats[1].memory > LOW_MEMORY-10

/*

*/
//E<> t_time >= SCHEDULE_LENGHT
