import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-schedule-table',
  templateUrl: './schedule-table.component.html',
  styleUrls: ['./schedule-table.component.sass'],
})
export class ScheduleTableComponent implements OnInit {
  displayedColumns: string[] = ['hour', 'monday', 'tuesday'];
  dataSource = SCHEDULE_DATA;
  hours = ['8.30', '10.30', '13.30'];

  constructor() {}

  ngOnInit(): void {}
}

export interface WeeklySchedule {
  hour: string; //TODO hours will be seperate
  monday: string;
  tuesday: string;
}

const SCHEDULE_DATA: WeeklySchedule[] = [
  { hour: '8.30', monday: 'ML', tuesday: 'PMBOK' },
  { hour: '10.30', monday: 'OOP', tuesday: 'Network' },
  { hour: '10.30', monday: 'OOP', tuesday: 'Network' },
  { hour: '13.30', monday: 'Cloud', tuesday: 'OS' },
];