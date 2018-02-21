//This file was generated from UPPAAL 4.0.2 (rev. 2491), August 2006

/*

*/
E<> sats[0].memory >= HIGH_MEMORY

/*

*/
E<> t_time < 1000 && priorities[0][0] == jobs[0].prio * 2

/*

*/
E<> orbit_time[0] >= 30 && runnable[0] && runnable[1]

/*

*/
E<> Processor(0).Block

/*

*/
E<> t_time >= SCHEDULE_LENGHT && sats[0].memory >= 50

/*

*/
E<> t_time >= SCHEDULE_LENGHT
