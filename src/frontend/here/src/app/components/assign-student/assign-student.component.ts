import { _isNumberValue } from '@angular/cdk/coercion';
import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-assign-student',
  templateUrl: './assign-student.component.html',
  styleUrls: ['./assign-student.component.sass']
})
export class AssignStudentComponent implements OnInit {
  studentId: number;
  constructor(@Inject(MAT_DIALOG_DATA) public data: {courseCode: string}, private dialogRef: MatDialogRef<AssignStudentComponent>) { }

  ngOnInit(): void {
    this.studentId = undefined;
  }

  assignStudent(): void{
    if(this.studentId != undefined){
      if(_isNumberValue(this.studentId)){
        alert("Assigning " + this.studentId + " to " + this.data.courseCode);
        alert("Database not implemeted yet");
        this.dialogRef.close();
      }
      else{
        alert("Enter numeric values");
      }
    }
    else{
      alert("Enter a valid ID");
    }
  }
}
