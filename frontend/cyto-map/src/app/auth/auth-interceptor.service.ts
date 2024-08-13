import { HttpHeaders, HttpInterceptorFn } from "@angular/common/http";
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { inject } from "@angular/core";
import { exhaustMap, of, switchMap, take } from "rxjs";
import { AuthService } from "./auth.service";
import { SigninDialogComponent } from "./signin-dialog/signin-dialog.component";

export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const authService = inject(AuthService);
    const router = inject(Router);
    const dialog = inject(MatDialog);
    const refreshTokenUrl = `${authService.authUrl}token/refresh/`;
    return authService.user.pipe(
        take(1),
        exhaustMap(user => {
            console.log(req.url) 
            if (!user || req.url === refreshTokenUrl) {
                return next(req)
            }
            console.log('checking access token');
            if(authService.isTokenExpired(user.access_token)){
                console.log('checking refresh token')
                if(authService.isTokenExpired(user.refresh_token)) {
                    dialog.open(SigninDialogComponent).afterClosed().
                        subscribe(() =>{
                            authService.onSignOut()
                            router.navigate(['/login']);
                        }
                    );
                    return of();
                }else{
                    return authService.refreshToken().pipe(
                        switchMap(() => {
                            const modifiedReq = req.clone(
                                {headers: new HttpHeaders().set(
                                    'Authorization', `Bearer ${authService.user.getValue()?.access_token}`
                                )}
                            )
                            return next(modifiedReq)
                        })
                    )
                }
            }else{
                const modifiedReq = req.clone({headers: new HttpHeaders().set('Authorization', `Bearer ${user.access_token}`)})
                return next(modifiedReq)
            }
        })
    )
}