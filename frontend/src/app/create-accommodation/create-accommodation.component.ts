import { Component, Input, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-accommodation',
  templateUrl: './create-accommodation.component.html',
  styleUrls: ['./create-accommodation.component.scss']
})
export class CreateAccommodationComponent implements OnInit {

  public address = "";
  public beds_no = "";
  public familyMembersNo: any;
  public imageSrc: string = '';
  authUser: any;
  user: any;

  handleInputChange(e: any) {
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
  _handleReaderLoaded(e: any) {
    let reader = e.target;
    this.imageSrc = reader.result;
    // console.log(this.imageSrc)
  }

  constructor(public auth: AuthService, private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.auth.user$.subscribe(
      user => {
        this.authUser = user;
        this.http.get<any>('http://127.0.0.1:5000/users/' + user?.sub?.replace('|', '')).subscribe(data => {
          this.user = data;
          // console.log(this.user);
          if (this.user.type == 'refugee') {
            this.router.navigateByUrl('/accommodations');
          }
        });
      }
    );
  }

  addAccommodation(): void {
    const body = {
      owner_id: this.user.id,
      photo: this.imageSrc,
      address: this.address,
      beds_no: this.beds_no,
    };
    // console.log(body);
    this.http.post<any>('http://127.0.0.1:5000/accommodations/create', body).subscribe(
      (data) => {
        this.router.navigateByUrl('/accommodations');
      },
      (error) => {
        console.log(error);
        this.router.navigateByUrl('/accommodations');
      }
    );
  }
}
