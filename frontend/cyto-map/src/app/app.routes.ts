import { Routes } from '@angular/router';
import { GraphComponent} from './graph/graph.component'
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component'
import { authorizedMatch } from './auth/auth.guard';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: '', component: GraphComponent, canMatch: [authorizedMatch]}
];
