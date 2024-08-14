import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component'
import { authorizedMatch } from './auth/auth.guard';
import { UserProfileComponent } from './auth/user-profile/user-profile.component';
import { UserDetailComponent } from './auth/user-profile/user-detail/user-detail.component';
import { UserDetailEditComponent } from './auth/user-profile/user-detail/user-detail-edit/user-detail-edit.component';
import { AccessTokensComponent } from './auth/user-profile/access-tokens/access-tokens.component'
import { PreferencesComponent } from './auth/user-profile/preferences/preferences.component'
import { NetworkMapComponent } from './network-map/network-map.component';


export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: '', component: NetworkMapComponent, canMatch: [authorizedMatch]},
    {
        path: 'profile', 
        component: UserProfileComponent, 
        children: [
            {
                path:'details',
                component: UserDetailComponent,
                children: [
                    {
                        path: 'details-edit', 
                        component: UserDetailEditComponent
                    }
                ]
            },
            {
                path: 'access-token',
                component: AccessTokensComponent
            },
            {
                path: 'preferences',
                component: PreferencesComponent
            }
        ]
    }
];
