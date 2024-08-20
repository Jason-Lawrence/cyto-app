import { Component, inject } from '@angular/core';
import cytoscape from 'cytoscape';
import { CytoscapeService } from '../../cytoscape.service';

@Component({
  selector: 'app-nodes',
  standalone: true,
  imports: [],
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
  cytoscape_service = inject(CytoscapeService)
  selectedNode: string | null = null;

  selectNode(nodeType: string) {
    this.selectedNode = nodeType
    this.cytoscape_service.selectedNodeType = nodeType
  }
}
