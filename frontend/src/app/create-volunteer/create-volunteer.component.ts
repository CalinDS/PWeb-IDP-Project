import { Component, Input, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-volunteer',
  templateUrl: './create-volunteer.component.html',
  styleUrls: ['./create-volunteer.component.scss']
})
export class CreateVolunteerComponent implements OnInit {

  public name = "";
  public contactInfo = "";
  user: any;

  constructor(public auth: AuthService, private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.auth.user$.subscribe(
      user => this.user = user
    );
  }

  saveProfile(): void {
    const body = {
      auth_id: this.user.sub.replace('|', ""),
      email: this.user.email,
      name: this.name,
      type: "volunteer",
      contact_info: this.contactInfo,
      family_members_no: -1
    };
    this.http.post<any>('http://127.0.0.1:5000/users/create', body).subscribe(
      (data) => {
        this.router.navigateByUrl('/accommodations');
      },
      (error) => {
         console.log(error);
         this.router.navigateByUrl('/accommodations');
      }
    )
  }

}
