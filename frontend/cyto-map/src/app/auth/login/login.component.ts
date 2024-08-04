import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { LoadingSpinnerComponent } from '../../shared/loading-spinner/loading-spinner.component' 


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, LoadingSpinnerComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  error: string | null = null;
  isLoading = false;
  email: string = 'test@example.com'
  password: string;

  constructor(private router: Router, private authService: AuthService) {}

  onRegister(){
    this.router.navigate(['register'])
  }
  onLogin() {
    this.isLoading = true;
    this.authService.onSignIn(this.email, this.password)
      .subscribe(
        resData => {
          this.router.navigate([''])
        },
        error => {
          this.error = 'An error occurred'
          console.log(error)
        }
      );
      this.isLoading = false;
  }
}
