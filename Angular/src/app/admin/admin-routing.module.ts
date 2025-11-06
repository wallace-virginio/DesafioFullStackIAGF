import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductListComponent } from './pages/product-list/product-list.component';
import { ProductFormComponent } from './pages/product-form/product-form.component';

const routes: Routes = [
  // Rota /admin (padrão) -> Lista de Produtos
  {
    path: '',
    component: ProductListComponent
  },
  // Rota /admin/new -> Formulário de Criação
  {
    path: 'new',
    component: ProductFormComponent
  },
  // Rota /admin/edit/123 -> Formulário de Edição
  {
    path: 'edit/:id',
    component: ProductFormComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }