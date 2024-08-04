import { HttpEvent, HttpHandler, HttpHeaders, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Injectable } from "@angular/core";
import { exhaustMap, Observable, take } from "rxjs";
import { AuthService } from "./auth.service";
import { SigninDialogComponent } from "./signin-dialog/signin-dialog.component";


@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

    constructor(private authservice: AuthService, private dialog: MatDialog, private router: Router) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return this.authservice.user.pipe(
            take(1),
            exhaustMap(user => {
                if (!user) {
                    return next.handle(req)
                }
                if (this.authservice.isTokenExpired(user.access_token)){
                    if (this.authservice.isTokenExpired(user.refresh_token)){
                        this.dialog.open(SigninDialogComponent).afterClosed().subscribe(() =>{
                            this.router.navigate(['/sign-in']);
                        })
                        
                    }else {
                        this.authservice.refreshToken()
                    }

                }
                const modifiedReq = req.clone({headers: new HttpHeaders().set('Authorization', `Bearer ${user.access_token}`)})
                return next.handle(modifiedReq)
            })
        )
    }
}