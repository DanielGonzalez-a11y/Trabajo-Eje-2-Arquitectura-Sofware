package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.CentroMaterial;
import com.eje2.trabajo.repository.CentroMaterialRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CentroMaterialService {

	@Autowired
    private CentroMaterialRepository centroMaterialRepository;

    public List<CentroMaterial> listarTodas() {
        return centroMaterialRepository.findAll();
    }

    public CentroMaterial guardar(CentroMaterial centroMaterial) {
        return centroMaterialRepository.save(centroMaterial);
    }

    public CentroMaterial obtenerPorId(Long id) {
        return centroMaterialRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	centroMaterialRepository.deleteById(id);
    }
}
