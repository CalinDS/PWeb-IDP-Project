import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.scss']
})
export class BookingComponent implements OnInit {

  @Input() address: any;
  @Input() image: any;
  @Input() beds_no: any;
  @Input() refugees: any;
  @Input() booking_id: any;
  

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    console.log(this.refugees)
  }

  cancelBooking(id: any): void {
    this.http.post<any>('http://127.0.0.1:5000/bookings/' + id + '/delete', {}).subscribe();
    window.location.reload();
  }

}
