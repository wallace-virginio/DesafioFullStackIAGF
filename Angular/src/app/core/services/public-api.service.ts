import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, Inject, PLATFORM_ID } from '@angular/core'; // 1. Importe
import { isPlatformBrowser } from '@angular/common'; // 2. Importe
import { Observable } from 'rxjs';
import { Product } from '../../core/models/product.model';
import { OrderItemCreateDTO } from './cart.service';
// Interface para a resposta da Busca AI
export interface AISearchResponse {
  interpretation: string;
  applied_filters: any;
  is_fallback: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class PublicApiService {
  private API_URL: string; // 3. Mude isto

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object // 4. Injete
  ) {
    // 5. Adicione esta lógica
    if (isPlatformBrowser(this.platformId)) {
      this.API_URL = 'http://localhost:8000';
    } else {
      this.API_URL = 'http://backend:8000';
    }
  }

  /**
   * Busca produtos publicamente com filtros.
   * A API /public/products já está pronta para receber estes parâmetros.
   */
  getPublicProducts(filters: any = {}): Observable<Product[]> {
    let params = new HttpParams();

    // Constrói os parâmetros de query baseados nos filtros
    if (filters.search) {
      params = params.set('search', filters.search);
    }
    if (filters.category) {
      params = params.set('category', filters.category);
    }
    if (filters.price_min) {
      params = params.set('price_min', filters.price_min);
    }
    if (filters.price_max) {
      params = params.set('price_max', filters.price_max);
    }

    // Adiciona paginação (vamos manter simples por agora)
    params = params.set('skip', '0');
    params = params.set('limit', '50');

    return this.http.get<Product[]>(`${this.API_URL}/public/products`, {
      params,
    });
  }

  // Busca as categorias para os filtros manuais
  getCategories(): Observable<string[]> {
    return this.http.get<string[]>(`${this.API_URL}/public/categories`);
  }

  // Envia a query de linguagem natural para a AI
  searchWithAI(queryText: string): Observable<AISearchResponse> {
    return this.http.post<AISearchResponse>(
      `${this.API_URL}/public/search-ai`,
      { query: queryText }
    );
  }
  // POST /public/orders
  createOrder(items: OrderItemCreateDTO[]): Observable<any> {
    const payload = { items: items };
    return this.http.post(`${this.API_URL}/public/orders`, payload);
  }
}
