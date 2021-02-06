import { Component, Inject, OnInit } from '@angular/core';
import {
  MatDialog,
  MatDialogRef,
  MAT_DIALOG_DATA,
} from '@angular/material/dialog';

import {RegisterComponent} from '../../components/register/register.component';
import {LoginComponent} from '../../components/login/login.component';


// https://codepen.io/andrewarchi/pen/beqjoL


@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.sass'],
})
export class AuthComponent implements OnInit {
  username: string;
  password: string;

  constructor(public dialog: MatDialog) {}
  ngOnInit(): void {}

  openLoginDialog(): void {
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '500px',
      data: {name: this.username, password: this.password}
    });

    dialogRef.afterClosed().subscribe(() => {
      console.log('The login dialog was closed');
    });
  }

  openRegisterDialog(): void {
    const dialogRef = this.dialog.open(RegisterComponent, {
      width: '500px',
      data: {name: this.username, password: this.password}
    });

    dialogRef.afterClosed().subscribe(() => {
      console.log('The register dialog was closed');
    });
  }

  
}

