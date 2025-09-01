package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.ConsejoEcologico;
import com.eje2.trabajo.repository.ConsejoEcologicoRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ConsejoEcologicoService {

	@Autowired
    private ConsejoEcologicoRepository consejoEcologicoRepository;

    public List<ConsejoEcologico> listarTodas() {
        return consejoEcologicoRepository.findAll();
    }

    public ConsejoEcologico guardar(ConsejoEcologico consejoEcologico) {
        return consejoEcologicoRepository.save(consejoEcologico);
    }

    public ConsejoEcologico obtenerPorId(Long id) {
        return consejoEcologicoRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	consejoEcologicoRepository.deleteById(id);
    }
}
