import { Routes } from '@angular/router';
import { GraphComponent} from './graph/graph.component'
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component'
import { authorizedMatch } from './auth/auth.guard';
import { UserProfileComponent } from './auth/user-profile/user-profile.component';
import { UserProfileEditComponent } from './auth/user-profile/user-profile-edit/user-profile-edit.component';


export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: '', component: GraphComponent, canMatch: [authorizedMatch]},
    {
        path: 'profile', 
        component: UserProfileComponent, 
        children: [
            {
                path:'edit',
                component: UserProfileEditComponent
            }
        ]
    }
];
