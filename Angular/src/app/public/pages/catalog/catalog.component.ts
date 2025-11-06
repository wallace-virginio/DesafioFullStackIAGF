import { Component, OnInit } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { Product } from '../../../core/models/product.model';
import { PublicApiService } from '../../../core/services/public-api.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { debounceTime, switchMap, startWith } from 'rxjs/operators';
import { CartService } from '../../../core/services/cart.service';

@Component({
  selector: 'app-catalog',
  templateUrl: './catalog.component.html',
  styleUrls: ['./catalog.component.scss'],
})
export class CatalogComponent implements OnInit {
  products$!: Observable<Product[]>;
  categories$!: Observable<string[]>;

  // Filtros Manuais
  manualFiltersForm: FormGroup;

  // Interpretação da AI
  aiInterpretation: string | null = null;

  // BehaviorSubject para guardar o estado atual dos filtros
  private filters$ = new BehaviorSubject<any>({});

  constructor(
    private publicApi: PublicApiService,
    private fb: FormBuilder,
    private cartService: CartService
  ) {
    this.manualFiltersForm = this.fb.group({
      category: [''],
      price_min: [''],
      price_max: [''],
    });
  }

  ngOnInit(): void {
    // Carrega as categorias para o <select>
    this.categories$ = this.publicApi.getCategories();

    // Reage a mudanças nos filtros manuais
    this.manualFiltersForm.valueChanges
      .pipe(
        debounceTime(300) // Espera 300ms após o usuário parar de digitar
      )
      .subscribe((manualFilters) => {
        // Combina com os filtros da AI (se houver)
        const currentFilters = this.filters$.value;
        this.filters$.next({ ...currentFilters, ...manualFilters });
      });

    // O Observable de produtos reage a CADA mudança no filters$
    this.products$ = this.filters$.pipe(
      switchMap((filters) => {
        return this.publicApi.getPublicProducts(filters);
      })
    );
  }

  /**
   * Chamado quando a Busca AI (componente filho) emite um resultado.
   */
  onFiltersFromAI(aiFilters: any): void {
    // Limpa os filtros manuais
    this.manualFiltersForm.reset(
      { category: '', price_min: '', price_max: '' },
      { emitEvent: false }
    );

    // Define os novos filtros vindos da AI
    this.filters$.next(aiFilters);
  }
  // Chamada quando o product-card emite o evento
  handleAddToCart(product: Product): void {
    this.cartService.addItem(product);
  }
}
