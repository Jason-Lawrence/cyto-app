import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  name: string = '';
  email: string = 'test@example.com';
  password: string = '';
  
  constructor(private authService: AuthService, private router: Router) {}

  onRegisterNewUser() {
    let userData = {
      'name': this.name,
      'email': this.email,
      'password': this.password
    }
    this.authService.registerNewUser(userData)
  }

  onSignIn(){
    this.router.navigate(['login'])
  }
}
