package com.eje2.trabajo.controller;

<<<<<<< HEAD
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
public class CategoriaReciclajeController {

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
    public String mostrarFormularioEditarUsuario(@PathVariable Long id, Model model) {
        model.addAttribute("usuario", centroReciclajeService.obtenerPorId(id));
        return "CentroReciclaje-form";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminarCentroReciclaje(@PathVariable Long id) {
    	centroReciclajeService.eliminar(id);
        return "redirect:/CentroReciclaje";
    }
}
=======
import com.eje2.trabajo.modelo.CategoriaReciclaje;
import com.eje2.trabajo.service.CategoriaReciclajeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/categorias")
public class CategoriaReciclajeController {
    
    @Autowired
    private CategoriaReciclajeService categoriaService;
    
    @GetMapping
    public List<CategoriaReciclaje> obtenerTodasCategorias() {
        return categoriaService.obtenerTodasCategorias();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<CategoriaReciclaje> obtenerCategoriaPorId(@PathVariable Long id) {
        Optional<CategoriaReciclaje> categoria = categoriaService.obtenerCategoriaPorId(id);
        return categoria.map(ResponseEntity::ok)
                       .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public CategoriaReciclaje crearCategoria(@RequestBody CategoriaReciclaje categoria) {
        return categoriaService.guardarCategoria(categoria);
    }
}
>>>>>>> 6d2c170b4adab05bd95deecdf0faf5732c2a68b7
