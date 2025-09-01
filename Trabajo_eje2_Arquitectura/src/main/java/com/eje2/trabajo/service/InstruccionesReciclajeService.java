package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.IntruccionesReciclaje;
import com.eje2.trabajo.repository.IntruccionesReciclajeRepository;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class InstruccionesReciclajeService {

	@Autowired
    private IntruccionesReciclajeRepository intruccionesReciclajeRepository;

    public List<IntruccionesReciclaje> listarTodas() {
        return intruccionesReciclajeRepository.findAll();
    }

    public IntruccionesReciclaje guardar(IntruccionesReciclaje intruccionesReciclaje) {
        return intruccionesReciclajeRepository.save(intruccionesReciclaje);
    }

    public IntruccionesReciclaje obtenerPorId(Long id) {
        return intruccionesReciclajeRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	intruccionesReciclajeRepository.deleteById(id);
    }
}
