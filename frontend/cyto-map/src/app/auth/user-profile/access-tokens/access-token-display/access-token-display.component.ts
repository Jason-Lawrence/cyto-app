import { Component, Inject, inject } from '@angular/core';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog'


@Component({
  selector: 'app-access-token-display',
  standalone: true,
  imports: [MatDialogModule],
  templateUrl: './access-token-display.component.html',
  styleUrl: './access-token-display.component.scss'
})
export class AccessTokenDisplayComponent {
  dialogRef = inject(MatDialogRef<AccessTokenDisplayComponent>)

  constructor(@Inject(MAT_DIALOG_DATA) public data: {token: string}) {}

  onClose(){
    this.dialogRef.close()
  }
}
