import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Verifica o estado de autenticação do AuthService
  return authService.isAuthenticated$.pipe(
    map(isAuthenticated => {
      if (isAuthenticated) {
        return true; // Usuário logado, permite o acesso
      } else {
        // Usuário não logado, redireciona para /login
        return router.createUrlTree(['/login']);
      }
    })
  );
};