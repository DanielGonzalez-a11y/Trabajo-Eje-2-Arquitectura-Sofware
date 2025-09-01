package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.UserLogro;
import com.eje2.trabajo.service.UserLogroService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/UserLogro")
public class UserLogroController {

	@Autowired
    private UserLogroService userLogroService;

    @GetMapping
    public String listarUserLogro(Model model) {
        model.addAttribute("UserLogro", userLogroService.listarTodas());
        return "pages/UserLogro";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoUserLogro(Model model) {
        model.addAttribute("UserLogro", new UserLogro());
        return "pages/UserLogro";
    }

    @PostMapping
    public String guardarUsuarios(UserLogro userLogro) {
    	userLogroService.guardar(userLogro);
        return "redirect:/usuarios";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarUserLogro(@PathVariable Long id, Model model) {
        model.addAttribute("UserLogro", userLogroService.obtenerPorId(id));
        return "UserLogro-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarUserLogro(@PathVariable Long id) {
    	userLogroService.eliminar(id);
        return "redirect:/UserLogro";
    }
}
