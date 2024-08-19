import { Component, ElementRef, inject, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { NetworkMap } from '../network-map.model';
import { Subscription } from 'rxjs';
import { NetworkMapService } from '../network-map.service';
import { NodeEdgeSelectComponent } from './node-edge-select/node-edge-select.component';
import { CdkDragDrop, DragDropModule } from '@angular/cdk/drag-drop';
import cytoscape from 'cytoscape';

@Component({
  selector: 'app-network-map-view',
  standalone: true,
  imports: [NodeEdgeSelectComponent, DragDropModule],
  templateUrl: './network-map-view.component.html',
  styleUrl: './network-map-view.component.scss'
})
export class NetworkMapViewComponent implements OnInit, OnDestroy{
  network_map: NetworkMap | null;
  network_map_sub: Subscription;
  network_map_service = inject(NetworkMapService)
  cy: any;

  ngOnInit(): void {
    this.network_map_sub = this.network_map_service.network_map_select.subscribe(
      network_map => {
        this.network_map = network_map
      }
    );
    this.cy = cytoscape({
      container: document.getElementById('cy'),
      elements: []
    })
  }

  ngOnDestroy(): void {
    this.network_map_sub.unsubscribe();
  }

  onDrop(event: CdkDragDrop<any>){
    const node = event.item.data;
    const position = event.dropPoint;

    console.log('adding node: ' + node.name)

    this.cy.add({
      group: 'nodes',
      data: {
        id: `node-${Date.now()}`,
        name: node.name
      },
      position: {
        x: position.x,
        y: position.y
      }
    });
    console.log('elements: ' + this.cy.elements)
  }
}
