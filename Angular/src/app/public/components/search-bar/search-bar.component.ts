import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import {
  PublicApiService,
  AISearchResponse,
} from '../../../core/services/public-api.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
})
export class SearchBarComponent {
  searchForm: FormGroup;
  isLoading = false;

  @Output() filtersApplied = new EventEmitter<any>();
  @Output() aiInterpretation = new EventEmitter<string | null>();

  constructor(private fb: FormBuilder, private publicApi: PublicApiService) {
    this.searchForm = this.fb.group({
      query: [''],
    });
  }

  onSearchSubmit(): void {
    const query = this.searchForm.value.query;
    if (!query) {
      // Se a busca for vazia, limpa os filtros
      this.filtersApplied.emit({});
      this.aiInterpretation.emit(null);
      return;
    }

    this.isLoading = true;
    this.aiInterpretation.emit('Interpretando busca...');

    this.publicApi
      .searchWithAI(query)
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response: AISearchResponse) => {
          this.aiInterpretation.emit(response.interpretation);
          this.filtersApplied.emit(response.applied_filters);
        },
        error: (err) => {
          this.aiInterpretation.emit('Erro da AI. Usando busca simples.');
          this.filtersApplied.emit({ search: query });
        },
      });
  }
}
