import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { NetworkMapService } from '../network-map.service';

@Component({
  selector: 'app-network-map-create',
  standalone: true,
  imports: [MatDialogModule, FormsModule],
  templateUrl: './network-map-create.component.html',
  styleUrl: './network-map-create.component.scss'
})
export class NetworkMapCreateComponent {
  name: string = '';
  description: string = '';
  is_public: boolean = false;
  layout: string = 'preset';
  dialogRef = inject(MatDialogRef<NetworkMapCreateComponent>);
  networkmap_service = inject(NetworkMapService)
  
  onCreate(){
    this.networkmap_service.createNetworkMap({
      name: this.name,
      description: this.description,
      is_public: this.is_public,
      layout: this.layout
    })
    this.dialogRef.close()
  }

  onCancel(){
    this.dialogRef.close()
  }
}
