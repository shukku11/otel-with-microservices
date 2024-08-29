import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { LoaderService } from '../loader.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-delay',
  templateUrl: './delay.component.html',
  styleUrls: ['./delay.component.css'],
})
export class DelayComponent {
  responseFromApi!: string;
  constructor(private http: HttpClient,private loaderService: LoaderService) {
    this.isLoading = this.loaderService.loading$
  }

  isLoading: Observable<boolean>;

  apiUrl = 'http://localhost:8002'; // Your API URL

  delay_simulate() {
    this.loaderService.show();
    const headers = new HttpHeaders({
      Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJ1c2VyX25hbWUiOiJzY2hlbWEudGVzdEB0ZXN0LmNvbSIsInVzZXJfdHlwZSI6InRlbmFudF91c2VyIiwidGVuYW50X2lkIjo4LCJyb2xlIjp7InJvbGVfaWQiOjEsInJvbGVfbmFtZSI6InN1cGVyX2FkbWluIiwicGVybWlzc2lvbnMiOnsiZ2xvYmFsIjpbXSwiREUiOltdLCJIQSI6W3sidGVuYW50X29uYm9hcmQiOltdfSx7ImJhc2ljX3VzZXJfYWRtaW5pc3RyYXRpb24iOltdfSx7ImNyZWF0ZV9wcm9qZWN0IjpbXX0seyJlZGEiOltdfSx7ImFmZSI6W119LHsiZGF0YV9hbm5vdGF0aW9uIjpbXX0seyJjb2RlX2NvbXBvc2UiOltdfSx7ImdyYXBoX2Nvbm5lY3QiOltdfSx7ImRvbWFpbl9vbnRvX2Nvbm5lY3QiOltdfSx7ImxmIjpbXX0seyJkZXBsb3ltZW50X3RvX2hpZ2hlcl9lbnZpcm9ubWVudHMiOltdfSx7InBmIjpbXX0seyJ2YWxpZGF0aW9uIHN0dWRpbyI6W119LHsicHVsc2VfbWV0cmljX2luc2lnaHRzIjpbXX0seyJkYXNoYm9hcmQiOltdfSx7InR3b193YXlfY29udmVyc2F0aW9uYWxfYWdlbnQiOltdfV0sIkNBSSI6W119LCJyb2xlX3R5cGUiOiJyZWd1bGFyIiwidGVuYW50X2lkIjpudWxsfSwiZXhwIjoxNzIzODI1MTMwfQ.bRB6gIYkzCbdbZu5_V-mkhI2ITEfa8qBhyA15jIAa1E` // Add the JWT token here
    });

    this.http.get(`${this.apiUrl}/delay-simulate`, {headers}).subscribe((x) => {
      this.responseFromApi = "Success";
      this.loaderService.hide();
    });
  }
}
