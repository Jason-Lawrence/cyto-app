import { Component } from '@angular/core';
import { NetworkMapViewComponent } from './network-map-view/network-map-view.component';
import { NetworkMapCreateComponent } from './network-map-create/network-map-create.component';
import { NetworkMapLoadComponent } from './network-map-load/network-map-load.component';

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
export class NetworkMapComponent {


  onCreateNetworkMap(){

  }

  onLoadNetworkMap(){
    
  }
}
