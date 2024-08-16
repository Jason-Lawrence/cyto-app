import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { NetworkMapViewComponent } from './network-map-view/network-map-view.component';
import { NetworkMapCreateComponent } from './network-map-create/network-map-create.component';
import { NetworkMapLoadComponent } from './network-map-load/network-map-load.component';
import { MatDialog } from '@angular/material/dialog';
import { NetworkMap } from './network-map.model';
import { Subscription } from 'rxjs';
import { NetworkMapService } from './network-map.service';

@Component({
  selector: 'app-network-map',
  standalone: true,
  imports: [
    NetworkMapViewComponent,
    NetworkMapCreateComponent,
    NetworkMapLoadComponent
  ],
  templateUrl: './network-map.component.html',
  styleUrl: './network-map.component.scss'
})
export class NetworkMapComponent implements OnInit, OnDestroy {
  dialog = inject(MatDialog)
  networkmapService = inject(NetworkMapService)
  network_map: NetworkMap | null = null;
  network_map_sub: Subscription;

  ngOnInit(): void {
    this.network_map_sub = this.networkmapService.network_map_select.subscribe(
      network_map => {
        this.network_map = network_map
      }
    )
  }

  ngOnDestroy(): void {
    this.network_map_sub.unsubscribe();
  }

  onCreateNetworkMap(){
    this.dialog.open(NetworkMapCreateComponent)
  }

  onLoadNetworkMap(){
    this.dialog.open(NetworkMapLoadComponent)
  }

  onSaveNetworkMap(){

  }
}
