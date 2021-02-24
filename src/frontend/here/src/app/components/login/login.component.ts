import { Component, OnInit } from '@angular/core';
import { throwMatDialogContentAlreadyAttachedError, MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass'],
})
export class LoginComponent implements OnInit {
  username: string;
  password: string;
  loginForm: FormGroup;
  SERVER_URL = "http://localhost:5000/login"; // TODO

  constructor(
    private router: Router, 
    public dialogRef: MatDialogRef<LoginComponent>,
    private formBuilder: FormBuilder,
    private httpClient: HttpClient) { }

  ngOnInit(): void {}

  login(): void {
    console.log(
      'Login called with username: ' +
      this.username +
      ' password: ' +
      this.password
    );
    const formData = new FormData();
    formData.append("username", this.username);
    formData.append("password", this.password);
    // console.log(formData);
    // console.log(formData.get("password"));
    // console.log(formData.get("username"));
    
    // TODO
    /* 
    this.httpClient.post<any>(this.SERVER_URL, formData).subscribe(
      (res) => console.log(res),
      (err) => console.log(err)
    );
    */
    this.router.navigate(['main']);
    this.dialogRef.close();
  }


}
