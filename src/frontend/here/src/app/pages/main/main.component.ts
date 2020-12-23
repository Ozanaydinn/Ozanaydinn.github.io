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

  }

  startVideo(): void {
    this.video = document.querySelector('video');
    navigator.mediaDevices.getUserMedia(this.constraints).then(
      stream => {
        this.video.srcObject = stream
        console.log("Streaming video")
      },
      error => {
        console.log('Error: ' + error);
      });
  }

  stopVideo(): void {
    this.video.srcObject = undefined;
  }

}