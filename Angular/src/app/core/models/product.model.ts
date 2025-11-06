export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  image_url: string;
  stock_qty: number;
  weight_grams: number;
  organization_id: number;
}
export type ProductCreateDTO = Omit<Product, 'id' | 'organization_id'>;
