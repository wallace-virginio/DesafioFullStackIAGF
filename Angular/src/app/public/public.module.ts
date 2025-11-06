import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { PublicRoutingModule } from './public-routing.module';
import { CatalogComponent } from './pages/catalog/catalog.component';
import { ProductCardComponent } from './components/product-card/product-card.component';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { CartComponent } from './pages/cart/cart.component';

@NgModule({
  declarations: [
    CatalogComponent,
    ProductCardComponent,
    SearchBarComponent,
    CartComponent,
  ],
  imports: [CommonModule, PublicRoutingModule, ReactiveFormsModule],
})
export class PublicModule {}
