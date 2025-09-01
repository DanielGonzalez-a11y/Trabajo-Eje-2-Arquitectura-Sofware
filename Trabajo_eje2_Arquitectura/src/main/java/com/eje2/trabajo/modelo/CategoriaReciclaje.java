package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;
import com.eje2.trabajo.modelo.TipoMaterial;

@Entity
@Table(name = "categorias_reciclaje")
public class CategoriaReciclaje {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_categoria;

    private String nombre_categoria;
    private String descripcion;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL)
    private List<TipoMaterial> materiales;

	public Long getId_categoria() {
		return id_categoria;
	}

	public void setId_categoria(Long id_categoria) {
		this.id_categoria = id_categoria;
	}

	public String getNombre_categoria() {
		return nombre_categoria;
	}

	public void setNombre_categoria(String nombre_categoria) {
		this.nombre_categoria = nombre_categoria;
	}

	public String getDescripcion() {
		return descripcion;
	}

	public void setDescripcion(String descripcion) {
		this.descripcion = descripcion;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}

	public List<TipoMaterial> getMateriales() {
		return materiales;
	}

	public void setMateriales(List<TipoMaterial> materiales) {
		this.materiales = materiales;
	}
    
    
}
