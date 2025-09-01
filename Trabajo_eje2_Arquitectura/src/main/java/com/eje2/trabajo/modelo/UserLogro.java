package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "user_logros")
public class UserLogro {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_logro;

    @ManyToOne
    @JoinColumn(name = "id_usuario")
    private Usuario usuario;

    private String tipo_logro;

    @Column(name = "fecha_obtencion")
    private LocalDateTime fechaObtencion;

	public Long getId_logro() {
		return id_logro;
	}

	public void setId_logro(Long id_logro) {
		this.id_logro = id_logro;
	}

	public Usuario getUsuario() {
		return usuario;
	}

	public void setUsuario(Usuario usuario) {
		this.usuario = usuario;
	}

	public String getTipo_logro() {
		return tipo_logro;
	}

	public void setTipo_logro(String tipo_logro) {
		this.tipo_logro = tipo_logro;
	}

	public LocalDateTime getFechaObtencion() {
		return fechaObtencion;
	}

	public void setFechaObtencion(LocalDateTime fechaObtencion) {
		this.fechaObtencion = fechaObtencion;
	}
    
}
