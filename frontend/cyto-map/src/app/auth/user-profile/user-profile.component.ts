import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Subscription } from 'rxjs';
import { User } from '../user.model';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.scss'
})
export class UserProfileComponent implements OnInit, OnDestroy {
  authService = inject(AuthService)
  router = inject(Router)
  route = inject(ActivatedRoute)

  user!: User ;
  private userSub: Subscription;

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (user: User | null) => {
        if (user){
          this.user = user;
        }
      }
    )
  }

  ngOnDestroy(): void {
    this.userSub.unsubscribe()
  }

  onEdit(): void {
    this.router.navigate(['edit'], {relativeTo: this.route})
  }
}
