package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "preguntas_frecuentes")
public class PreguntaFrecuente {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_pregunta;

    private String pregunta;
    private String respuesta;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

	public Long getId_pregunta() {
		return id_pregunta;
	}

	public void setId_pregunta(Long id_pregunta) {
		this.id_pregunta = id_pregunta;
	}

	public String getPregunta() {
		return pregunta;
	}

	public void setPregunta(String pregunta) {
		this.pregunta = pregunta;
	}

	public String getRespuesta() {
		return respuesta;
	}

	public void setRespuesta(String respuesta) {
		this.respuesta = respuesta;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}
    
}
