import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})
export class MainComponent implements OnInit {

  video: HTMLVideoElement;
  constraints = { audio: true, video: true };
  constructor() { }

  ngOnInit(): void {
    this.video = document.querySelector('video');
    navigator.mediaDevices.getUserMedia(this.constraints).then(
      stream => {
        this.video.srcObject = stream
      },
      error => {
        console.log('Error: ' + error);
      });
  }

}