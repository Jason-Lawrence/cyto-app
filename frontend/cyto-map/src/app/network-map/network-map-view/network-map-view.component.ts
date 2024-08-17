import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { NetworkMap } from '../network-map.model';
import { Subscription } from 'rxjs';
import { NetworkMapService } from '../network-map.service';
import { NodeEdgeSelectComponent } from './node-edge-select/node-edge-select.component';

@Component({
  selector: 'app-network-map-view',
  standalone: true,
  imports: [NodeEdgeSelectComponent],
  templateUrl: './network-map-view.component.html',
  styleUrl: './network-map-view.component.scss'
})
export class NetworkMapViewComponent implements OnInit, OnDestroy{
  network_map: NetworkMap | null;
  network_map_sub: Subscription;
  network_map_service = inject(NetworkMapService)

  ngOnInit(): void {
    this.network_map_sub = this.network_map_service.network_map_select.subscribe(
      network_map => {
        this.network_map = network_map
      }
    );
  }

  ngOnDestroy(): void {
    this.network_map_sub.unsubscribe();
  }

}
