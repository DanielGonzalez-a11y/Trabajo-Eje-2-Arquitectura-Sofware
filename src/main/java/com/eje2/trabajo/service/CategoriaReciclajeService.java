package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.repository.CategoriaReciclajeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CategoriaReciclajeService {
    
    @Autowired
    private CategoriaReciclajeRepository categoriaRepository;
    
    public List<CategoriaReciclaje> obtenerTodasCategorias() {
        return categoriaRepository.findAll();
    }
    
    public Optional<CategoriaReciclaje> obtenerCategoriaPorId(Long id) {
        return categoriaRepository.findById(id);
    }
    
    public CategoriaReciclaje guardarCategoria(CategoriaReciclaje categoria) {
        return categoriaRepository.save(categoria);
    }
    
    public void eliminarCategoria(Long id) {
        categoriaRepository.deleteById(id);
    }
}