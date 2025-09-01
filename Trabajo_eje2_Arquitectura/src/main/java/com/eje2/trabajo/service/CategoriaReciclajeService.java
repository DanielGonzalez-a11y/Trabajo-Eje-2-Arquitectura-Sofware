package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.repository.CategoriaReciclajeRepository;
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
