export class User {

    constructor(
        public email: string,
        public name: string,
        private _access_token: string,
        private _refresh_token: string
    ) {}

    get access_token() {
        return this._access_token
    }

    set access_token(new_access_token: string) {
        this._access_token = new_access_token
    }

    get refresh_token() {
        return this._refresh_token
    }

}