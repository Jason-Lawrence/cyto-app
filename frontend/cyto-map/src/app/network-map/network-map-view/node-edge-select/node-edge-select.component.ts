import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { NodesComponent } from './nodes/nodes.component';

@Component({
  selector: 'app-node-edge-select',
  standalone: true,
  imports: [
    MatIconModule,
    CommonModule,
    NodesComponent
  ],
  templateUrl: './node-edge-select.component.html',
  styleUrl: './node-edge-select.component.scss'
})
export class NodeEdgeSelectComponent {
  isExpanded = false;

  toggleExpand() {
    this.isExpanded = !this.isExpanded
  }
}
