import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass'],
})
export class LoginComponent implements OnInit {
  username: string;
  password: string;

  constructor() {}

  ngOnInit(): void {}

  login(): void {
    console.log("Login called with username: " + this.username + " password: " + this.password);

  }
}
