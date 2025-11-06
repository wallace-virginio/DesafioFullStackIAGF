import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AdminApiService } from '../../../core/services/admin-api.service';
import { Product } from '../../../core/models/product.model';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss'],
})
export class ProductListComponent implements OnInit {
  products$!: Observable<Product[]>;

  constructor(
    private adminApi: AdminApiService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.products$ = this.adminApi.getProducts();
  }

  deleteProduct(id: number): void {
    if (confirm('Tem certeza que deseja deletar este produto?')) {
      this.adminApi.deleteProduct(id).subscribe({
        next: () => {
          this.loadProducts();
        },
        error: (err: any) => alert('Falha ao deletar o produto.'),
      });
    }
  }

  logout(): void {
    this.authService.logout();
  }
}
