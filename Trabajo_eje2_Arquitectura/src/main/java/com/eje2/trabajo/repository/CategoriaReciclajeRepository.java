package com.eje2.trabajo.repository;

import com.eje2.trabajo.modelo.CategoriaReciclaje;
import org.springframework.data.jpa.repository.JpaRepository;
<<<<<<< HEAD

public interface CategoriaReciclajeRepository extends JpaRepository<CategoriaReciclaje, Long>{

}
=======
import org.springframework.stereotype.Repository;

@Repository
public interface CategoriaReciclajeRepository extends JpaRepository<CategoriaReciclaje, Long> {
    CategoriaReciclaje findByNombreCategoria(String nombreCategoria);
}
>>>>>>> 6d2c170b4adab05bd95deecdf0faf5732c2a68b7
