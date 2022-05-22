import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PopupComponentUser } from './popup.component';

describe('PopupComponent', () => {
  let component: PopupComponentUser;
  let fixture: ComponentFixture<PopupComponentUser>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PopupComponentUser ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PopupComponentUser);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
