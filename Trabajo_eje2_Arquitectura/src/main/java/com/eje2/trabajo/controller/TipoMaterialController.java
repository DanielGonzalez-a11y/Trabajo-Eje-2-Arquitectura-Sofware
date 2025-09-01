package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.TipoMaterial;
import com.eje2.trabajo.service.TipoMaterialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;


@Controller
@RequestMapping("/TipoMaterial")
public class TipoMaterialController {

	@Autowired
    private TipoMaterialService tipoMaterialService;

    @GetMapping
    public String listarTipoMaterial(Model model) {
        model.addAttribute("TipoMaterial", tipoMaterialService.listarTodas());
        return "pages/TipoMaterial";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoTipoMaterial(Model model) {
        model.addAttribute("TipoMaterial", new TipoMaterial());
        return "pages/TipoMaterial";
    }

    @PostMapping
    public String guardarTipoMaterial(TipoMaterial tipoMaterial) {
    	tipoMaterialService.guardar(tipoMaterial);
        return "redirect:/TipoMaterial";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarTipoMaterial(@PathVariable Long id, Model model) {
        model.addAttribute("TipoMaterial", tipoMaterialService.obtenerPorId(id));
        return "TipoMaterial-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarTipoMaterial(@PathVariable Long id) {
    	tipoMaterialService.eliminar(id);
        return "redirect:/TipoMaterial";
    }
}
