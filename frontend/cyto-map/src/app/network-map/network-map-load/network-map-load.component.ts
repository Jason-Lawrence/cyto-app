import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { NetworkMapService } from '../network-map.service';
import { Subscription } from 'rxjs';
import { NetworkMap } from '../network-map.model';

@Component({
  selector: 'app-network-map-load',
  standalone: true,
  imports: [MatDialogModule, FormsModule],
  templateUrl: './network-map-load.component.html',
  styleUrl: './network-map-load.component.scss'
})
export class NetworkMapLoadComponent implements OnInit, OnDestroy{
  dialogRef = inject(MatDialogRef<NetworkMapLoadComponent>);
  networkmap_service = inject(NetworkMapService)
  network_maps_sub: Subscription;
  network_maps: NetworkMap[];

  ngOnInit(): void {
    this.network_maps_sub = this.networkmap_service.network_maps.subscribe(
      network_maps => {
        this.network_maps = network_maps
      }
    )
  }

  ngOnDestroy(): void {
    this.network_maps_sub.unsubscribe();
  }

  onLoad(){
    
  }
}
