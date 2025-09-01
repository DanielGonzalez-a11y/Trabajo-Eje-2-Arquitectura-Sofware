package com.eje2.trabajo.service;

import com.eje2.trabajo.modelo.UserLogro;
import com.eje2.trabajo.repository.UserLogroRepository;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserLogroService {
	
	@Autowired
    private UserLogroRepository userLogroRepository;

    public List<UserLogro> listarTodas() {
        return userLogroRepository.findAll();
    }

    public UserLogro guardar(UserLogro userLogro) {
        return userLogroRepository.save(userLogro);
    }

    public UserLogro obtenerPorId(Long id) {
        return userLogroRepository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
    	userLogroRepository.deleteById(id);
    }
    
}
