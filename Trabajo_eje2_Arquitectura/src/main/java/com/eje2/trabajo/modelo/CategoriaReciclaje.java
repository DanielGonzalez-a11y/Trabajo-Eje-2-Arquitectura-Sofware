package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "categorias_reciclaje")
public class CategoriaReciclaje {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_categoria")
    private Long idCategoria;
    
    @Column(name = "nombre_categoria", nullable = false, length = 100)
    private String nombreCategoria;
    
    @Column(name = "descripcion")
    private String descripcionCategoria;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    public CategoriaReciclaje() {
        this.createdAt = LocalDateTime.now();
    }
}