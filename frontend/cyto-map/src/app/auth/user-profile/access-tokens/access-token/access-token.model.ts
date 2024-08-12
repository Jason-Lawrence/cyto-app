export class AccessToken {
    constructor(
        public id: number,
        public name: string,
        public created: string,
        public expires: string,
        public is_revoked: boolean,
        public is_expired: boolean,
        private _token: string,
    ) {}

    get token(){
        return this._token
    }
}