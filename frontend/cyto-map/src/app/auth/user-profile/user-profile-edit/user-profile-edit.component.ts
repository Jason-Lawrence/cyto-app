import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { AuthService } from '../../auth.service';
import { User } from '../../user.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-profile-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './user-profile-edit.component.html',
  styleUrl: './user-profile-edit.component.scss'
})
export class UserProfileEditComponent implements OnInit, OnDestroy{
  error: string | null = null;
  resetPassword: boolean = false
  authService = inject(AuthService)
  router = inject(Router)
  userSub: Subscription;
  user!: User
  name: string = '';
  confirmPassword: string = '';
  newPassword: string = '';

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (user: User | null) => {
        if(user){
          this.user = user
          this.name = user.name
        }
      }
    )
  }

  ngOnDestroy(): void {
    this.userSub.unsubscribe()
  }

  onResetPassword(){
    this.resetPassword = true;
  }

  onCancelReset(){
    this.resetPassword = false;
    this.confirmPassword = '';
    this.newPassword = '';
  }

  onCancel(){
    this.router.navigate(['profile'])
  }

  onUpdateUser(){
    var data;
    if (this.newPassword.length > 0 && this.newPassword !== this.confirmPassword){
      let data = {
        name: this.name,
        password: this.newPassword
      }
    }else{
      let data = {
        name: this.name
      }
    }
    return this.authService.onUpdateUser(data)
  }
}
