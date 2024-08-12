import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { AccessToken } from "./access-token/access-token.model";
import { BehaviorSubject, Observable } from "rxjs";


@Injectable(
    {providedIn: 'root'}
)
export class AccessTokenService {
    private accessTokensSubject: BehaviorSubject<AccessToken[]> = new BehaviorSubject<AccessToken[]>([]);
    public accessTokens: Observable<AccessToken[]> = this.accessTokensSubject.asObservable();
    private tokenUrl: string = "http://127.0.0.1:8000/api/users/PAT/"

    constructor(private http: HttpClient) {}

    listTokens() {
        console.log()
        this.http.get<AccessToken[]>(this.tokenUrl).subscribe(
            (tokens: AccessToken[]) => {
                this.accessTokensSubject.next(tokens);
            }
        );
    }

    createToken(tokenData: {name: string, expires?: Date}) {
        return this.http.post<AccessToken>(this.tokenUrl, tokenData).subscribe(
            (newToken: AccessToken) => {
                const currentTokens = this.accessTokensSubject.getValue();
                this.accessTokensSubject.next([...currentTokens, newToken]);
            }
        );
    }

    deleteToken(token: AccessToken) {
        return this.http.delete(`${this.tokenUrl}${token.id}/`).subscribe(
            () => {
                const currentTokens = this.accessTokensSubject.getValue();
                this.accessTokensSubject.next(
                    currentTokens.filter(accessToken => accessToken.id !== token.id)
                );
            }
        )
    }

    revokeToken(token_id: number){
        this.http.patch(`${this.tokenUrl}${token_id}/`, {revoked: true}).subscribe(
            resp => {
                console.log(resp)
            }
        );
    }
}