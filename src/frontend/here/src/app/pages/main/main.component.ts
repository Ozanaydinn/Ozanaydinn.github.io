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
      {
        courseCode: "CS464",
        courseName: "Machine Learning"
      },
      {
        courseCode: "CS491",
        courseName: "Seminar"
      },
    ]
  }
}
