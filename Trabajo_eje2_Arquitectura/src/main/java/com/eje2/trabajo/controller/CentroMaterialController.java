package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.CentroMaterial;
import com.eje2.trabajo.service.CentroMaterialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/CentroMaterial")
public class CentroMaterialController {

	@Autowired
    private CentroMaterialService centroMaterialService;

    @GetMapping
    public String listarCentroMaterial(Model model) {
        model.addAttribute("CentroMaterial", centroMaterialService.listarTodas());
        return "pages/CentroMaterial";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoCentroMaterial(Model model) {
        model.addAttribute("CentroMaterial", new CentroMaterial());
        return "pages/CentroMaterial";
    }

    @PostMapping
    public String guardarCentroMaterial(CentroMaterial centroMaterial) {
    	centroMaterialService.guardar(centroMaterial);
        return "redirect:/CentroMaterial";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarCentroMaterial(@PathVariable Long id, Model model) {
        model.addAttribute("CentroMaterial", centroMaterialService.obtenerPorId(id));
        return "CentroMaterial-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarCentroMaterial(@PathVariable Long id) {
    	centroMaterialService.eliminar(id);
    	return "redirect:/CentroMaterial";
    }
}
