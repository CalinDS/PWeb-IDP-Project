import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  isDataLoaded = false;
  loggedInAuth = false;

  user: any;
  authUser: any;

  constructor(public auth: AuthService, private router: Router, private http: HttpClient) { }

  ngOnInit(): void {
    this.auth.isAuthenticated$.subscribe(
      loggedInAuth => {
        if (loggedInAuth) {
          this.auth.user$.subscribe(
            user => {
              this.authUser = user;
              this.http.get<any>('http://127.0.0.1:5000/users/' + user?.sub?.replace('|', '')).subscribe(data => {
                this.user = data;
                if (this.user) {
                  this.router.navigateByUrl('/accommodations');
                }
              });
            }
          );
        } 

        this.isDataLoaded = true;
        this.loggedInAuth = loggedInAuth
      }
    )
  }

}
