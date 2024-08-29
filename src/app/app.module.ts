import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ErrorComponent } from './error/error.component';
import { DelayComponent } from './delay/delay.component';
import { TripPathOneComponent } from './trip-path-one/trip-path-one.component';
import { TripPathTwoComponent } from './trip-path-two/trip-path-two.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    ErrorComponent,
    DelayComponent,
    TripPathOneComponent,
    TripPathTwoComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
