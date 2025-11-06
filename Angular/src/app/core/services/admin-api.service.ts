import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import { Product } from '../models/product.model';
import { ProductCreateDTO } from '../models/product.model';

@Injectable({
  providedIn: 'root',
})
export class AdminApiService {
  private API_URL: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    if (isPlatformBrowser(this.platformId)) {
      this.API_URL = 'http://localhost:8000';
    } else {
      this.API_URL = 'http://backend:8000';
    }
  }

  // GET /products (Lista produtos da ONG logada)
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.API_URL}/products/`);
  }

  // GET /products/{id} (Busca um produto específico)
  getProduct(id: string): Observable<Product> {
    return this.http.get<Product>(`${this.API_URL}/products/${id}`);
  }

  // POST /products (Cria um novo produto)
  createProduct(product: ProductCreateDTO): Observable<Product> {
    return this.http.post<Product>(`${this.API_URL}/products/`, product);
  }

  // PUT /products/{id} (Atualiza um produto)
  updateProduct(id: string, product: ProductCreateDTO): Observable<Product> {
    return this.http.put<Product>(`${this.API_URL}/products/${id}`, product);
  }

  // DELETE /products/{id} (Deleta um produto)
  deleteProduct(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/products/${id}`);
  }
}
