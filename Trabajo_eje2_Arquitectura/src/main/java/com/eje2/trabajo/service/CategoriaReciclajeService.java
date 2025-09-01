package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.repository.CategoriaReciclajeRepository;
<<<<<<< HEAD
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CategoriaReciclajeService {

	@Autowired
    private CategoriaReciclajeRepository categoriaReciclajeRepository;

    public List<CategoriaReciclaje> listarTodas() {
        return categoriaReciclajeRepository.findAll();
    }

    public CategoriaReciclaje guardar(CategoriaReciclaje categoriaReciclaje) {
        return categoriaReciclajeRepository.save(categoriaReciclaje);
    }

    public CategoriaReciclaje obtenerPorId(Long id) {
        return categoriaReciclajeRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	categoriaReciclajeRepository.deleteById(id);
    }
}
=======
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
>>>>>>> 6d2c170b4adab05bd95deecdf0faf5732c2a68b7
