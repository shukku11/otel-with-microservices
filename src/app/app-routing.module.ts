import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { DelayComponent } from './delay/delay.component';
import { ErrorComponent } from './error/error.component';
import { TripPathTwoComponent } from './trip-path-two/trip-path-two.component';
import { TripPathOneComponent } from './trip-path-one/trip-path-one.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'path_one', component: TripPathOneComponent },
  { path: 'path_two', component: TripPathTwoComponent },
  { path: 'error', component: ErrorComponent },
  { path: 'delay', component: DelayComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Default route
  { path: '**', redirectTo: '/error' }, // Wildcard route for a 404 page
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
