import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRefugeeComponent } from './create-refugee.component';

describe('CreateRefugeeComponent', () => {
  let component: CreateRefugeeComponent;
  let fixture: ComponentFixture<CreateRefugeeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateRefugeeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateRefugeeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
