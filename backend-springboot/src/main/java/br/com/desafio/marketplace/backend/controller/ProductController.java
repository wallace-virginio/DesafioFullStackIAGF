package br.com.desafio.marketplace.backend.controller;

import br.com.desafio.marketplace.backend.model.Product;
import br.com.desafio.marketplace.backend.model.Organization;
import br.com.desafio.marketplace.backend.repository.ProductRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/ong/products")
public class ProductController {

    @Autowired
    private ProductRepository productRepository;

    private Specification<Product> orgFilter(UUID organizationId) {
        return (root, query, cb) -> cb.equal(root.get("organization").get("id"), organizationId);
    }

    private UUID getAuthenticatedOrganizationId() {
        return UUID.fromString("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11");
    }

    @GetMapping
    public List<Product> getMyProducts() {
        UUID orgId = getAuthenticatedOrganizationId();
        return productRepository.findAll(orgFilter(orgId));
    }

    @GetMapping("/{id}")
    public Product getMyProductById(@PathVariable UUID id) {
        UUID orgId = getAuthenticatedOrganizationId();

        Optional<Product> product = productRepository.findByOrganizationIdAndId(orgId, id);

        return product.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
                "Product not found or does not belong to this organization"));
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        UUID orgId = getAuthenticatedOrganizationId();

        Organization org = new Organization();
        org.setId(orgId);
        product.setOrganization(org);
        product.setId(null);

        Product savedProduct = productRepository.save(product);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedProduct);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable UUID id, @RequestBody Product productDetails) {
        UUID orgId = getAuthenticatedOrganizationId();

        Product existingProduct = productRepository.findByOrganizationIdAndId(orgId, id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found"));

        existingProduct.setName(productDetails.getName());
        existingProduct.setDescription(productDetails.getDescription());
        existingProduct.setPrice(productDetails.getPrice());
        existingProduct.setCategory(productDetails.getCategory());
        existingProduct.setImageUrl(productDetails.getImageUrl());
        existingProduct.setStockQty(productDetails.getStockQty());
        existingProduct.setWeightGrams(productDetails.getWeightGrams());

        Product updatedProduct = productRepository.save(existingProduct);
        return ResponseEntity.ok(updatedProduct);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable UUID id) {
        UUID orgId = getAuthenticatedOrganizationId();

        Product productToDelete = productRepository.findByOrganizationIdAndId(orgId, id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found"));

        productRepository.delete(productToDelete);

        return ResponseEntity.noContent().build();
    }
}