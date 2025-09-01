package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.PreguntaFrecuente;
import com.eje2.trabajo.repository.PreguntasFrecuentesRepository;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PreguntasFrecuentesService {

	@Autowired
    private PreguntasFrecuentesRepository preguntasFrecuentesRepository;

    public List<PreguntaFrecuente> listarTodas() {
        return preguntasFrecuentesRepository.findAll();
    }

    public PreguntaFrecuente guardar(PreguntaFrecuente preguntaFrecuente) {
        return preguntasFrecuentesRepository.save(preguntaFrecuente);
    }

    public PreguntaFrecuente obtenerPorId(Long id) {
        return preguntasFrecuentesRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	preguntasFrecuentesRepository.deleteById(id);
    }
}
