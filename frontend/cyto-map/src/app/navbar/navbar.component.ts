import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router'
import { Subscription } from 'rxjs';
import { AuthService } from '../auth/auth.service'

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent implements OnInit, OnDestroy{
  isAuthenticated: boolean = false;
  private userSub: Subscription;
  authService = inject(AuthService)


  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      user => {this.isAuthenticated = !!user}
    )
  }

  ngOnDestroy(): void {
    this.userSub.unsubscribe();
  }
}
