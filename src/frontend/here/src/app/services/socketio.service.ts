import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SocketioService {
  socket;
  constructor() {}

  setupSocketConnection() {
    this.socket = io(environment.SOCKET_ENDPOINT, {transports: ['websocket', 'polling', 'flashsocket']});
  }

  emitMessage(message: string): void{
    this.socket.emit('message', message);
  }

  emitImage(image: string): void{
    this.socket.emit('image', image);
  }


  getMessages() {
    return new Observable((observer) => {
        this.socket.on('message', (message) => {
          observer.next(message);
        });
    });
  }
}
