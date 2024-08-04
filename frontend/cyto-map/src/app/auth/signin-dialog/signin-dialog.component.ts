import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog'

@Component({
  selector: 'app-signin-dialog',
  standalone: true,
  imports: [],
  templateUrl: './signin-dialog.component.html',
  styleUrl: './signin-dialog.component.scss'
})
export class SigninDialogComponent {

  constructor(private dialogRef: MatDialogRef<SigninDialogComponent>) {}

  onClose(): void{
    this.dialogRef.close();
  }
}
