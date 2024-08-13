import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog'
import { AccessTokenService } from '../access-token.service';

@Component({
  selector: 'app-access-token-create',
  standalone: true,
  imports: [MatDialogModule, FormsModule],
  templateUrl: './access-token-create.component.html',
  styleUrl: './access-token-create.component.scss'
})
export class AccessTokenCreateComponent {
  name: string = '';
  expiration: Date | null;
  dialogRef = inject(MatDialogRef<AccessTokenCreateComponent>)
  tokenService = inject(AccessTokenService)
  
  onCreateNewAccessToken(){
    if (this.expiration){
      this.tokenService.createToken({name: this.name, expires: this.expiration})
    } else{
      this.tokenService.createToken({name: this.name})
    }
    this.dialogRef.close()
  }

  onCancel() {
    this.dialogRef.close()
  }
}
