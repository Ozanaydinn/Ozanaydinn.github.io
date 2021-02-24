import { Component, OnInit } from '@angular/core';
import { SocketioService } from './services/socketio.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent{
  username: string;
  loggedIn: boolean;
  constructor(private router: Router) {
    this.username = "John Doe";
    this.loggedIn = false;
  }
  goMain(){
    this.router.navigate(['/main']);
  }

  goProfile(){
    this.router.navigate(['/profile']);
  }

  logout(){
    this.router.navigate(['/auth']);
  }
}
