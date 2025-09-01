package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "consejos_ecologicos")
public class ConsejoEcologico {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_consejo;

    private String titulo;
    private String contenido;
    private String imagen_url;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

	public Long getId_consejo() {
		return id_consejo;
	}

	public void setId_consejo(Long id_consejo) {
		this.id_consejo = id_consejo;
	}

	public String getTitulo() {
		return titulo;
	}

	public void setTitulo(String titulo) {
		this.titulo = titulo;
	}

	public String getContenido() {
		return contenido;
	}

	public void setContenido(String contenido) {
		this.contenido = contenido;
	}

	public String getImagen_url() {
		return imagen_url;
	}

	public void setImagen_url(String imagen_url) {
		this.imagen_url = imagen_url;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}
    
}
