import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.sass']
})
export class ProfileComponent implements OnInit {
  user_type: string;
  username: string;
  saved_notes: any[];
  constructor() { }

  ngOnInit(): void {
    // Fetch them from database
    this.username = "John Doe";
    this.user_type = "Student";
    this.saved_notes = [
      {
        date: "10/11/2020",
        class: "CS464",
        link:""
      },
      {
        date: "29/01/2021",
        class: "CS413",
        link:""
      }
    ];
  }

}
