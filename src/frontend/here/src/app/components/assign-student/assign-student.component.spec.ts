import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignStudentComponent } from './assign-student.component';

describe('AssignStudentComponent', () => {
  let component: AssignStudentComponent;
  let fixture: ComponentFixture<AssignStudentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssignStudentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssignStudentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
