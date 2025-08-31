package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "tipos_material")
public class TipoMaterial {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_material;

    @ManyToOne
    @JoinColumn(name = "id_categoria")
    private CategoriaReciclaje categoria;

    private String nombre_material;
    private String descripcion;
    private String tiempo_descomposicion;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

	public Long getId_material() {
		return id_material;
	}

	public void setId_material(Long id_material) {
		this.id_material = id_material;
	}

	public CategoriaReciclaje getCategoria() {
		return categoria;
	}

	public void setCategoria(CategoriaReciclaje categoria) {
		this.categoria = categoria;
	}

	public String getNombre_material() {
		return nombre_material;
	}

	public void setNombre_material(String nombre_material) {
		this.nombre_material = nombre_material;
	}

	public String getDescripcion() {
		return descripcion;
	}

	public void setDescripcion(String descripcion) {
		this.descripcion = descripcion;
	}

	public String getTiempo_descomposicion() {
		return tiempo_descomposicion;
	}

	public void setTiempo_descomposicion(String tiempo_descomposicion) {
		this.tiempo_descomposicion = tiempo_descomposicion;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}

    
}

