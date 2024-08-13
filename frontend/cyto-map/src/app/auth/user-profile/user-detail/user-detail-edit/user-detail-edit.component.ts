import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../../../auth.service';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { User } from '../../../user.model';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-detail-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './user-detail-edit.component.html',
  styleUrl: './user-detail-edit.component.scss'
})
export class UserDetailEditComponent implements OnInit, OnDestroy{
  error: string | null = null;
  resetPassword: boolean = false;
  authService = inject(AuthService)
  router = inject(Router)
  userSub: Subscription;
  user!: User;
  name: string = '';
  confirmPassword: string = '';
  newPassword: string = '';

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (user: User | null) => {
        if(user) {
          this.user = user
          this.name = user.name
        }
      }
    )
  }

  ngOnDestroy(): void {
    this.userSub.unsubscribe()
  }
  onResetPassword(): void {
    this.resetPassword = true;
  }

  onCancelReset(): void {
    this.resetPassword = false;
    this.confirmPassword = '';
    this.newPassword = ''; 
  }

  onCancel(): void {
    this.router.navigate(['profile'])
  }

  onUpdateUser(): void {
    var data;
    if (this.newPassword.length > 0 && 
        this.newPassword === this.confirmPassword
      ){
        data = {
          name: this.name,
          password: this.newPassword
        }
    } else {
      data = {
        name: this.name
      }
    }
    return this.authService.onUpdateUser(data)
  }
}
