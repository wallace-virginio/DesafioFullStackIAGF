import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard'; // Importa a nova guarda funcional

export const routes: Routes = [
  // Rota de Login (Carrega um componente standalone)
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(c => c.LoginComponent)
  },

  // Área Restrita (Admin/ONG)
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule),
    canActivate: [authGuard] // Protege este módulo e seus filhos
  },

  // Portal Público (Catálogo, Carrinho)
  {
    path: '', // Rota padrão
    loadChildren: () => import('./public/public.module').then(m => m.PublicModule)
  },

  // Redirecionamento padrão
  {
    path: '**',
    redirectTo: ''
  }
];