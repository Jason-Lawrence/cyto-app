import { Component, inject, OnInit } from '@angular/core';
import { AccessToken } from './access-token.model';
import { AccessTokenService } from './access-token.service';
import { MatDialog } from '@angular/material/dialog'
import { AccessTokenCreateComponent } from './access-token-create/access-token-create.component';

@Component({
  selector: 'app-access-tokens',
  standalone: true,
  imports: [],
  templateUrl: './access-tokens.component.html',
  styleUrl: './access-tokens.component.scss'
})
export class AccessTokensComponent implements OnInit{
  accessTokens: AccessToken[]
  tokenService = inject(AccessTokenService);
  dialog = inject(MatDialog)

  ngOnInit(): void {
    this.tokenService.listTokens()
    this.tokenService.accessTokens.subscribe(
      tokens => {
        this.accessTokens = tokens
      }
    );
  }

  onCreateToken() {
    this.dialog.open(AccessTokenCreateComponent)
  }

  onRevokeToken(token: AccessToken){
    this.tokenService.revokeToken(token.id)
    token.is_revoked = true
  }
  
  onDeleteToken(token: AccessToken) {
    this.tokenService.deleteToken(token)
  }
}
