import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'refbnb';

  authUser: any;
  user: any = {
    type: 'refugee'
  };

  constructor(public auth: AuthService, private http: HttpClient) { }

  ngOnInit(): void {
    this.auth.user$.subscribe(
      user => {
        this.authUser = user;
        this.http.get<any>('http://127.0.0.1:5000/users/' + user?.sub?.replace('|', '')).subscribe(data => {
          this.user = data;
          console.log(this.user);
          
        });
      }
    );
  }

}
