import { HttpClient } from '@angular/common/http';
import {Component, Inject, OnInit} from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.scss']
})
export class PopupComponent implements OnInit {

  public refugee_id: any;
  public accommodation_id: any
  authUser: any;
  user: any;
;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any, public auth: AuthService, private http: HttpClient,
    public dialogRef: MatDialogRef<PopupComponent>, private router: Router) { }

  ngOnInit(): void {
    this.auth.user$.subscribe(
      user => {
        this.authUser = user;
        this.http.get<any>('http://127.0.0.1:5000/users/' + user?.sub?.replace('|', '')).subscribe(data => {
          this.user = data;
          // console.log(this.user);
        });
      }
    );
  }

  createBooking(): void {
    const body = {
      refugee_id: this.user.id,
      accommodation_id: this.data.accommodation.id,
    };
    // console.log(body);
    this.http.post<any>('http://127.0.0.1:5000/bookings/create', body).subscribe();
    this.dialogRef.close();
  }

  deleteAccommodation(): void {
    this.http.post<any>('http://127.0.0.1:5000/accommodations/' + this.data.accommodation.id + '/delete', {}).subscribe();
    window.location.reload();
    this.dialogRef.close();
  }

}
