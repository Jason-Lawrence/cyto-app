import { Injectable } from '@angular/core';
import cytoscape from 'cytoscape';


@Injectable({
  providedIn: 'root'
})
export class CytoscapeService {
  private cy: cytoscape.Core
  public selectedNodeType: string | null = null;

  constructor() { }

  initCytoscape(container: HTMLElement, options?: cytoscape.CytoscapeOptions): void {
    this.cy = cytoscape({
      container: container,
      ...options,
    });
    this.cy.on('tap', (event) => {
      const evtTarget = event.target;
      if (evtTarget === this.cy){
        const clickPosition = event.position;
        this.addNode(clickPosition)
      }
    })
  }

  addNode(position: {x: number, y: number}): void {
    if (this.selectedNodeType){
      this.cy.add({
        group: 'nodes',
        data: {
          id: `${this.selectedNodeType}-${Date.now()}`,
          label: this.selectedNodeType,
          shape: this.selectedNodeType,
        },
        position: position
      });
      this.selectedNodeType = null;
    }
  }

  getCyInstance(): cytoscape.Core {
    return this.cy
  }

}
