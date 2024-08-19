import { Component } from '@angular/core';
import { DragDropModule } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-nodes',
  standalone: true,
  imports: [DragDropModule],
  templateUrl: './nodes.component.html',
  styleUrl: './nodes.component.scss'
})
export class NodesComponent {
  nodes = [
    {
      id: 1,
      icon: 'circle-fill.svg',
      name: 'circle'
    },
    {
      id: 2,
      icon: 'square-fill.svg',
      name: 'square'
    },
    {
      id: 3,
      icon: 'triangle-fill.svg',
      name: 'triangle'
    },
    {
      id: 4,
      icon: 'rectangle-fill.svg',
      name: 'rectangle'
    }
  ]
}
