import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CommonModule } from '@angular/common'; // Necessário para *ngIf

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule, // Importa o CommonModule
    ReactiveFormsModule, // Importa o ReactiveFormsModule
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      // Preenchemos com os dados do seed.py para facilitar o teste
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.errorMessage = null;
    const { email, password } = this.loginForm.value;

    this.authService.login(email, password).subscribe({
      next: () => {
        // Sucesso: Redireciona para o dashboard da ONG
        this.router.navigate(['/admin']);
      },
      error: (err) => {
        // Falha: Exibe a mensagem de erro
        this.errorMessage = 'Email ou senha incorretos.';
        console.error(err);
      },
    });
  }
}
