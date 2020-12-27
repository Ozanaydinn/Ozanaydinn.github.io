import { Component, OnInit } from '@angular/core';
import { SocketioService } from 'src/app/services/socketio.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass'],
})
export class MainComponent implements OnInit {
  video: HTMLVideoElement;
  constraints = { audio: true, video: true };
  videoOn: boolean;
  message: string;
  imageSrc: string = '';

  constructor(private socketService: SocketioService) {}

  ngOnInit(): void {
    this.socketService.setupSocketConnection();
    this.videoOn = false;
    this.message = 'Start';
    this.socketService.getMessages().subscribe(
      (message: string) => {
        console.log('Received', message);
      },
      (err) => {
        console.log(err);
      }
    );
  }

  startVideo(): void {
    this.video = document.querySelector('video');
    this.videoOn = true;
    navigator.mediaDevices.getUserMedia(this.constraints).then(
      (stream) => {
        this.video.srcObject = stream;
        console.log('Streaming video');
      },
      (error) => {
        console.log('Error: ' + error);
        this.videoOn = false;
      }
    );
  }

  stopVideo(): void {
    (<MediaStream>this.video.srcObject).getTracks().forEach((track) => {
      track.stop();
    });
    this.videoOn = false;
  }

  emitMessage(): void {
    console.log('Sending', this.message);
    this.socketService.emitMessage(this.message);
  }

  handleInputChange(e) {
    var file = e.dataTransfer ? e.dataTransfer.files[0] : e.target.files[0];
    var pattern = /image-*/;
    var reader = new FileReader();
    if (!file.type.match(pattern)) {
      alert('invalid format');
      return;
    }
    reader.onload = this._handleReaderLoaded.bind(this);
    reader.readAsDataURL(file);
  }
  
  _handleReaderLoaded(e) {
    let reader = e.target;
    this.imageSrc = reader.result;
    this.socketService.emitImage(reader.result);
  }
}
