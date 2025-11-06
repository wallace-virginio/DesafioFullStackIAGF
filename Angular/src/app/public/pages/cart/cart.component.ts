import { Component } from '@angular/core';
import { CartService, CartItem } from '../../../core/services/cart.service';
import { PublicApiService } from '../../../core/services/public-api.service';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
})
export class CartComponent {
  cartItems$: Observable<CartItem[]>;
  isLoading = false;

  constructor(
    private cartService: CartService,
    private publicApi: PublicApiService,
    private router: Router
  ) {
    this.cartItems$ = this.cartService.cartItems$;
  }

  onCheckout(): void {
    this.isLoading = true;
    const orderItems = this.cartService.getCartForCheckout();

    if (orderItems.length === 0) {
      alert('Seu carrinho está vazio.');
      this.isLoading = false;
      return;
    }

    this.publicApi.createOrder(orderItems).subscribe({
      next: (orderResponse) => {
        alert(`Pedido #${orderResponse.id} realizado com sucesso!`);
        this.cartService.clearCart();
        this.isLoading = false;
        // Redireciona de volta ao catálogo
        this.router.navigate(['/']);
      },
      error: (err) => {
        console.error(err);
        alert('Falha ao realizar o pedido.');
        this.isLoading = false;
      },
    });
  }
}
