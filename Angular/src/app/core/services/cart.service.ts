import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Product } from '../../core/models/product.model';

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface OrderItemCreateDTO {
  product_id: number;
  quantity: number;
}

@Injectable({
  providedIn: 'root',
})
export class CartService {
  private cartItems = new BehaviorSubject<CartItem[]>([]);
  public cartItems$ = this.cartItems.asObservable();

  constructor() {}

  addItem(product: Product): void {
    const currentItems = this.cartItems.getValue();
    const existingItem = currentItems.find(
      (item: { product: { id: number } }) => item.product.id === product.id
    );

    if (existingItem) {
      existingItem.quantity++;
    } else {
      currentItems.push({ product: product, quantity: 1 });
    }
    this.cartItems.next([...currentItems]);
    alert(`${product.name} adicionado ao carrinho!`);
  }

  getCartForCheckout(): OrderItemCreateDTO[] {
    return this.cartItems.getValue().map((item) => ({
      product_id: item.product.id,
      quantity: item.quantity,
    }));
  }

  clearCart(): void {
    this.cartItems.next([]);
  }
}
