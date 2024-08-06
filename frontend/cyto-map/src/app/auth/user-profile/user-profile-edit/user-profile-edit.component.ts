import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { AuthService } from '../../auth.service';
import { User } from '../../user.model';

@Component({
  selector: 'app-user-profile-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './user-profile-edit.component.html',
  styleUrl: './user-profile-edit.component.scss'
})
export class UserProfileEditComponent implements OnInit, OnDestroy{
  error: string | null = null;
  email: string;
  authService = inject(AuthService)
  userSub: Subscription;
  user!: User

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (user: User | null) => {
        if(user){
          this.user = user
        }
      }
    )
  }

  ngOnDestroy(): void {
    this.userSub.unsubscribe()
  }

  onUpdateUser(){

  }
}
