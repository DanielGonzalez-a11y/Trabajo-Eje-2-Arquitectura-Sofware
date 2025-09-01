package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.service.CategoriaReciclajeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/CategoriaReciclaje")
public class CategoriaReciclajeController {

	@Autowired
    private CategoriaReciclajeService categoriaReciclajeService;

    @GetMapping
    public String listarCategoriaReciclaje(Model model) {
        model.addAttribute("CategoriaReciclaje", categoriaReciclajeService.listarTodas());
        return "pages/CategoriaReciclaje";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoCategoriaReciclaje(Model model) {
        model.addAttribute("CategoriaReciclaje", new CategoriaReciclaje());
        return "pages/CategoriaReciclaje";
    }

    @PostMapping
    public String guardarCategoriaReciclaje(CategoriaReciclaje categoriaReciclaje) {
    	categoriaReciclajeService.guardar(categoriaReciclaje);
        return "redirect:/usuarios";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarCategoriaReciclaje(@PathVariable Long id, Model model) {
        model.addAttribute("CategoriaReciclaje", categoriaReciclajeService.obtenerPorId(id));
        return "CategoriaReciclaje-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarCategoriaReciclaje(@PathVariable Long id) {
    	categoriaReciclajeService.eliminar(id);
        return "redirect:/CategoriaReciclaje";
    }
}
