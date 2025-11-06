import { Component, Input, Output, EventEmitter } from '@angular/core'; // 1. Importa Output e EventEmitter
import { Product } from '../../../core/models/product.model';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss'],
})
export class ProductCardComponent {
  @Input() product!: Product;

  // 2. Cria um evento de output
  @Output() addToCart = new EventEmitter<Product>();

  // 3. Função chamada pelo clique do botão
  onAddToCart(): void {
    this.addToCart.emit(this.product);
  }
}
