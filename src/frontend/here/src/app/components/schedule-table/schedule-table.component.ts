import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-schedule-table',
  templateUrl: './schedule-table.component.html',
  styleUrls: ['./schedule-table.component.sass'],
})
export class ScheduleTableComponent implements OnInit {
  displayedColumns: string[] = ['hour', 'monday', 'tuesday'];
  dataSource = SCHEDULE_DATA;

  constructor() {}

  ngOnInit(): void {}
}

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H' },
  { position: 2, name: 'Helium', weight: 4.0026, symbol: 'He' },
  { position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li' },
  { position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be' },
  { position: 5, name: 'Boron', weight: 10.811, symbol: 'B' },
  // { position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C' },
  // { position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N' },
  // { position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O' },
  // { position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F' },
  // { position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne' },
];

export interface WeeklySchedule {
  hour: string; //TODO hours will be seperate
  monday: string;
  tuesday: string;
}

const SCHEDULE_DATA: WeeklySchedule[] = [
  { hour: '8.30', monday: 'ML', tuesday: 'PMBOK' },
  { hour: '10.30', monday: 'OOP', tuesday: 'Network' },
  { hour: '13.30', monday: 'Cloud', tuesday: 'OS' },
];