import { _isNumberValue } from '@angular/cdk/coercion';
import { HttpClient } from '@angular/common/http';
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
  SERVER_URL = "http://localhost:5000/login";
  constructor(@Inject(MAT_DIALOG_DATA) public data: {courseCode: string}, private httpClient: HttpClient, private dialogRef: MatDialogRef<AssignStudentComponent>) { }

  ngOnInit(): void {
    this.studentId = undefined;
  }

  assignStudent(): void{
    if(this.studentId != undefined){
      if(_isNumberValue(this.studentId)){
        alert("Assigning " + this.studentId + " to " + this.data.courseCode);
        const formData = new FormData();
        formData.append("studentId", "slmyucoyici");
        formData.append("courseCode", this.data.courseCode);
        // console.log(formData);
        // console.log(formData.get("password"));
        // console.log(formData.get("username"));
        
        // TODO
        this.httpClient.post<any>(this.SERVER_URL, formData).subscribe(
          (res) => console.log(res),
          (err) => console.log(err)
        );
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
