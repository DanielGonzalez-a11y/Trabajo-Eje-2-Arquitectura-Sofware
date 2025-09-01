package com.eje2.trabajo.controller;

import com.eje2.trabajo.modelo.Usuario;
import com.eje2.trabajo.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/usuarios")
public class UsuarioController {

	@Autowired
    private UsuarioService usuarioService;

    @GetMapping
    public String listarUsuario(Model model) {
        model.addAttribute("usuarios", usuarioService.listarTodas());
        return "pages/Usuarios";
    }

    @GetMapping("/nuevo")
    public String mostrarFormularioNuevoUsuario(Model model) {
        model.addAttribute("usuario", new Usuario());
        return "pages/Usuarios";
    }

    @PostMapping
    public String guardarUsuarios(Usuario usuario) {
    	usuarioService.guardar(usuario);
        return "redirect:/usuarios";
    }

    @GetMapping("/editar/{id}")
    public String mostrarFormularioEditarUsuario(@PathVariable Long id, Model model) {
        model.addAttribute("usuario", usuarioService.obtenerPorId(id));
        return "usuario-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarUsuario(@PathVariable Long id) {
    	usuarioService.eliminar(id);
        return "redirect:/usuarios";
    }
}
