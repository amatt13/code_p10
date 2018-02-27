//This file was generated from (Commercial) UPPAAL 4.0.14 (rev. 5615), May 2014

/*

*/
E<> Processor(0).exe_time == 1 && Processor(0).Occupied && Processor(0).task == 2 && !Processor(1).Occupied 

/*

*/
E<>  runs[0][2] > runs[1][3] && !Processor(1).Occupied

/*

*/
E<>  runs[1][2] > runs[2][3] && !Processor(2).Occupied

/*

*/
E<> runs[1][2] == 1 && runs[2][3] == 0 && !Processor(2).Occupied

/*

*/
E<> runs[2][3] == 1

/*

*/
E<> t_time >= 1080

/*
ca max time
*/
E<> t_time >= 2380

/*
36timer
*/
E<> t_time >= 2160
