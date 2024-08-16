import { Injectable } from "@angular/core";
import { NetworkMap, Node, Edge } from "./network-map.model";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, Observable } from "rxjs";


@Injectable(
    {providedIn: 'root'}
)
export class NetworkMapService {
    private network_map_subject = new BehaviorSubject<NetworkMap | null>(null)
    public network_map_select: Observable<NetworkMap | null> = this.network_map_subject.asObservable();

    private network_maps_subject = new BehaviorSubject<NetworkMap[]>([])
    public network_maps: Observable<NetworkMap[]> = this.network_maps_subject.asObservable();

    private network_map_url: string = "http://127.0.0.1:8000/api/network-maps/"

    
    constructor(private http: HttpClient) {}

    listNetworkMaps() {
        this.http.get<NetworkMap[]>(this.network_map_url).subscribe(
            (network_maps: NetworkMap[]) => {
                this.network_maps_subject.next(network_maps);
            }
        );
    }

    createNetworkMap(network_map_data: {name: string, description: string, is_public: boolean, layout: string}) {
        return this.http.post<NetworkMap>(this.network_map_url, network_map_data).subscribe(
            (new_network_map: NetworkMap) => {
                this.network_map_subject.next(new_network_map)
                const current_network_maps = this.network_maps_subject.getValue()
                this.network_maps_subject.next([...current_network_maps, new_network_map])
            }
        )
    }

    deleteNetworkMap(network_map_to_delete: NetworkMap) {
        return this.http.delete(`${this.network_map_url}${network_map_to_delete.id}/`).subscribe(
            () => {
                const current_network_maps = this.network_maps_subject.getValue();
                this.network_maps_subject.next(
                    current_network_maps.filter(network_map => network_map.id !== network_map_to_delete.id)
                )
                const current = this.network_map_subject.getValue();
                if (current && current.id === network_map_to_delete.id) {
                    this.network_map_subject.next(null)
                }
            }
        )
    }

    getNetworkMap(network_map_id: number) {
        this.http.get<NetworkMap>(`${this.network_map_url}${network_map_id}/`).subscribe(
            (network_map: NetworkMap) => {
                this.network_map_subject.next(network_map)
            }
        )
    }

    updateNetworkMap(network_map: NetworkMap) {
        this.http.put<NetworkMap>(`${this.network_map_url}${network_map.id}/`, network_map).subscribe(
            (network_map: NetworkMap) => {
                console.log(network_map)
            }
        )
    }

    getNetworkMapCytoscape(network_map_id: number) {
        return this.http.get(`${this.network_map_url}${network_map_id}/cytoscape/`)
    }
}