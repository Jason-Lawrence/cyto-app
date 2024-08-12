import { Component, inject, OnInit } from '@angular/core';
import { AccessToken } from './access-token/access-token.model';
import { AccessTokenComponent } from './access-token/access-token.component';
import { AccessTokenService } from './access-token.service';
import { MatDialog } from '@angular/material/dialog'
import { AccessTokenCreateComponent } from './access-token-create/access-token-create.component';

@Component({
  selector: 'app-access-tokens',
  standalone: true,
  imports: [AccessTokenComponent],
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
}
