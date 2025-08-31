package com.eje2.trabajo.repository;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CategoriaReciclajeRepository extends JpaRepository<CategoriaReciclaje, Long> {
    CategoriaReciclaje findByNombreCategoria(String nombreCategoria);
}