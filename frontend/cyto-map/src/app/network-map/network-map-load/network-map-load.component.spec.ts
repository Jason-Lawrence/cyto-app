import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NetworkMapLoadComponent } from './network-map-load.component';

describe('NetworkMapLoadComponent', () => {
  let component: NetworkMapLoadComponent;
  let fixture: ComponentFixture<NetworkMapLoadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NetworkMapLoadComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NetworkMapLoadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
