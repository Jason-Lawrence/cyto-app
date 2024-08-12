import { Component, inject, Input } from '@angular/core';
import { AccessToken } from './access-token.model';
import { AccessTokenService } from '../access-token.service';

@Component({
  selector: 'app-access-token',
  standalone: true,
  imports: [],
  templateUrl: './access-token.component.html',
  styleUrl: './access-token.component.scss'
})
export class AccessTokenComponent {
  @Input() accessToken!: AccessToken;
  tokenService = inject(AccessTokenService)

  onRevokeToken(){
    this.tokenService.revokeToken(this.accessToken.id)
    this.accessToken.is_revoked = true
  }
  
  onDeleteToken() {
    this.tokenService.deleteToken(this.accessToken)
  }
}
