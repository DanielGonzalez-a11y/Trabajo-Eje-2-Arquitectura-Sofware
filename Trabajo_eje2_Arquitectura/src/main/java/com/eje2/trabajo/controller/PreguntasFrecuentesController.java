package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.PreguntaFrecuente;
import com.eje2.trabajo.service.PreguntasFrecuentesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/PreguntaFrecuente")
public class PreguntasFrecuentesController {

	@Autowired
    private PreguntasFrecuentesService preguntasFrecuentesService;

    @GetMapping
    public String listarPreguntaFrecuente(Model model) {
        model.addAttribute("PreguntaFrecuente", preguntasFrecuentesService.listarTodas());
        return "pages/PreguntaFrecuente";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoUsuario(Model model) {
        model.addAttribute("PreguntaFrecuente", new PreguntaFrecuente());
        return "pages/PreguntaFrecuente";
    }

    @PostMapping
    public String guardarPreguntaFrecuente(PreguntaFrecuente preguntaFrecuente) {
    	preguntasFrecuentesService.guardar(preguntaFrecuente);
        return "redirect:/PreguntaFrecuente";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarPreguntaFrecuente(@PathVariable Long id, Model model) {
        model.addAttribute("PreguntaFrecuente", preguntasFrecuentesService.obtenerPorId(id));
        return "PreguntaFrecuente-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarPreguntaFrecuente(@PathVariable Long id) {
    	preguntasFrecuentesService.eliminar(id);
        return "redirect:/PreguntaFrecuente";
    }
}
