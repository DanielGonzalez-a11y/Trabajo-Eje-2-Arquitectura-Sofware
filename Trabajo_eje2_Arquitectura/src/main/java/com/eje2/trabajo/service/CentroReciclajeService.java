package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.CentroReciclaje;
import com.eje2.trabajo.repository.CentroReciclajeRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CentroReciclajeService {

	@Autowired
    private CentroReciclajeRepository centroReciclajeRepository;

    public List<CentroReciclaje> listarTodas() {
        return centroReciclajeRepository.findAll();
    }

    public CentroReciclaje guardar(CentroReciclaje centroReciclaje) {
        return centroReciclajeRepository.save(centroReciclaje);
    }

    public CentroReciclaje obtenerPorId(Long id) {
        return centroReciclajeRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	centroReciclajeRepository.deleteById(id);
    }
}
