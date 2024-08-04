import { inject } from "@angular/core";
import { CanMatchFn, RedirectCommand, Router } from "@angular/router";
import { AuthService } from "./auth.service";
import { take, map } from "rxjs";


export const authorizedMatch: CanMatchFn = (route, segments) => {
    const router = inject(Router)
    const authService = inject(AuthService)
    return authService.user.pipe(
        take(1),
        map((user => {
            const isAuthorized = !!user;
            console.log(isAuthorized)
            if (isAuthorized) {
                return true;
            }else {
                console.log("Please sign in.")
                return new RedirectCommand(router.parseUrl('/login'))
            }
        }))
    )
}