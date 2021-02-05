import { Component, OnInit } from '@angular/core';
import { throwMatDialogContentAlreadyAttachedError, MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass'],
})
export class LoginComponent implements OnInit {
  username: string;
  password: string;

  constructor(private router: Router, public dialogRef: MatDialogRef<LoginComponent>) {}

  ngOnInit(): void {}

  login(): void {
    console.log(
      'Login called with username: ' +
        this.username +
        ' password: ' +
        this.password
    );
    this.router.navigate(['main']);
    this.dialogRef.close();
  }

  
}
