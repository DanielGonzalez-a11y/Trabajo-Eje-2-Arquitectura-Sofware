package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.ConsejoEcologico;
import com.eje2.trabajo.service.ConsejoEcologicoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/ConsejoEcologico")
public class ConsejoEcologicoController {

	@Autowired
    private ConsejoEcologicoService consejoEcologicoService;

    @GetMapping
    public String listarConsejoEcologico(Model model) {
        model.addAttribute("ConsejoEcologico", consejoEcologicoService.listarTodas());
        return "pages/ConsejoEcologico";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoConsejoEcologico(Model model) {
        model.addAttribute("ConsejoEcologico", new ConsejoEcologico());
        return "pages/ConsejoEcologico";
    }

    @PostMapping
    public String guardarConsejoEcologico(ConsejoEcologico consejoecologicoService) {
    	consejoEcologicoService.guardar(consejoecologicoService);
        return "redirect:/ConsejoEcologico";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarConsejoEcologico(@PathVariable Long id, Model model) {
        model.addAttribute("ConsejoEcologico", consejoEcologicoService.obtenerPorId(id));
        return "ConsejoEcologico-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarConsejoEcologico(@PathVariable Long id) {
    	consejoEcologicoService.eliminar(id);
        return "redirect:/ConsejoEcologico";
    }
}
