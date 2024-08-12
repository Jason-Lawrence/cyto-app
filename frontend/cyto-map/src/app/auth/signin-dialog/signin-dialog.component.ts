import { Component } from '@angular/core';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog'

@Component({
  selector: 'app-signin-dialog',
  standalone: true,
  imports: [MatDialogModule],
  templateUrl: './signin-dialog.component.html',
  styleUrl: './signin-dialog.component.scss'
})
export class SigninDialogComponent {

  constructor(private dialogRef: MatDialogRef<SigninDialogComponent>) {}

  onClose(): void{
    this.dialogRef.close();
  }
}
