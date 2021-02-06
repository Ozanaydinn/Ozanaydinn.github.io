import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AssignStudentComponent } from 'src/app/components/assign-student/assign-student.component';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.sass']
})
export class ProfileComponent implements OnInit {
  user_type: string;
  username: string;
  user_id: number;
  saved_notes: any[];
  courses: any[];
  constructor(private dialog: MatDialog) { }

  ngOnInit(): void {
    // Fetch them from database
    this.username = "John Doe";
    this.user_type = "instructor";
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
    this.courses = [
      {
        name: "Machine Learning",
        code: "CS464",
      },
      {
        name: "Seminar",
       code: "CS491",
      }
    ];
  }

  addCourse(): void{
    if(this.user_type === "instructor"){
      alert("Not yet implemented");
      // TODO
    }
  }

  assignStudent(courseCode: string): void{
    this.dialog.open(AssignStudentComponent, {
      data: {courseCode: courseCode}
    });
  }

}
