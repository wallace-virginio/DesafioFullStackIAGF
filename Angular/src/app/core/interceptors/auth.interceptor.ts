import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  // Se o token existir e a URL não for a de login
  if (token && !req.url.includes('/auth/login')) {
    // Clona a requisição e adiciona o header de autorização
    const clonedRequest = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`)
    });
    return next(clonedRequest);
  }

  // Se não tiver token ou for a rota de login, passa a requisição original
  return next(req);
};