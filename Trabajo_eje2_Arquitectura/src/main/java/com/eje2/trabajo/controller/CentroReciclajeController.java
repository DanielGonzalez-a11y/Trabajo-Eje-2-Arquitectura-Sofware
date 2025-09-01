package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.CentroReciclaje;
import com.eje2.trabajo.service.CentroReciclajeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/CentroReciclaje")
public class CentroReciclajeController {

	@Autowired
    private CentroReciclajeService centroReciclajeService;

    @GetMapping
    public String listarCentroReciclaje(Model model) {
        model.addAttribute("CentroReciclaje", centroReciclajeService.listarTodas());
        return "pages/CentroReciclaje";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoCentroReciclaje(Model model) {
        model.addAttribute("CentroReciclaje", new CentroReciclaje());
        return "pages/CentroReciclaje";
    }

    @PostMapping
    public String guardarCentroReciclaje(CentroReciclaje centroReciclaje) {
    	centroReciclajeService.guardar(centroReciclaje);
        return "redirect:/CentroReciclaje";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarCentroReciclaje(@PathVariable Long id, Model model) {
        model.addAttribute("CentroReciclaje", centroReciclajeService.obtenerPorId(id));
        return "CentroReciclaje-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarCentroReciclaje(@PathVariable Long id) {
    	centroReciclajeService.eliminar(id);
        return "redirect:/CentroReciclaje";
    }
}
