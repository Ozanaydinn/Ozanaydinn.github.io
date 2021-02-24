import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConferenceComponent } from './pages/conference/conference.component';
import { LoginComponent } from './components/login/login.component';
import { MainComponent } from './pages/main/main.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { RegisterComponent } from './components/register/register.component';
import { AuthComponent } from './pages/auth/auth.component';

const routes: Routes = [
  {path: '',  redirectTo: 'auth', pathMatch:'full'},
  {path: 'main', component: MainComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'conference', component: ConferenceComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'auth', component: AuthComponent},
  {path: '**', component: PageNotFoundComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
