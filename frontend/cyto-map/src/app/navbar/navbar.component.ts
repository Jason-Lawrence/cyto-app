import { Component, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  isAuthenticated: boolean = false;
  //private userSub: Subscription;

  constructor(){ }

  // ngOnInit(): void {
    
  // }

  // ngOnDestroy(): void {
  //   this.userSub.unsubscribe();
  // }
}
