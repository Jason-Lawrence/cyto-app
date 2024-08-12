import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../../auth.service';
import { User } from '../../user.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-user-detail',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './user-detail.component.html',
  styleUrl: './user-detail.component.scss'
})
export class UserDetailComponent implements OnInit, OnDestroy{
  authService = inject(AuthService)
  router = inject(Router)
  route = inject(ActivatedRoute)

  user!: User;
  private userSub: Subscription;

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      (user: User | null) => {
        if (user) {
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
