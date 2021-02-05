import { Component, OnInit } from '@angular/core';
import { SocketioService } from 'src/app/services/socketio.service';

@Component({
  selector: 'app-conference',
  templateUrl: './conference.component.html',
  styleUrls: ['./conference.component.sass']
})
export class ConferenceComponent implements OnInit {
  video: HTMLVideoElement;
  share: HTMLVideoElement;
  constraints = { audio: false, video: true };
  videoOn: boolean;
  shareOn: boolean;
  message: string;

  constructor(private socketService: SocketioService) { }

  ngOnInit(): void {
    this.socketService.setupSocketConnection();
    this.videoOn = false;
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
    this.video = document.getElementById('host-video') as HTMLVideoElement;
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

  startShare(): void {
    this.share = document.getElementById('shared-screen') as HTMLVideoElement;
    this.shareOn = true;
    // @ts-ignore
    navigator.mediaDevices.getDisplayMedia().then(
      (stream) => {
        this.share.srcObject = stream;
        console.log('Sharing screen');
        (<MediaStream>this.share.srcObject).getVideoTracks()[0].addEventListener('ended', () => {
          this.stopSharing();
        });
      },
      (error) => {
        console.log('Error: ' + error);
        this.shareOn = false;
      }
    );
  }

  stopSharing(): void {
    console.log('screensharing has ended')
    this.share.srcObject = undefined;
    this.shareOn = false;
  }

  stopVideo(): void {
    console.log('video sharing has ended')
    if(this.videoOn){
      (<MediaStream>this.video.srcObject).getTracks().forEach((track) => {
        track.stop();
      });
      this.videoOn = false;
      this.video.srcObject = undefined;
    }
  }

  emitMessage(): void {
    console.log('Sending', this.message);
    this.socketService.emitMessage(this.message);
  }

  captureVideo(){
    if( this.videoOn){
      const canvas = document.createElement("canvas");
      // scale the canvas accordingly
      canvas.width = this.video.videoWidth;
      canvas.height = this.video.videoHeight;
      // draw the video at that frame
      canvas.getContext('2d')
        .drawImage(this.video, 0, 0, canvas.width, canvas.height);
      // convert it to a usable data URL
      this.socketService.emitImage(canvas.toDataURL());
    }
    else{
      console.error("Video stream is not on!");
    }

  }

}
