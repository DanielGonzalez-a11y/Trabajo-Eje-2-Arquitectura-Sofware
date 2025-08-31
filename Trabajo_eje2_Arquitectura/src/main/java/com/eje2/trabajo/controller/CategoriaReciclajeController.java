package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.service.CategoriaReciclajeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/categorias")
public class CategoriaReciclajeController {
    
    @Autowired
    private CategoriaReciclajeService categoriaService;
    
    @GetMapping
    public List<CategoriaReciclaje> obtenerTodasCategorias() {
        return categoriaService.obtenerTodasCategorias();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<CategoriaReciclaje> obtenerCategoriaPorId(@PathVariable Long id) {
        Optional<CategoriaReciclaje> categoria = categoriaService.obtenerCategoriaPorId(id);
        return categoria.map(ResponseEntity::ok)
                       .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public CategoriaReciclaje crearCategoria(@RequestBody CategoriaReciclaje categoria) {
        return categoriaService.guardarCategoria(categoria);
    }
}