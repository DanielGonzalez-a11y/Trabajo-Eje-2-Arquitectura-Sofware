package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.TipoMaterial;
import com.eje2.trabajo.repository.TipoMaterialRepository;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TipoMaterialService {

	@Autowired
    private TipoMaterialRepository tipoMaterialRepository;

    public List<TipoMaterial> listarTodas() {
        return tipoMaterialRepository.findAll();
    }

    public TipoMaterial guardar(TipoMaterial tipoMaterial) {
        return tipoMaterialRepository.save(tipoMaterial);
    }

    public TipoMaterial obtenerPorId(Long id) {
        return tipoMaterialRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	tipoMaterialRepository.deleteById(id);
    }
}
