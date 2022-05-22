import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-accommodation',
  templateUrl: './accommodation.component.html',
  styleUrls: ['./accommodation.component.scss']
})
export class AccommodationComponent implements OnInit {

  @Input() address: any;
  @Input() image: any;
  @Input() free_beds_no: any;
  @Input() beds_no: any;
  

  constructor() { }

  ngOnInit(): void {
  }

}
