package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.Usuario;
import com.eje2.trabajo.repository.UsuarioRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UsuarioService {

	@Autowired
    private UsuarioRepository usuarioRepository;

    public List<Usuario> listarTodas() {
        return usuarioRepository.findAll();
    }

    public Usuario guardar(Usuario usuario) {
        return usuarioRepository.save(usuario);
    }

    public Usuario obtenerPorId(Long id) {
        return usuarioRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	usuarioRepository.deleteById(id);
    }
}
