import { Routes } from '@angular/router';
import { RegistrationComponent } from './register/registration/registration.component';
import { LoginComponent } from './auth/login/login.component';
import { HomeComponent } from './contents/home/home.component';
import { LayoutComponent } from './shared/layout/layout.component';

export const routes: Routes = [
    { path: 'app',
        component: LayoutComponent,
        children: [
            { path: '', component: HomeComponent },
            { path: 'register', component: RegistrationComponent, },
            { path: 'login', component: LoginComponent, },
        ],
    },
    { path: '**', redirectTo: 'app' },
];
