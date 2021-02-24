import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass'],
})
export class RegisterComponent implements OnInit {
  username: string;
  password: string;
  email: string;
  type: string;
  registerForm: FormGroup;
  SERVER_URL = "http://localhost:5000/register"; // TODO

  constructor(
    private formBuilder: FormBuilder,
    private httpClient: HttpClient) {
      this.type = "student"
    }

  ngOnInit(): void {}
  register(): void {
    console.log("Register called with username: " + this.username + " password: " + this.password + " email: " + this.email);
    const formData = new FormData();
    formData.append("username", this.username);
    formData.append("password", this.password);
    formData.append("email", this.email);
    
    // TODO
    
    this.httpClient.post<any>(this.SERVER_URL, formData).subscribe(
      (res) => console.log(res),
      (err) => console.log(err)
    );
    
  }
}
