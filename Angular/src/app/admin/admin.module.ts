import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms'; // 1. Importe o Módulo de Formulários

import { AdminRoutingModule } from './admin-routing.module';
import { ProductListComponent } from './pages/product-list/product-list.component';
import { ProductFormComponent } from './pages/product-form/product-form.component';

@NgModule({
  declarations: [
    ProductListComponent,
    ProductFormComponent, // 2. Declare os componentes
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    ReactiveFormsModule, // 3. Adicione o módulo aqui
  ],
})
export class AdminModule {}
