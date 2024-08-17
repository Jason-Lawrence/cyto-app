import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-node-edge-select',
  standalone: true,
  imports: [MatIconModule, CommonModule],
  templateUrl: './node-edge-select.component.html',
  styleUrl: './node-edge-select.component.scss'
})
export class NodeEdgeSelectComponent {
  isExpanded = false;

  toggleExpand() {
    this.isExpanded = !this.isExpanded
  }
}
