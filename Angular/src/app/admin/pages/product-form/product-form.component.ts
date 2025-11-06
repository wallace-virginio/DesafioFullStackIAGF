import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AdminApiService } from '../../../core/services/admin-api.service';
import { ProductCreateDTO } from '../../../core/models/product.model';
import { Product } from '../../../core/models/product.model';

@Component({
  selector: 'app-product-form',
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.scss'],
})
export class ProductFormComponent implements OnInit {
  productForm: FormGroup;
  isEditMode = false;
  productId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private adminApi: AdminApiService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.productForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      price: [0, [Validators.required, Validators.min(0.01)]],
      category: ['', Validators.required],
      image_url: [''],
      stock_qty: [0, [Validators.required, Validators.min(0)]],
      weight_grams: [0, [Validators.required, Validators.min(1)]],
    });
  }

  ngOnInit(): void {
    this.productId = this.route.snapshot.paramMap.get('id');

    if (this.productId) {
      this.isEditMode = true;
      this.adminApi.getProduct(this.productId).subscribe((product: Product) => {
        this.productForm.patchValue(product);
      });
    }
  }

  onSubmit(): void {
    if (this.productForm.invalid) {
      return;
    }

    const productData = this.productForm.value as ProductCreateDTO;

    if (this.isEditMode && this.productId) {
      this.adminApi.updateProduct(this.productId, productData).subscribe({
        next: () => this.router.navigate(['/admin']),
        error: (err: any) => alert('Falha ao atualizar produto.'),
      });
    } else {
      this.adminApi.createProduct(productData).subscribe({
        next: () => this.router.navigate(['/admin']),
        error: (err: any) => alert('Falha ao criar produto.'),
      });
    }
  }
}
