import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass'],
})
export class RegisterComponent implements OnInit {
  username: string;
  password: string;
  email: string;
  constructor() {}

  ngOnInit(): void {}
  register(): void {
    console.log("Register called with username: " + this.username + " password: " + this.password + " email: " + this.email);
  }
}
