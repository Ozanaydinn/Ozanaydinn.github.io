import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})
export class MainComponent implements OnInit {

  video: HTMLVideoElement;
  constraints = { audio: true, video: true };
  videoOn: boolean

  constructor() { }

  ngOnInit(): void {
    this.videoOn = false;
  }

  startVideo(): void {
    this.video = document.querySelector('video');
    navigator.mediaDevices.getUserMedia(this.constraints).then(
      stream => {
        this.video.srcObject = stream
        console.log("Streaming video")
        this.videoOn = true
      },
      error => {
        console.log('Error: ' + error);
        this.videoOn = false;
      });
  }

  stopVideo(): void {
    (<MediaStream>this.video.srcObject).getTracks().forEach( (track) => {
      track.stop();
    })
    this.videoOn = false;
  }

  foo(): void {
    var socket = io('http://localhost:5000');

    socket.on('connect', function(){
        console.log("Connected...!", socket.connected)
    });

    const video = document.querySelector("#videoElement");

    video.width = 500; 
    video.height = 375; ;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err0r) {
            console.log(err0r)
            console.log("Something went wrong!");
        });
    }

    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    let cap = new cv.VideoCapture(video);

    const FPS = 22;

    setInterval(() => {
        cap.read(src);

        var type = "image/png"
        var data = document.getElementById("canvasOutput").toDataURL(type);
        data = data.replace('data:' + type + ';base64,', ''); //split off junk at the beginning

        socket.emit('image', data);
    }, 10000/FPS);


    socket.on('response_back', function(image){
        const image_id = document.getElementById('image');
        image_id.src = image;
    });
  }

}