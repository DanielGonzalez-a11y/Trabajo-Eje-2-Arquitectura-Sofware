package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.IntruccionesReciclaje;
import com.eje2.trabajo.service.InstruccionesReciclajeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/IntruccionesReciclaje")
public class IntruccionesReciclajeController {

	@Autowired
    private InstruccionesReciclajeService instruccionesReciclajeService;

    @GetMapping
    public String listarIntruccionesReciclaje(Model model) {
        model.addAttribute("IntruccionesReciclaje", instruccionesReciclajeService.listarTodas());
        return "pages/IntruccionesReciclaje";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoIntruccionesReciclaje(Model model) {
        model.addAttribute("IntruccionesReciclaje", new IntruccionesReciclaje());
        return "pages/IntruccionesReciclaje";
    }

    @PostMapping
    public String guardarIntruccionesReciclaje(IntruccionesReciclaje intruccionesReciclaje) {
    	instruccionesReciclajeService.guardar(intruccionesReciclaje);
        return "redirect:/IntruccionesReciclaje";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarIntruccionesReciclaje(@PathVariable Long id, Model model) {
        model.addAttribute("IntruccionesReciclaje", instruccionesReciclajeService.obtenerPorId(id));
        return "IntruccionesReciclaje-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarIntruccionesReciclaje(@PathVariable Long id) {
    	instruccionesReciclajeService.eliminar(id);
        return "redirect:/IntruccionesReciclaje";
    }
}
