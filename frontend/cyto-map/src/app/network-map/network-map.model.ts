export class NetworkMap {

    constructor(
        public name: string,
        public description: string,
        public is_public: boolean,
        public layout: string,
        public nodes?: Node[],
        public edges?: Edge[],
        public created_at?: Date,
        public last_updated?: Date,
        public id?: number
    ) {}
}

export class Node {

    constructor(
        public nid: string,
        public label: string,
        public x: number,
        public y: number,
        public selectable: boolean,
        public locked: boolean,
        public pannable: boolean,
        public classes: string,
        public style: string,
        public scratch: string,
        public parent?: Node,
        public id?: number
    ) {}
}

export class Edge {

    constructor(
        public eid: string,
        public label: string,
        public source: Node,
        public target: Node,
        public pannable: boolean,
        public id?: number
    ) {}
}