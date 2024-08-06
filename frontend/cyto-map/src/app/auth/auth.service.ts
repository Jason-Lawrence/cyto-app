import { BehaviorSubject, map, switchMap, tap } from "rxjs";
import { User } from "./user.model";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";


@Injectable(
    {providedIn: 'root'}
)
export class AuthService {
    user = new BehaviorSubject<User | null>(null);

    authUrl: string = "http://127.0.0.1:8000/api/users/"

    constructor(private http: HttpClient) { }

    isTokenExpired(token: string): boolean {
        const expiry = (JSON.parse(atob(token.split('.')[1]))).exp;
        return (Math.floor((new Date).getTime() / 1000)) >= expiry;
    }

    autoLogin(){
        const storedData = localStorage.getItem('userData');
        if (storedData){
            const userData: {
                email: string,
                name: string,
                _access_token: string,
                _refresh_token: string
            } = JSON.parse(storedData);

            const user = new User(userData.email, userData.name, userData._access_token, userData._refresh_token)
            this.user.next(user)
        }else {
            return
        }
        
    }

    private handlePostAuthentication(email: string, name:string, access_token: string, refresh_token: string) {
        const user = new User(email, name, access_token, refresh_token)
        this.user.next(user)
        localStorage.setItem('userData',JSON.stringify((user)))
    }

    registerNewUser(userData: any) {
        this.http.post(`${this.authUrl}create/`, userData).subscribe(
            responseData => {
                console.log(responseData)
            }
        )
    }

    onSignOut(){
        localStorage.removeItem('userData')
        this.user.next(null)
    }

    onSignIn(email: string, password: string) {
        return this.http.post<{access: string, refresh: string}>(
            `${this.authUrl}token/`, {'email': email, 'password': password}
        ).pipe(switchMap(
            (resData: {access: string, refresh: string}) => {
                const headers: HttpHeaders = new HttpHeaders().set('Authorization', `Bearer ${resData.access}`)
                return this.http.get<{email: string, name: string}>(`${this.authUrl}me/`, {'headers': headers}).pipe(
                    tap((userData: {email: string, name: string}) => {
                        this.handlePostAuthentication(userData.email, userData.name, resData.access, resData.refresh)
                    })
                )
            }
        ))
    }

    refreshToken() {
        const current_user = this.user.getValue()
        if (current_user) {
            return this.http.post<{access: string}>(
                `${this.authUrl}token/refresh/`, {refresh: current_user.refresh_token}
            ).pipe(
                tap((resData) => {
                    current_user.access_token = resData.access
                    localStorage.setItem('userData', JSON.stringify(current_user))
                })
            )
        }
        return
    } 
}