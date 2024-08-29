import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { LoaderService } from './loader.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  apiUrl = 'http://localhost:8002'; // Your API URL

  isLoading: Observable<boolean>;

  constructor(private http: HttpClient,private loaderService: LoaderService) {
    this.isLoading = this.loaderService.loading$;
  }

  responseFromApi: any;
  sendMessage() {
    this.http.get(`${this.apiUrl}/context-propagation`).subscribe((x) => {
      this.responseFromApi = "Success";
    });
  }
  title = 'Tracing Demo';
}
