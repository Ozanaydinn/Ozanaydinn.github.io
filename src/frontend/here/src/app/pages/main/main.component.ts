import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass'],
})
export class MainComponent implements OnInit {
  upcomingClasses: any[];
  constructor() {}

  ngOnInit(): void {
    this.upcomingClasses = [
      { // will be fetched
        name: "ML",
        code: "CS464",
        time: "09.30",
        link:""
      },
      {
        name: "PMBOK",
        code: "CS413",
        time: "13.30",
        link:""
      }
    ];
  }

  
}
